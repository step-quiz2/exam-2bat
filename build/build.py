#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════
#  build.py — valida el banc, compila els PDF i genera cataleg.js
#  ─────────────────────────────────────────────────────────────────────
#  Ús:   python3 build/build.py [opcions]
#
#    --nomes-cataleg     no compila res, només revalida i regenera el
#                        catàleg (ràpid, per a canvis de meta.json)
#    --headers FITXER    compila amb uns altres paquets (per a proves, si a
#                        l'entorn en falten). Aquests PDF no són definitius;
#                        el catàleg porta sempre els oficials.
#    --pregunta RUTA     compila només les preguntes que la contenen
#
#  Modalitats: cada pregunta té una versió per a l'examen d'1 h 30 i, si
#  el .tex la defineix (\apartat[50 min]{1 h 30} i nomesllarg), una altra
#  per al de 50 min, amb els seus PDF (enunciat-curt.pdf, solucio-curt.pdf).
#  Abans de compilar, materialitza() deixa cada versió neta: el que diu el
#  .tex és exactament el que surt al PDF. El lloc fa el mateix.
#
#  El build FALLA (codi 1) i no escriu res si hi ha cap error: ni PDF ni
#  catàleg. Els PDF es compilen en una carpeta temporal i només es copien
#  a out/ al final, quan ja se sap que tot és correcte. És deliberat: val
#  més no publicar que publicar un banc inconsistent.
# ═══════════════════════════════════════════════════════════════════════

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
PUNTS_PREGUNTA = 250          # centèsimes: tota pregunta val 2,50 punts
GRA = 25                      # centèsimes: tot apartat és múltiple de 0,25

CLAUS_META = {
    "titol": str, "temes_secundaris": list, "dificultat": str,
    "origen": list, "minuts": int, "etiquetes": list,
}
DIFICULTATS = {"●○○", "●●○", "●●●"}
# Claus que poden faltar. minuts_curt: minuts a l'examen de 50 min; és
# obligatòria si la pregunta té versió de 50 min, i prohibida si no en té.
OPCIONALS_META = {"minuts_curt": int}

# Preguntes PAU: viuen a pau/<bloc>/<codi>/ i el codi és l'identificador del
# repositori pau (p. ex. ana-26j-q1). Del codi se'n dedueix la convocatòria,
# i de la convocatòria (pau/convocatories.json) la línia de procedència.
CLAUS_META_PAU = {
    "titol": str, "unitats": list, "dificultat": str, "minuts": int, "etiquetes": list,
}
BLOCS_PAU = {"alg": "algebra", "geo": "geometria", "ana": "analisi", "pro": "probabilitat"}
CODI_PAU = re.compile(r"^(alg|geo|ana|pro)-(\d{2}(?:i|j2|j|s))-(q\d[a-z]*)$")
CODI_BANC = re.compile(r"^q\d{3}$")
MESOS = {"juny", "setembre"}

errors: list[str] = []
avisos: list[str] = []


def error(on: str, msg: str) -> None:
    errors.append(f"{on}: {msg}")


def avis(on: str, msg: str) -> None:
    avisos.append(f"{on}: {msg}")


# ── assemblatge ────────────────────────────────────────────────────────
def munta(plantilla: str, preambul: str, cossos: list[str], solucions: bool) -> str:
    """Construeix un .tex complet. El lloc web fa EXACTAMENT això mateix
    amb la mateixa plantilla; per això la plantilla és un fitxer i no
    està escrita dins del codi."""
    # count=1: el mateix que String.replace de JavaScript (només la primera).
    return (plantilla
            .replace("%%SOLUCIONS%%", r"\solucionstrue" if solucions else r"\solucionsfalse", 1)
            .replace("%%PREAMBUL%%", preambul, 1)
            .replace("%%COS%%", "\n\n".join(cossos), 1))


MARCADORS = ("%%SOLUCIONS%%", "%%PREAMBUL%%", "%%COS%%")


def valida_plantilla(plantilla: str) -> None:
    for m in MARCADORS:
        n = plantilla.count(m)
        if n != 1:
            error("embolcall.tex", f"{m} hi apareix {n} cops (ha de ser exactament 1)")


