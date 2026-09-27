#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════
#  prova_validacio.py — comprova que build.py REBUTJA cada tipus d'error
#  ─────────────────────────────────────────────────────────────────────
#  Copia el banc a una carpeta temporal, hi injecta una sola avaria cada
#  vegada i exigeix que el build falli amb el missatge esperat. Si algun
#  dia una regla deixa de funcionar, aquesta prova ho detecta.
#
#  Ús:   python3 build/prova_validacio.py
# ═══════════════════════════════════════════════════════════════════════

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
Q = "u7/continuitat-trossos/q001"


def tex(r):  return r / Q / "pregunta.tex"
def meta(r): return r / Q / "meta.json"


def edita_tex(vell, nou):
    def f(r):
        s = tex(r).read_text(encoding="utf-8")
        assert vell in s, f"la prova no troba «{vell}»"
        tex(r).write_text(s.replace(vell, nou, 1), encoding="utf-8")
    return f


def edita_meta(canvi):
    def f(r):
        m = json.loads(meta(r).read_text(encoding="utf-8"))
        canvi(m)
        meta(r).write_text(json.dumps(m, ensure_ascii=False), encoding="utf-8")
    return f


QP = "pau/analisi/ana-26j-q1"
QM = "u7/limits-punt/q001"      # té versió de 50 min


def mou(de, a):
    def f(r):
        (r / a).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(r / de), str(r / a))
    return f


def edita_text(ruta, vell, nou):
    def f(r):
        t = (r / ruta).read_text(encoding="utf-8")
        assert vell in t, f"la prova no troba «{vell}» a {ruta}"
        (r / ruta).write_text(t.replace(vell, nou, 1), encoding="utf-8")
    return f


def edita_json(ruta, canvi):
    def f(r):
        d = json.loads((r / ruta).read_text(encoding="utf-8"))
        canvi(d)
        (r / ruta).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return f


