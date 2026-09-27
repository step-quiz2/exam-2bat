#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════
#  prova_sortida.py — comprova QUÈ escriu build.py i QUAN
#  ─────────────────────────────────────────────────────────────────────
#  1. Un build que falla no escriu res: ni PDF ni catàleg.
#  2. Un build correcte escriu els PDF que ha compilat, i només aquests.
#  3. --headers només canvia la compilació: el catàleg porta sempre els
#     fitxers de format oficials, que són els que el lloc posa als .tex.
#
#  No cal TeX. La prova posa al PATH un pdflatex fals que «compila» en un
#  instant i copia dins del PDF el .tex que ha rebut: així es veu quins
#  fitxers s'han tocat i amb quin preàmbul s'han compilat.
#
#  Ús:   python3 build/prova_sortida.py
# ═══════════════════════════════════════════════════════════════════════

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
PROVA = "% PREAMBUL DE PROVA (prova_sortida.py)"

# \provocaerror només fa fallar la versió AMB solucions, com passaria amb una
# ordre desconeguda dins d'un \begin{solucio}: l'enunciat compilaria bé.
PDFLATEX_FALS = r'''#!/usr/bin/env python3
import sys
from pathlib import Path
tex = Path("main.tex").read_text(encoding="utf-8")
if r"\provocaerror" in tex and r"\solucionstrue" in tex:
    Path("main.log").write_text("! Undefined control sequence.\n", encoding="utf-8")
    sys.exit(1)
Path("main.pdf").write_text("%PDF-fals\n" + tex, encoding="utf-8")
Path("main.log").write_text("Output written on main.pdf (1 page, 1 bytes).\n", encoding="utf-8")
'''