def valida_preambul(preambul: str, on: str) -> None:
    for m in MARCADORS:
        if m in preambul:
            error(on, f"conté el marcador reservat {m}")


def cos_amb_capcalera(tex: str, etiqueta: str, procedencia: str | None = None) -> str:
    """Capçalera + (procedència PAU) + cos. app.js fa exactament el mateix."""
    cap = "\\encapcalament{%s}\n" % etiqueta
    if procedencia:
        cap += "\\procedencia{%s}\n" % procedencia
    return cap + tex.strip()


# ── validació ──────────────────────────────────────────────────────────
RE_APARTAT = re.compile(r"\\apartat(?:\[([^\]]*)\])?\{([^}]*)\}")
RE_NOMESLLARG = re.compile(r"\\(begin|end)\{nomesllarg\}")


def centesimes(brut: str, on: str, com: str) -> int | None:
    """«1,25» → 125. Els punts es compten en centèsimes per no arrossegar decimals."""
    try:
        valor = round(float(brut.strip().replace(",", ".")) * 100)
    except ValueError:
        error(on, f"{com} no és un nombre")
        return None
    if valor % GRA:
        error(on, f"{com} no és múltiple de 0,25")
    return valor


def trams_nomesllarg(tex: str, on: str) -> list[tuple[int, int]]:
    """Posicions [inici, final) del contingut de cada bloc nomesllarg."""
    trams: list[tuple[int, int]] = []
    obert = None
    for m in RE_NOMESLLARG.finditer(tex):
        if m.group(1) == "begin":
            if obert is not None:
                error(on, "hi ha un nomesllarg dins d'un altre")
            obert = m.end()
        elif obert is None:
            error(on, r"\end{nomesllarg} sense \begin{nomesllarg}")
        else:
            trams.append((obert, m.start()))
            obert = None
    if obert is not None:
        error(on, r"\begin{nomesllarg} sense tancar")
    return trams


def punts_del_tex(tex: str, on: str) -> tuple[list[int], list[int], bool]:
    """Llegeix els \\apartat[50 min]{1 h 30}. La puntuació viu al .tex i enlloc
    més. Torna els punts de l'examen d'1 h 30, els de l'examen de 50 min (sense
    els apartats de nomesllarg) i si la versió de 50 min és diferent."""
    trams = trams_nomesllarg(tex, on)
    llarg: list[int] = []
    curt: list[int] = []
    diferent = bool(trams)
    for m in RE_APARTAT.finditer(tex):
        opcional, brut = m.group(1), m.group(2)
        valor = centesimes(brut, on, f"\\apartat{{{brut}}}")
        if valor is None:
            continue
        llarg.append(valor)
        if any(a <= m.start() < b for a, b in trams):
            if opcional is not None:
                error(on, "un apartat de nomesllarg no surt a l'examen de 50 min: "
                          "no hi pot dur puntuació entre claudàtors")
            continue
        if opcional is None:
            curt.append(valor)
        else:
            diferent = True
            v = centesimes(opcional, on, f"\\apartat[{opcional}]")
            if v is not None:
                curt.append(v)
    if not llarg:
        error(on, "no hi ha cap \\apartat{...}")
    elif sum(llarg) != PUNTS_PREGUNTA:
        error(on, f"els apartats sumen {sum(llarg)/100:.2f} i han de sumar 2,50")
    if diferent and llarg:
        if not curt:
            error(on, "a l'examen de 50 min no hi queda cap apartat")
        elif sum(curt) != PUNTS_PREGUNTA:
            error(on, f"a l'examen de 50 min, els apartats sumen {sum(curt)/100:.2f} "
                      "i han de sumar 2,50")
    return llarg, curt, diferent


RE_APARTAT_OPCIONAL = re.compile(r"\\apartat\[([^\]]*)\]\{([^}]*)\}")