AVARIES = [
    ("apartats que sumen 2,25",
     edita_tex(r"\apartat{0,75}", r"\apartat{0,5}"), "han de sumar 2,50"),
    ("apartat que no és múltiple de 0,25",
     edita_tex(r"\apartat{0,75}", r"\apartat{0,7}"), "múltiple de 0,25"),
    ("\\end{solucio} enganxat a text",
     edita_tex("\\end{solucio}", "fi. \\end{solucio}"), "sol a la seva línia"),
    ("\\usepackage dins d'una pregunta",
     edita_tex(r"\begin{apartats}", "\\usepackage{xcolor}\n\\begin{apartats}"), "només el cos"),
    ("marcador reservat dins d'una pregunta",
     edita_tex(r"\begin{apartats}", "%%COS%%\n\\begin{apartats}"), "marcador reservat"),
    ("tema secundari inexistent",
     edita_meta(lambda m: m.update(temes_secundaris=["no-existeix"])), "inexistent"),
    ("clau desconeguda a meta.json",
     edita_meta(lambda m: m.update(puntuacio=2.5)), "clau desconeguda"),
    ("dificultat mal escrita",
     edita_meta(lambda m: m.update(dificultat="alta")), "dificultat"),
    ("clau obligatòria absent",
     edita_meta(lambda m: m.pop("titol")), "falta la clau"),
    ("graella de TikZ sense step explícit",
     edita_tex(r"\begin{apartats}", "\\begin{tikzpicture}[x=0.9cm]\\draw[gray] (0,0) grid (3,3);\\end{tikzpicture}\n\\begin{apartats}"),
     "grid sense step"),
    # ── preguntes PAU ──
    ("codi PAU mal format",
     mou(QP, "pau/analisi/ana-2026-q1"), "codi PAU mal format"),
    ("convocatòria PAU inexistent",
     mou(QP, "pau/analisi/ana-27j-q1"), "no és a pau/convocatories.json"),
    ("prefix de bloc que no correspon a la carpeta",
     mou(QP, "pau/algebra/ana-26j-q1"), "no correspon al bloc"),
    ("unitat inexistent als requisits d'una PAU",
     edita_json(f"{QP}/meta.json", lambda m: m.update(unitats=["u99"])), "unitat inexistent"),
    ("clau del banc dins d'una PAU (origen)",
     edita_json(f"{QP}/meta.json", lambda m: m.update(origen=[44])), "clau desconeguda"),
    ("procedència escrita a mà",
     edita_text(f"{QP}/pregunta.tex", "Considereu", "\\procedencia{PAU juny 2026, sèrie 1}\nConsidereu"),
     "la línia PAU la posa el build"),
    ("convocatòria sense font",
     edita_json("pau/convocatories.json", lambda d: d["26j"].pop("font")), "cal «font»"),
    ("sèrie que no és un enter",
     edita_json("pau/convocatories.json", lambda d: d["26j"].update(serie="1")), "han de ser enters"),
    # ── taxonomia ──
    ("slug duplicat a temes.json",
     edita_json("temes.json", lambda d: d["temes"].append(dict(d["temes"][0]))), "slug duplicat"),
    ("tema d'una unitat desat en una altra",
     mou("u7/limits-punt/q001", "pau/limits-punt/q001"), "pertany a «u7»"),
    ("meta.json que no és JSON",
     lambda r: meta(r).write_text("{ titol: sense cometes }", encoding="utf-8"), "JSON vàlid"),
    # ── modalitats: la pregunta pilot és la primera amb versió de 50 min ──
    ("punts de 50 min que no sumen 2,50",
     edita_text(f"{QM}/pregunta.tex", r"\apartat[1,25]{1}", r"\apartat[1]{1}"),
     "a l'examen de 50 min, els apartats sumen"),
    ("puntuació de 50 min dins de nomesllarg",
     edita_text(f"{QM}/pregunta.tex", "\\begin{nomesllarg}\n\\apartat{0,75}",
                "\\begin{nomesllarg}\n\\apartat[0,75]{0,75}"), "no hi pot dur puntuació"),
    ("\\end{nomesllarg} enganxat a text",
     edita_text(f"{QM}/pregunta.tex", "\\end{nomesllarg}", "Fi. \\end{nomesllarg}"),
     "\\end{nomesllarg} ha d'anar sol"),
    ("nomesllarg sense tancar",
     edita_text(f"{QM}/pregunta.tex", "\\end{nomesllarg}\n", ""), "sense tancar"),
    ("versió de 50 min sense minuts_curt",
     edita_json(f"{QM}/meta.json", lambda m: m.pop("minuts_curt")), "falta «minuts_curt»"),
    ("minuts_curt més gran que minuts",
     edita_json(f"{QM}/meta.json", lambda m: m.update(minuts_curt=99)), "no pot ser més gran"),
    ("minuts_curt sense versió de 50 min",
     edita_json(f"{QP}/meta.json", lambda m: m.update(minuts_curt=5)), "sense versió de 50 min"),
    ("\\begin{nomesllarg} amb text a la mateixa línia",
     edita_text(f"{QM}/pregunta.tex", "\\begin{nomesllarg}\n", "\\begin{nomesllarg} Opcional.\n"),
     "\\begin{nomesllarg} ha d'anar sol"),
]


def main() -> int:
    fallades = 0
    for nom, avaria, esperat in AVARIES:
        with tempfile.TemporaryDirectory() as tmp:
            copia = Path(tmp) / "banc"
            shutil.copytree(ARREL, copia, ignore=shutil.ignore_patterns(".git", "*.pdf"))
            avaria(copia)
            r = subprocess.run([sys.executable, str(copia / "build" / "build.py"), "--nomes-cataleg"],
                               capture_output=True, text=True)
            ok = r.returncode == 1 and esperat in r.stderr
            fallades += not ok
            print(f"  {'✓' if ok else '✗'} {nom}")
            if not ok:
                print(f"      esperava codi 1 amb «{esperat}»; ha tornat {r.returncode}\n{r.stderr}")
    print(f"\n{'✓ Totes les regles es compleixen.' if not fallades else f'✗ {fallades} regla(es) no funcionen.'}")
    return 1 if fallades else 0


if __name__ == "__main__":
    sys.exit(main())
