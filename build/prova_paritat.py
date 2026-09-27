#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════
#  prova_paritat.py — el .tex que baixa el lloc web ha de ser IDÈNTIC,
#  byte a byte, al que munta build.py per a la mateixa selecció.
#  ─────────────────────────────────────────────────────────────────────
#  Executa els fitxers reals cataleg.js + assets/app.js dins de Node amb
#  un DOM mínim, simula una adreça amb quatre temes i compara el resultat
#  amb munta() de build.py. També comprova el recompte de punts, que
#  una adreça amb codis inexistents no trenca la pàgina, i els exàmens
#  amb opcions (1, 2, 3, 4a, 4b): etiquetes, punts i accions.
#
#  Ús:   python3 build/prova_paritat.py      (cal node i cataleg.js)
# ═══════════════════════════════════════════════════════════════════════

import json
import re
import subprocess
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ARREL / "build"))
from build import munta, cos_amb_capcalera, materialitza  # noqa: E402

HARNES = r"""
const fs = require('fs'), vm = require('vm');
const [arrel, hash, accions] = process.argv.slice(1);
function el() {
  return { innerHTML:'', className:'', title:'', type:'', textContent:'', disabled:false,
    dataset:{}, style:{}, children:[], setAttribute(){}, appendChild(c){ this.children.push(c); return c; },
    remove(){}, click(){}, querySelectorAll(){ return []; } };
}
const nodes = {};
const ctx = vm.createContext({
  document: { querySelector: s => (nodes[s] ||= el()), createElement: el, body: el() },
  location: { hash, pathname: '/index.html', search: '' },
  history: { replaceState(_, __, u) { ctx.location.hash = String(u).split('#')[1] || ''; } },
  URL, Blob, setTimeout, console,
});
vm.runInContext(fs.readFileSync(arrel + '/cataleg.js', 'utf8'), ctx, { filename: 'cataleg.js' });
// Tema buit sintètic: la prova no pot dependre que el banc real en tingui cap.
vm.runInContext("BANC.temes.push({slug:'__buit__', unitat:'u7', nom:'Tema buit de prova', descripcio:''})", ctx);
vm.runInContext(fs.readFileSync(arrel + '/assets/app.js', 'utf8'), ctx, { filename: 'app.js' });
if (accions) vm.runInContext(accions, ctx, { filename: 'accions.js' });
const r = vm.runInContext(`({
  ids: triades().map(q => q.id),
  etiquetes: etiquetes(),
  tex: munta(pecesExamen(), false),
  prova: pecesExamen().join('\\n\\n') + '\\n',
  sol: munta(pecesExamen(), true),
  recompte: document.querySelector('#recompte').innerHTML,
  hash: location.hash,
})`, ctx);
process.stdout.write(JSON.stringify(r));
"""


# El cos de l'examen comença a la LÍNIA \begin{document}. No n'hi ha prou de
# buscar-ne el text: el preàmbul el cita en un comentari, i s'hi tallaria abans.
INICI_COS = "\n\\begin{document}\n"


class AppPetada(Exception):
    """app.js ha llançat una excepció dins de Node: al navegador, pàgina en blanc."""


def web(hash_: str, accions: str = "") -> dict:
    """Obre el lloc amb l'adreça #hash_, hi executa `accions` (els mateixos
    clics que faria el professor, com a crides d'app.js) i en torna l'estat."""
    r = subprocess.run(["node", "-e", HARNES, str(ARREL), hash_, accions],
                       capture_output=True, text=True)
    if r.returncode:
        raise AppPetada(r.stderr.strip())
    return json.loads(r.stdout)