def materialitza(tex: str, curt: bool) -> str:
    """La versió d'una pregunta per a una modalitat, neta: sense cap marca de
    l'altra. A 50 min, fora els blocs nomesllarg i \\apartat[x]{y} → \\apartat{x};
    a 1 h 30, fora només les línies del bloc i \\apartat[x]{y} → \\apartat{y}.
    materialitza() d'app.js fa EXACTAMENT el mateix."""
    sortida: list[str] = []
    dins = False
    for linia in tex.split("\n"):
        net = linia.strip()
        if net == r"\begin{nomesllarg}":
            dins = True
            continue
        if net == r"\end{nomesllarg}":
            dins = False
            continue
        if dins and curt:
            continue
        sortida.append(linia)
    net = RE_APARTAT_OPCIONAL.sub(
        lambda m: "\\apartat{" + (m.group(1) if curt else m.group(2)) + "}", "\n".join(sortida))
    return re.sub(r"\n{3,}", "\n\n", net)


def valida_tex(tex: str, on: str) -> None:
    for prohibit in (r"\documentclass", r"\usepackage", r"\begin{document}"):
        if prohibit in tex:
            error(on, f"conté {prohibit}; una pregunta és només el cos")
    obre = len(re.findall(r"\\begin\{solucio\}", tex))
    tanca = len(re.findall(r"\\end\{solucio\}", tex))
    if obre != tanca:
        error(on, f"{obre} \\begin{{solucio}} i {tanca} \\end{{solucio}}")
    # El paquet comment exigeix que aquestes línies no portin res més.
    for ordre in (r"\end{solucio}", r"\begin{nomesllarg}", r"\end{nomesllarg}"):
        for linia in tex.splitlines():
            if ordre in linia and linia.strip() != ordre:
                error(on, f"{ordre} ha d'anar sol a la seva línia")
    if obre == 0:
        avis(on, "no té solució")
    if r"\procedencia" in tex:
        error(on, "conté \\procedencia; la línia PAU la posa el build a partir del codi")
    # TikZ fa els passos del grid en cm absoluts (step=1cm per defecte). Si la
    # figura té x= o y= diferents d'1 cm, la graella queda desquadrada respecte
    # dels enters i l'alumne llegeix valors falsos. Exigim step explícit.
    for ordre in re.findall(r"\\draw(?:\[[^\]]*\])?[^;]*?\bgrid\b[^;]*;", tex):
        if "step=" not in ordre:
            error(on, "grid sense step= explícit (la graella quedaria desquadrada)")


def valida_meta(meta: dict, on: str, slugs: set[str], esquema: dict = CLAUS_META,
                unitats_valides: set[str] = frozenset()) -> None:
    for clau, tipus in esquema.items():
        if clau not in meta:
            error(on, f"falta la clau «{clau}» a meta.json")
        elif not isinstance(meta[clau], tipus):
            error(on, f"«{clau}» hauria de ser {tipus.__name__}")
    for extra in set(meta) - set(esquema) - set(OPCIONALS_META):
        error(on, f"clau desconeguda a meta.json: «{extra}»")
    for clau, tipus in OPCIONALS_META.items():
        if clau in meta and not isinstance(meta[clau], tipus):
            error(on, f"«{clau}» hauria de ser {tipus.__name__}")
    if meta.get("dificultat") not in DIFICULTATS:
        error(on, "«dificultat» ha de ser ●○○, ●●○ o ●●●")
    if esquema is CLAUS_META_PAU:
        for u in meta.get("unitats", []):
            if u not in unitats_valides:
                error(on, f"unitat inexistent a «unitats»: «{u}»")
        if meta.get("unitats") == []:
            avis(on, "«unitats» és buida: la targeta no podrà dir fins on cal haver arribat")
    for t in meta.get("temes_secundaris", []):
        if t not in slugs:
            error(on, f"tema secundari inexistent: «{t}»")