def copia_banc(tmp: Path) -> Path:
    banc = tmp / "banc"
    shutil.copytree(ARREL, banc, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return banc


def edita(fitxer: Path, vell: str, nou: str) -> None:
    text = fitxer.read_text(encoding="utf-8")
    assert vell in text, f"la prova no troba «{vell}» a {fitxer.name}"
    fitxer.write_text(text.replace(vell, nou, 1), encoding="utf-8")


def empremta(banc: Path) -> dict[str, str]:
    """Hash de cada fitxer que el build pot escriure: els PDF i el catàleg."""
    fitxers = sorted(banc.glob("*/*/*/out/*.pdf")) + [banc / "cataleg.js"]
    return {f.relative_to(banc).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in fitxers if f.exists()}


def cataleg(banc: Path) -> dict:
    text = (banc / "cataleg.js").read_text(encoding="utf-8")
    return json.loads(text.split("const BANC = ", 1)[1].rstrip().rstrip(";"))


def build(banc: Path, fals: Path, *opcions: str) -> subprocess.CompletedProcess:
    entorn = {**os.environ, "PATH": f"{fals}{os.pathsep}{os.environ.get('PATH', '')}"}
    return subprocess.run([sys.executable, str(banc / "build" / "build.py"), *opcions],
                          capture_output=True, text=True, env=entorn)


def main() -> int:
    fallades = 0

    def comprova(nom: str, cond: bool, detall: str = "") -> None:
        nonlocal fallades
        fallades += not cond
        print(f"  {'✓' if cond else '✗'} {nom}" + (f"\n      {detall}" if not cond and detall else ""))

    with tempfile.TemporaryDirectory() as t:
        fals = Path(t) / "fals"
        fals.mkdir()
        (fals / "pdflatex").write_text(PDFLATEX_FALS, encoding="utf-8")
        (fals / "pdflatex").chmod(0o755)

        # 1. Una pregunta invàlida, l'última a compilar-se: les 17 anteriors ja
        #    s'han compilat bé quan el build descobreix l'error.
        with tempfile.TemporaryDirectory() as t1:
            banc = copia_banc(Path(t1))
            edita(banc / "u7/parametres-ab/q001/pregunta.tex", r"\apartat[2,5]{1,5}", r"\apartat[2,5]{1,25}")
            abans = empremta(banc)
            r = build(banc, fals)
            tocats = sorted(k for k, v in empremta(banc).items() if abans.get(k) != v)
            comprova("una pregunta invàlida fa fallar el build",
                     r.returncode == 1 and "han de sumar 2,50" in r.stderr, r.stderr[-300:])
            comprova("i el build fallit no toca cap PDF ni el catàleg",
                     not tocats, f"{len(tocats)} fitxers tocats, p. ex. {tocats[:3]}")

        # 2. Una pregunta l'enunciat de la qual compila però la solució no.
        with tempfile.TemporaryDirectory() as t2:
            banc = copia_banc(Path(t2))
            edita(banc / "u7/limits-punt/q001/pregunta.tex",
                  r"\begin{solucio}", "\\begin{solucio}\n\\provocaerror")
            abans = empremta(banc)
            r = build(banc, fals)
            tocats = sorted(k for k, v in empremta(banc).items() if abans.get(k) != v)
            comprova("una solució que no compila fa fallar el build",
                     r.returncode == 1 and "no compila" in r.stderr, r.stderr[-300:])
            comprova("i no se'n desa ni l'enunciat, que sí que compilava",
                     not tocats, f"{len(tocats)} fitxers tocats, p. ex. {tocats[:3]}")

        # 3. Un build correcte escriu tots els PDF (control positiu).
        with tempfile.TemporaryDirectory() as t3:
            banc = copia_banc(Path(t3))
            r = build(banc, fals)
            pdfs = sorted(banc.glob("*/*/*/out/*.pdf"))
            escrits = [p for p in pdfs if p.read_text(encoding="utf-8", errors="replace").startswith("%PDF-fals")]
            comprova(f"un build correcte escriu els {len(pdfs)} PDF",
                     r.returncode == 0 and pdfs and len(escrits) == len(pdfs),
                     f"codi {r.returncode}; {len(escrits)} de {len(pdfs)} escrits\n{r.stderr[-300:]}")

        # 4. --pregunta només escriu els PDF de la pregunta demanada.
        with tempfile.TemporaryDirectory() as t4:
            banc = copia_banc(Path(t4))
            abans = empremta(banc)
            r = build(banc, fals, "--pregunta", "u7/limits-punt/q001")
            tocats = sorted(k for k, v in empremta(banc).items()
                            if abans.get(k) != v and k.endswith(".pdf"))
            # La pregunta té versió de 50 min: quatre PDF.
            esperats = sorted(f"u7/limits-punt/q001/out/{nom}.pdf"
                              for nom in ("enunciat", "enunciat-curt", "solucio", "solucio-curt"))
            comprova("--pregunta només escriu els PDF d'aquella pregunta, també els de 50 min",
                     r.returncode == 0 and tocats == esperats, f"codi {r.returncode}; tocats {tocats}")

        # 5. --headers: els PDF es compilen amb uns altres paquets; el catàleg
        #    porta sempre els oficials, amb el segell de versió del format.
        with tempfile.TemporaryDirectory() as t5:
            banc = copia_banc(Path(t5))
            oficials = (banc / "build/headers.tex").read_text(encoding="utf-8")
            de_prova = Path(t5) / "headers-prova.tex"
            de_prova.write_text(PROVA + "\n" + oficials.replace("\\usepackage{microtype}\n", ""),
                                encoding="utf-8")
            r = build(banc, fals, "--headers", str(de_prova))
            pdf = (banc / "u7/limits-punt/q001/out/enunciat.pdf").read_text(encoding="utf-8", errors="replace")
            comprova("--headers compila els PDF amb els paquets de prova",
                     r.returncode == 0 and PROVA in pdf, f"codi {r.returncode}\n{r.stderr[-300:]}")
            comprova("però el catàleg porta els paquets oficials",
                     r.returncode == 0 and cataleg(banc)["headers"] == oficials,
                     "el catàleg porta uns headers que no són build/headers.tex")
            comprova("i el defs del catàleg porta el segell de versió",
                     r.returncode == 0
                     and f"\\def\\bancversio{{{cataleg(banc)['versio']}}}" in cataleg(banc)["defs"],
                     "falta el segell al defs.tex del catàleg")
            comprova("i el build avisa que aquests PDF no són definitius",
                     "no són definitius" in r.stdout, r.stdout[-300:])

    print(f"\n{'✓ El build només escriu quan tot és correcte.' if not fallades else f'✗ {fallades} comprovació(ns) fallides.'}")
    return 1 if fallades else 0


if __name__ == "__main__":
    sys.exit(main())