def main() -> int:
    banc = json.loads((ARREL / "cataleg.js").read_text(encoding="utf-8")
                      .split("const BANC = ", 1)[1].rstrip().rstrip(";"))

    def peces(cossos):
        """Les peces d'un examen, en el mateix ordre que les munta el lloc."""
        return [f"\\bancrequereix{{{banc['versio']}}}", "\\capsaleraexamen", *cossos]
    per_id = {q["id"]: q for q in banc["preguntes"]}
    fallades = 0

    def comprova(nom, cond, detall=""):
        nonlocal fallades
        fallades += not cond
        print(f"  {'✓' if cond else '✗'} {nom}" + (f"\n      {detall}" if not cond and detall else ""))

    # 1. Paritat amb quatre temes (un d'ells buit, que no ha de comptar)
    hash_ = "limits-grafica:q001,__buit__,continuitat-trossos:q001,bolzano-biseccio:q001,limits-punt:q001"
    r = web(hash_)
    esperat = ["u7/limits-grafica/q001", "u7/continuitat-trossos/q001",
               "u7/bolzano-biseccio/q001", "u7/limits-punt/q001"]
    comprova("el tema buit no entra a l'examen", r["ids"] == esperat, r["ids"])
    cossos = [cos_amb_capcalera(materialitza(per_id[i]["tex"], False), f"Q{n}", per_id[i]["procedencia"]) for n, i in enumerate(esperat, 1)]
    for sol, clau in ((False, "tex"), (True, "sol")):
        py = munta(banc["plantilla"], banc["preambul"], peces(cossos), sol)
        igual = py == r[clau]
        detall = "" if igual else next(
            (f"primera diferència al caràcter {k}" for k, (a, b) in enumerate(zip(py, r[clau])) if a != b),
            f"longituds {len(py)} i {len(r[clau])}")
        comprova(f"paritat JS = Python ({'amb' if sol else 'sense'} solucions, {len(py)} caràcters)", igual, detall)
    comprova("el recompte diu 10,00 punts", "10,00 punts" in r["recompte"], r["recompte"])

    # 1b. Paritat amb segones variants i els temes nous
    hash_ = "limits-grafica:q002,parametres-ab:q001,bolzano-biseccio:q002,limits-infinit:q001"
    r = web(hash_)
    esperat = ["u7/limits-grafica/q002", "u7/parametres-ab/q001",
               "u7/bolzano-biseccio/q002", "u7/limits-infinit/q001"]
    comprova("les variants q002 es trien per codi", r["ids"] == esperat, r["ids"])
    cossos = [cos_amb_capcalera(materialitza(per_id[i]["tex"], False), f"Q{n}", per_id[i]["procedencia"]) for n, i in enumerate(esperat, 1)]
    py = munta(banc["plantilla"], banc["preambul"], peces(cossos), True)
    comprova(f"paritat JS = Python amb variants ({len(py)} caràcters)", py == r["sol"])
    comprova("el recompte torna a dir 10,00 punts", "10,00 punts" in r["recompte"], r["recompte"])

    # 1c. Un examen PAU sencer (juny 2026): paritat i línia de procedència
    hash_ = "analisi:ana-26j-q1,algebra:alg-26j-q2,probabilitat:pro-26j-q3,geometria:geo-26j-q4b"
    r = web(hash_)
    esperat = ["pau/analisi/ana-26j-q1", "pau/algebra/alg-26j-q2",
               "pau/probabilitat/pro-26j-q3", "pau/geometria/geo-26j-q4b"]
    comprova("un examen PAU sencer es tria per codi", r["ids"] == esperat, r["ids"])
    cossos = [cos_amb_capcalera(materialitza(per_id[i]["tex"], False), f"Q{n}", per_id[i]["procedencia"])
              for n, i in enumerate(esperat, 1)]
    py = munta(banc["plantilla"], banc["preambul"], peces(cossos), False)
    comprova(f"paritat JS = Python amb preguntes PAU ({len(py)} caràcters)", py == r["tex"])
    linies = r["tex"].splitlines()
    ok = all(linies[linies.index(f"\\encapcalament{{Q{n}}}") + 1]
             == "\\procedencia{PAU juny 2026, sèrie 1}" for n in range(1, 5))
    comprova("cada pregunta PAU comença amb «PAU juny 2026, sèrie 1»", ok)
    comprova("el recompte de l'examen PAU diu 10,00 punts", "10,00 punts" in r["recompte"], r["recompte"])
    r = web("analisi:ana-26j-q4a")
    comprova("l'opció 4A es tria com a variant del bloc d'anàlisi", r["ids"] == ["pau/analisi/ana-26j-q4a"], r["ids"])
    r = web("limits-punt:q001")
    comprova("una pregunta del banc no porta cap línia de procedència", "\\procedencia{" not in
             r["tex"].split(INICI_COS, 1)[1], "")

    # 1d. Un examen com el de la PAU: 1, 2, 3, 4a i 4b, amb dues preguntes d'anàlisi
    def cossos(ids, etiquetes, curt=False):
        return [cos_amb_capcalera(materialitza(per_id[i]["tex"], curt), f"Q{e}",
                                  per_id[i]["procedencia"])
                for i, e in zip(ids, etiquetes)]

    pau = "analisi:ana-26j-q1,algebra:alg-26j-q2,probabilitat:pro-26j-q3,analisi:ana-26j-q4a|geometria:geo-26j-q4b"
    ana1, alg2, pro3, ana4a, geo4b = ("pau/analisi/ana-26j-q1", "pau/algebra/alg-26j-q2",
                                      "pau/probabilitat/pro-26j-q3", "pau/analisi/ana-26j-q4a",
                                      "pau/geometria/geo-26j-q4b")
    r = web(pau)
    comprova("un tema pot sortir dues vegades (la 1 i la 4a són d'anàlisi)",
             r["ids"] == [ana1, alg2, pro3, ana4a, geo4b], r["ids"])
    comprova("les etiquetes són 1, 2, 3, 4a i 4b", r["etiquetes"] == ["1", "2", "3", "4a", "4b"], r["etiquetes"])
    for sol, clau in ((False, "tex"), (True, "sol")):
        py = munta(banc["plantilla"], banc["preambul"], peces(cossos(r["ids"], r["etiquetes"])), sol)
        comprova(f"paritat JS = Python amb opcions ({'amb' if sol else 'sense'} solucions, {len(py)} caràcters)",
                 py == r[clau])
    comprova("el .tex diu «Q4a» i «Q4b»",
             "\\encapcalament{Q4a}" in r["tex"] and "\\encapcalament{Q4b}" in r["tex"])
    comprova("les opcions compten una vegada: 5 preguntes, se'n responen 4, 10,00 punts",
             all(s in r["recompte"] for s in ("5 preguntes", "se'n responen 4", "10,00 punts")), r["recompte"])
    comprova("l'adreça conserva les opcions", r["hash"] == pau, r["hash"])

    # 1e. Les accions de les targetes, com les faria el professor
    cinc = pau.replace("|", ",")
    r = web(cinc)
    comprova("una adreça amb cinc preguntes separades per comes les manté separades: 1…5",
             r["etiquetes"] == ["1", "2", "3", "4", "5"] and "12,50 punts" in r["recompte"], r["etiquetes"])
    r = web(cinc, "commutaOpcio(4)")
    comprova("«Opció de l'anterior» a la cinquena → 4a i 4b",
             r["etiquetes"] == ["1", "2", "3", "4a", "4b"] and r["hash"] == pau, r["hash"])
    r = web(pau, "mou(4, -1)")
    comprova("▲ a la 4b la porta a la 4a, i l'estructura es manté",
             r["ids"][3:] == [geo4b, ana4a] and r["etiquetes"] == ["1", "2", "3", "4a", "4b"], r["ids"])
    r = web(pau, "treu(3)")
    comprova("✕ a la 4a: la 4b passa a ser la 4 i surten 10,00 punts",
             r["ids"] == [ana1, alg2, pro3, geo4b] and r["etiquetes"] == ["1", "2", "3", "4"]
             and "se'n responen" not in r["recompte"] and "10,00 punts" in r["recompte"], r["recompte"])
    r = web("", "afegeix('limits-punt'); " * 4)
    comprova("cada clic a un tema n'afegeix una pregunta diferent, fins que s'esgoten",
             r["ids"] == [f"u7/limits-punt/q00{n}" for n in (1, 2, 3)], r["ids"])
    r = web("limits-punt:q001,limits-punt:q002,limits-punt:q003", "rota(0, 1)")
    comprova("◀ ▶ no hi posa una pregunta que ja és a l'examen",
             r["ids"] == [f"u7/limits-punt/q00{n}" for n in (1, 2, 3)], r["ids"])
    r = web("limits-punt:q001", "rota(0, 1)")
    comprova("◀ ▶ passa a la variant següent si és lliure", r["ids"] == ["u7/limits-punt/q002"], r["ids"])

    # 1f. Per defecte, l'estructura és la de la PAU (1, 2, 3, 4a, 4b), també amb
    #     preguntes dels temes, i es poden combinar temes i PAU en un mateix examen.
    cinc_clics = ("afegeix('limits-punt'); afegeix('analisi'); afegeix('bolzano-biseccio'); "
                  "afegeix('probabilitat'); afegeix('geometria')")
    combinat = ["u7/limits-punt/q001", "pau/analisi/ana-26j-q1", "u7/bolzano-biseccio/q001",
                "pau/probabilitat/pro-26j-q3", "pau/geometria/geo-26j-q4b"]
    pau5 = ["1", "2", "3", "4a", "4b"]
    r = web("", cinc_clics)
    comprova("per defecte, cinc clics donen 1, 2, 3, 4a i 4b", r["etiquetes"] == pau5, r["etiquetes"])
    comprova("i l'examen fa 10,00 punts: se'n responen 4",
             all(s in r["recompte"] for s in ("5 preguntes", "se'n responen 4", "10,00 punts")), r["recompte"])
    comprova("es poden combinar preguntes dels temes i de la PAU", r["ids"] == combinat, r["ids"])
    for sol, clau in ((False, "tex"), (True, "sol")):
        py = munta(banc["plantilla"], banc["preambul"], peces(cossos(r["ids"], r["etiquetes"])), sol)
        comprova(f"paritat JS = Python en un examen combinat ({'amb' if sol else 'sense'} solucions)",
                 py == r[clau])
    comprova("només les tres preguntes PAU porten la línia de procedència",
             r["tex"].split(INICI_COS, 1)[1].count("\\procedencia{") == 3)
    comprova("l'adreça el desa amb la 4a i la 4b",
             r["hash"] == "limits-punt:q001,analisi:ana-26j-q1,bolzano-biseccio:q001,"
                          "probabilitat:pro-26j-q3|geometria:geo-26j-q4b", r["hash"])
    r = web("", cinc_clics + "; treu(1); afegeix('continuitat-trossos')")
    comprova("l'estructura és de les places: ✕ a la 2 i un clic nou tornen a fer 1, 2, 3, 4a, 4b",
             r["etiquetes"] == pau5 and r["ids"][-1] == "u7/continuitat-trossos/q001", r["ids"])
    r = web("", cinc_clics + "; treu(1); afegeix('continuitat-trossos'); mou(4, -1); mou(3, -1); mou(2, -1)")
    comprova("amb ▲, la pregunta nova passa a ser la 2 i la 4a i la 4b no es mouen",
             r["ids"][1] == "u7/continuitat-trossos/q001" and r["etiquetes"] == pau5
             and r["ids"][3:] == combinat[3:], r["ids"])
    r = web("", cinc_clics + "; commutaOpcio(4)")
    comprova("«Opció de l'anterior» a la 4b la separa: 1, 2, 3, 4 i 5",
             r["etiquetes"] == ["1", "2", "3", "4", "5"] and "12,50 punts" in r["recompte"], r["etiquetes"])
    r = web("limits-punt:q001,analisi:ana-26j-q1,bolzano-biseccio:q001,probabilitat:pro-26j-q3",
            "afegeix('geometria')")
    comprova("una adreça antiga de quatre preguntes, amb una cinquena, també fa 4a i 4b",
             r["etiquetes"] == pau5, r["etiquetes"])

    # 1g. La modalitat: examen d'1 h 30 (per defecte) o de 50 min
    r = web("limits-punt:q001")
    cos = r["sol"].split(INICI_COS, 1)[1]
    comprova("sense prefix, l'examen és d'1 h 30: tres apartats i cap marca de 50 min",
             cos.count("\\apartat{") == 3 and "\\apartat[" not in cos and "nomesllarg" not in cos
             and "Estudia si existeix" in cos and "de 90 min" in r["recompte"], r["recompte"])
    r = web("50min/limits-punt:q001")
    cos = r["sol"].split(INICI_COS, 1)[1]
    comprova("amb el prefix 50min/, el .tex ja és el de 50 min: dos apartats d'1,25 i res més",
             cos.count("\\apartat{1,25}") == 2 and cos.count("\\apartat{") == 2
             and "\\apartat[" not in cos and "nomesllarg" not in cos
             and "Estudia si existeix" not in cos, cos[:200])
    for sol, clau in ((False, "tex"), (True, "sol")):
        py = munta(banc["plantilla"], banc["preambul"], peces(cossos(r["ids"], r["etiquetes"], curt=True)), sol)
        comprova(f"paritat JS = Python a 50 min ({'amb' if sol else 'sense'} solucions)", py == r[clau])
    comprova("a 50 min compten els minuts de la versió de 50 min", "~11 de 50 min" in r["recompte"],
             r["recompte"])
    comprova("l'adreça conserva la modalitat", r["hash"] == "50min/limits-punt:q001", r["hash"])
    r = web("50min/analisi:ana-26j-q1")
    comprova("una pregunta sense versió de 50 min hi va sencera, amb els seus minuts",
             "~22 de 50 min" in r["recompte"], r["recompte"])
    r = web("limits-punt:q001", "curt = true; pinta()")
    comprova("en canviar a 50 min, l'adreça ho recull", r["hash"] == "50min/limits-punt:q001", r["hash"])
    r = web("50min/%")
    comprova("una adreça de 50 min mal formada no peta", r["ids"] == [], r["ids"])

    # 1h. El fitxer prova-N.tex: el cos de l'examen, per a la carpeta del professorat
    r = web("limits-punt:q001,bolzano-biseccio:q001")
    comprova("el prova-N.tex no porta preàmbul ni \\begin{document}",
             "\\documentclass" not in r["prova"] and "\\begin{document}" not in r["prova"],
             r["prova"][:80])
    comprova("comença pel segell de versió i per la crida a la capçalera",
             r["prova"].startswith(f"\\bancrequereix{{{banc['versio']}}}\n\n\\capsaleraexamen"),
             r["prova"][:60])
    comprova("porta les preguntes numerades Q1, Q2…",
             "\\encapcalament{Q1}" in r["prova"] and "\\encapcalament{Q2}" in r["prova"])
    comprova("i és exactament el cos del fitxer «tot en un»", r["prova"].strip() in r["tex"])
    comprova("el catàleg porta l'entorn: main.tex, headers.tex i defs.tex",
             all(banc.get(k, "").strip() for k in ("main", "headers", "defs")))
    comprova("i el defs.tex hi declara el segell de versió",
             f"\\def\\bancversio{{{banc['versio']}}}" in banc["defs"])

    # 1i. El banc és públic: no hi pot haver cap dada del centre
    rastres = ("logo-institut", "Nom i cognoms", "Qualificació:", "DEPARTAMENT DE",
               "cursacademic", "Miquel Tarradell")
    tot = banc["headers"] + banc["defs"] + banc["main"] + banc["plantilla"]
    trobats = [r for r in rastres if r in tot]
    comprova("els fitxers de format no porten cap dada del centre", not trobats, str(trobats))
    cataleg_sencer = (ARREL / "cataleg.js").read_text(encoding="utf-8")
    trobats = [r for r in rastres if r in cataleg_sencer]
    comprova("ni el catàleg tampoc", not trobats, str(trobats))
    comprova("la capçalera d'examen és buida al banc i es pot redefinir a la carpeta",
             "\\providecommand{\\capsaleraexamen}{}" in banc["defs"]
             and "capsalera.tex" in banc["main"], "")

    # 1j. El color de les gràfiques viu a defs.tex, no a les preguntes
    colors = re.compile(r"\\[(?:red|blue|green|orange|violet)[,!\\]]")
    amb_color = [q["id"] for q in banc["preguntes"] if colors.search(q["tex"])]
    comprova("cap pregunta no escriu un color a mà: fan servir \\colorgrafica",
             not amb_color, str(amb_color))
    comprova("i defs.tex el defineix", "\\newcommand{\\colorgrafica}" in banc["defs"])

    # 2. Una adreça amb codis inexistents i brossa no ha de petar
    r = web("bolzano-biseccio:q999,no-existeix:q001,,limits-punt:q001,limits-punt:q001")
    comprova("codi inexistent → primera variant, sense petar",
             r["ids"] == ["u7/bolzano-biseccio/q001", "u7/limits-punt/q001"], r["ids"])
    comprova("l'adreça es normalitza a codis estables",
             r["hash"] == "bolzano-biseccio:q001,limits-punt:q001", r["hash"])

    # 2b. Adreces mal formades: el que no s'entén s'ignora; la pàgina no peta
    for hash_, nom in (("limits-punt:q001,%", "un % solt"),
                       ("limits-punt:q001,%E2%9C", "una seqüència UTF-8 retallada"),
                       ("__proto__:q001,constructor,limits-punt:q001", "noms interns de JavaScript")):
        try:
            r = web(hash_)
            ok = r["ids"] == ["u7/limits-punt/q001"] and r["hash"] == "limits-punt:q001"
            detall = f"{r['ids']} · #{r['hash']}"
        except AppPetada as e:
            ok = False
            detall = "app.js peta: " + next((l for l in str(e).splitlines() if "Error" in l), str(e)[:120])
        comprova(f"una adreça amb {nom} s'ignora sense petar", ok, detall)

    # 3. Una selecció buida
    r = web("")
    comprova("sense selecció no hi ha preguntes", r["ids"] == [] and "Cap" in r["recompte"], r["recompte"])

    print(f"\n{'✓ El lloc i el build munten exactament el mateix.' if not fallades else f'✗ {fallades} comprovació(ns) fallides.'}")
    return 1 if fallades else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AppPetada as e:
        sys.exit(f"app.js ha petat dins de Node:\n{e}")