# ── compilació ─────────────────────────────────────────────────────────
def compila(document: str, desti: Path, on: str) -> int | None:
    """Compila un .tex complet i desa el PDF a `desti`. Retorna les pàgines."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "main.tex").write_text(document, encoding="utf-8")
        # Sense text=True: pdflatex escriu els caràcters accentuats en la
        # codificació de la font (T1), no en UTF-8. Descodifiquem tolerant.
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            cwd=tmp, capture_output=True)
        sortida = r.stdout.decode("utf-8", errors="replace")
        log = (tmp / "main.log").read_text(encoding="utf-8", errors="replace") \
            if (tmp / "main.log").exists() else sortida
        if r.returncode != 0 or not (tmp / "main.pdf").exists():
            primera = next((l for l in log.splitlines() if l.startswith("! ")), "error desconegut")
            error(on, f"no compila → {primera}")
            return None
        for l in log.splitlines():
            if l.startswith("Overfull") or l.startswith("Underfull"):
                avis(on, l.strip()[:90])
        desti.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(tmp / "main.pdf", desti)
        m = re.search(r"main\.pdf \((\d+) pages?", log)
        return int(m.group(1)) if m else None


# ── programa ───────────────────────────────────────────────────────────
def construeix(provisional: Path) -> int:
    """Valida, compila els PDF dins de `provisional` i, només si no hi ha
    cap error, els copia a out/ i escriu el catàleg."""
    p = argparse.ArgumentParser()
    p.add_argument("--nomes-cataleg", action="store_true")
    p.add_argument("--headers", default=None, metavar="FITXER")
    p.add_argument("--pregunta", default=None, metavar="RUTA")
    args = p.parse_args()

    temes_doc = json.loads((ARREL / "temes.json").read_text(encoding="utf-8"))
    slugs = {t["slug"] for t in temes_doc["temes"]}
    unitats = set(temes_doc["unitats"])
    for t in temes_doc["temes"]:
        if t["unitat"] not in unitats:
            error("temes.json", f"«{t['slug']}» apunta a una unitat inexistent")
    llista_slugs = [t["slug"] for t in temes_doc["temes"]]
    for sl in sorted({x for x in llista_slugs if llista_slugs.count(x) > 1}):
        error("temes.json", f"slug duplicat: «{sl}» (l'adreça del lloc en depèn)")
    tema_unitat = {t["slug"]: t["unitat"] for t in temes_doc["temes"]}

    convocatories = {}
    fitxer_conv = ARREL / "pau" / "convocatories.json"
    if fitxer_conv.exists():
        try:
            convocatories = {k: v for k, v in json.loads(fitxer_conv.read_text(encoding="utf-8")).items()
                             if not k.startswith("_")}
        except json.JSONDecodeError as e:
            error("pau/convocatories.json", f"no és JSON vàlid ({e})")
        for k, c in convocatories.items():
            on_c = f"pau/convocatories.json «{k}»"
            if not (isinstance(c.get("any"), int) and isinstance(c.get("serie"), int)):
                error(on_c, "«any» i «serie» han de ser enters")
            if c.get("mes") not in MESOS:
                error(on_c, f"«mes» ha de ser un de {sorted(MESOS)}")
            if not str(c.get("font", "")).strip():
                error(on_c, "cal «font»: una sèrie sense font no s'imprimeix en un examen")

    plantilla = (ARREL / "build" / "embolcall.tex").read_text(encoding="utf-8")
    valida_plantilla(plantilla)
    # El format viu en dos fitxers: headers.tex (paquets) i defs.tex (macros).
    # El catàleg porta SEMPRE els oficials, perquè són els que el lloc posa als
    # .tex que es baixen. --headers només canvia amb què es compila aquí.
    headers = (ARREL / "build" / "headers.tex").read_text(encoding="utf-8")
    defs = (ARREL / "build" / "defs.tex").read_text(encoding="utf-8")
    valida_preambul(headers, "headers.tex")
    valida_preambul(defs, "defs.tex")
    # Segell: identifica aquesta versió del format. El .tex d'un examen el
    # comprova, i així un defs.tex vell no passa desapercebut.
    versio = hashlib.sha256((headers + defs).encode("utf-8")).hexdigest()[:8]
    defs += f"\n\\def\\bancversio{{{versio}}}\n"
    preambul = headers + "\n" + defs
    preambul_compila = preambul
    if args.headers:
        altres = Path(args.headers).read_text(encoding="utf-8")
        valida_preambul(altres, args.headers)
        preambul_compila = altres + "\n" + defs
        if altres != headers and not args.nomes_cataleg:
            avis(args.headers, "els PDF s'han compilat amb aquests paquets i no amb els oficials: "
                 "no són definitius (el catàleg sí que porta els oficials)")

    # El catàleg SEMPRE inclou totes les preguntes. --pregunta només limita
    # quines es compilen; si filtrés el catàleg, en deixaria un de mutilat.
    carpetes = sorted(m.parent for m in ARREL.glob("*/*/*/meta.json")
                      if m.parts[-4] in unitats or re.fullmatch(r"u\d+|pau", m.parts[-4]))

    preguntes = []
    vistos: set[str] = set()

    for dir_q in carpetes:
        unitat, tema, codi = dir_q.parts[-3:]
        ident = f"{unitat}/{tema}/{codi}"
        on = ident

        if unitat not in unitats:
            error(on, f"la unitat «{unitat}» no és a temes.json")
            continue
        if tema not in slugs:
            error(on, f"el tema «{tema}» no és a temes.json")
            continue
        if tema_unitat[tema] != unitat:
            error(on, f"el tema «{tema}» pertany a «{tema_unitat[tema]}», no a «{unitat}»")
            continue
        es_pau = unitat == "pau"
        procedencia = None
        if es_pau:
            mt = CODI_PAU.match(codi)
            if not mt:
                error(on, "codi PAU mal format: ha de ser com ana-26j-q1 (bloc-convocatòria-exercici)")
                continue
            if BLOCS_PAU[mt.group(1)] != tema:
                error(on, f"el prefix «{mt.group(1)}» no correspon al bloc «{tema}»")
                continue
            conv = convocatories.get(mt.group(2))
            if conv is None:
                error(on, f"la convocatòria «{mt.group(2)}» no és a pau/convocatories.json")
                continue
            procedencia = f"PAU {conv['mes']} {conv['any']}, sèrie {conv['serie']}"
        elif not CODI_BANC.match(codi):
            error(on, "codi mal format: ha de ser q001, q002…")
            continue
        if ident in vistos:
            error(on, "identificador repetit")
            continue
        vistos.add(ident)

        try:
            meta = json.loads((dir_q / "meta.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            error(on, f"meta.json no és JSON vàlid ({e})")
            continue
        valida_meta(meta, on, slugs, CLAUS_META_PAU if es_pau else CLAUS_META,
                    {u for u in unitats if u != "pau"})

        if not (dir_q / "pregunta.tex").exists():
            error(on, "falta pregunta.tex")
            continue
        tex = (dir_q / "pregunta.tex").read_text(encoding="utf-8")
        valida_tex(tex, on)
        for m in MARCADORS:
            if m in tex:
                error(on, f"conté el marcador reservat {m}")
        apartats, apartats_curt, te_curt = punts_del_tex(tex, on)
        if te_curt and "minuts_curt" not in meta:
            error(on, "té versió de 50 min: falta «minuts_curt» a meta.json")
        if not te_curt and "minuts_curt" in meta:
            error(on, "«minuts_curt» sense versió de 50 min (cap \\apartat[..] ni nomesllarg)")
        if isinstance(meta.get("minuts_curt"), int) and isinstance(meta.get("minuts"), int) \
                and meta["minuts_curt"] > meta["minuts"]:
            error(on, "«minuts_curt» no pot ser més gran que «minuts»")

        compilar = not args.nomes_cataleg and (args.pregunta is None or args.pregunta in ident)
        if compilar:
            # Els PDF van a la carpeta provisional, amb la mateixa estructura que
            # el banc. Només es copien a out/ al final, si no hi ha cap error.
            cos = cos_amb_capcalera(materialitza(tex, False), "Pregunta", procedencia)
            pagines = compila(munta(plantilla, preambul_compila, [cos], False),
                              provisional / ident / "out" / "enunciat.pdf", on)
            compila(munta(plantilla, preambul_compila, [cos], True),
                    provisional / ident / "out" / "solucio.pdf", on)
            if pagines and pagines > 1:
                avis(on, f"l'enunciat ocupa {pagines} pàgines")
            if te_curt:
                cos_curt = cos_amb_capcalera(materialitza(tex, True), "Pregunta", procedencia)
                pagines_curt = compila(munta(plantilla, preambul_compila, [cos_curt], False),
                                       provisional / ident / "out" / "enunciat-curt.pdf", on)
                compila(munta(plantilla, preambul_compila, [cos_curt], True),
                        provisional / ident / "out" / "solucio-curt.pdf", on)
                if pagines_curt and pagines_curt > 1:
                    avis(on, f"l'enunciat de 50 min ocupa {pagines_curt} pàgines")
            estat = "✓" if not any(e.startswith(on + ":") for e in errors) else "✗"
            print(f"  {estat} {ident:<40} {' + '.join(f'{a/100:.2f}' for a in apartats):<22}"
                  f" {pagines or '?'} pàg."
                  + (f"  · 50 min: {' + '.join(f'{a/100:.2f}' for a in apartats_curt)}" if te_curt else ""))

        preguntes.append({
            "id": ident, "unitat": unitat, "tema": tema, "codi": codi,
            "titol": meta.get("titol", ""),
            "punts": sum(apartats) / 100,
            "apartats": [a / 100 for a in apartats],
            "apartats_curt": [a / 100 for a in apartats_curt],
            "te_curt": te_curt,
            "dificultat": meta.get("dificultat", ""),
            "origen": meta.get("origen", []),
            "minuts": meta.get("minuts", 0),
            "minuts_curt": meta.get("minuts_curt", meta.get("minuts", 0)),
            "etiquetes": meta.get("etiquetes", []),
            "temes_secundaris": meta.get("temes_secundaris", []),
            "procedencia": procedencia,
            "unitats": meta.get("unitats", []),
            "tex": tex,
            "pdf": f"{ident}/out/enunciat.pdf",
            "pdf_solucio": f"{ident}/out/solucio.pdf",
            # Sense versió de 50 min, a l'examen de 50 min hi va la pregunta sencera.
            "pdf_curt": f"{ident}/out/{'enunciat-curt' if te_curt else 'enunciat'}.pdf",
            "pdf_solucio_curt": f"{ident}/out/{'solucio-curt' if te_curt else 'solucio'}.pdf",
        })

    for a in avisos:
        print(f"  avís  {a}")
    if errors:
        print(f"\n✗ {len(errors)} error(s). No s'ha escrit res.\n", file=sys.stderr)
        for e in errors:
            print(f"  ERROR {e}", file=sys.stderr)
        return 1

    # Cap error: ara, i només ara, es publiquen els PDF compilats.
    pdfs = sorted(provisional.rglob("*.pdf"))
    for pdf in pdfs:
        desti = ARREL / pdf.relative_to(provisional)
        desti.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pdf, desti)

    banc = {
        "generat": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "unitats": temes_doc["unitats"],
        "temes": temes_doc["temes"],
        "plantilla": plantilla,
        "preambul": preambul,
        "headers": headers,
        "defs": defs,
        "main": (ARREL / "build" / "main.tex").read_text(encoding="utf-8"),
        "versio": versio,
        "preguntes": preguntes,
    }
    sortida = ("/* FITXER GENERAT PER build/build.py — NO L'EDITIS MAI */\n"
               "const BANC = " + json.dumps(banc, ensure_ascii=False, indent=1) + ";\n")
    (ARREL / "cataleg.js").write_text(sortida, encoding="utf-8")

    minuts = sum(q["minuts"] for q in preguntes)
    n = len(preguntes)
    print(f"\n✓ {n} {'pregunta' if n == 1 else 'preguntes'} · {len(slugs)} temes · "
          f"{minuts} min de banc · {len(pdfs)} PDF desats · cataleg.js {len(sortida)//1024} kB")
    return 0


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="banc-") as tmp:
        return construeix(Path(tmp))


if __name__ == "__main__":
    sys.exit(main())
