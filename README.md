# Banc de preguntes · Matemàtiques II (CT)

Eina del professor per muntar exàmens de Matemàtiques II (2n de Batxillerat, Catalunya) a
partir d'un banc de preguntes escrites en LaTeX.

Tries uns quants temes i el lloc et proposa una pregunta de 2,5 punts per a cada tema. En
veus l'enunciat i la solució en PDF, i en baixes el codi `.tex`, sol o muntat en un examen
complet. El banc inclou **preguntes reals de la PAU**, i cadascuna porta la seva procedència
(«PAU juny 2026, sèrie 1»).

> **Estat a 28 de setembre de 2026:** 97 preguntes. N'hi ha 24 de la unitat 7 (Límits i
> continuïtat) en 8 temes i 18 de la unitat 8 (Derivades) en 6 temes, totes amb tres variants
> per tema; 12 de la unitat 9 (Aplicacions de les derivades) en 4 temes, també amb tres
> variants; 15 de la unitat 10 (Representació de funcions) en 5 temes, també amb tres variants; 12 de la unitat 13 (Probabilitat) en 4 temes, també amb tres
> variants; 6 de la unitat 14 (la distribució binomial) en 2 temes, també amb tres variants; i 10 de la PAU (les dues
> sèries de juny de 2026). **Les 87 preguntes de les unitats 7 a 10, 13 i 14 ofereixen una tria** en algun
> apartat: un altre cas, una altra tècnica o una tasca diferent de la del defecte, amb el seu
> propi Enunciat i Solució, triable des de la mateixa carta. El detall
> de la feina feta i pendent és a [`handout.md`](handout.md).

---

## Ús

1. Obre `index.html` amb doble clic. No cal servidor ni connexió.
2. A l'esquerra hi ha els temes, agrupats per unitat. La PAU hi té el seu grup propi, amb
   quatre blocs: Àlgebra, Geometria, Anàlisi i Probabilitat. Cada unitat es plega i es desplega
   clicant-ne el títol. Plegada, diu quantes preguntes seves hi ha a l'examen, i el navegador
   recorda quines has plegat.
3. **Cada clic a un tema hi afegeix una pregunta** d'aquell tema. Un segon clic n'afegeix una
   altra, si n'hi ha. El quadret diu quantes n'hi ha a l'examen, i el número de la dreta,
   quantes en té el tema.
4. Cada pregunta és una targeta. Amb ◀ ▶ passes d'una variant a l'altra del mateix tema, amb
   ▲ ▼ la mous i amb ✕ la treus. Una mateixa pregunta no hi pot sortir dues vegades.
5. **Si un apartat ofereix una tria**, la targeta hi mostra un selector amb cada alternativa i
   els seus punts a la durada triada: quants ítems calculadors dur (un límit o quatre), o una
   alternativa sencera per al mateix apartat (classificar una discontinuïtat o llegir imatges
   d'una gràfica). Sense tocar-hi res, l'examen surt exactament igual que si la tria no
   existís. Canviar-la pot fer que la pregunta ja no sumi 2,50: el comptador de la targeta i el
   de baix de tot ho avisen en viu. Cada tria té el seu propi **Enunciat** i **Solució**, de
   només l'alternativa triada: mai cal triar a cegues. Si els tens oberts i canvies l'ítem,
   s'actualitzen sols. L'Enunciat i la Solució de la pregunta sencera, més avall, mostren
   sempre el defecte; el `.tex` que en baixis, en canvi, ja reflecteix la tria feta.
6. **Per defecte, l'examen té l'estructura de la PAU.** Les cinc primeres preguntes queden
   numerades com a 1, 2, 3, 4a i 4b: l'alumne fa la 1, la 2 i la 3, i tria entre la 4a i la 4b.
   Val igual per a preguntes dels temes, de la PAU o barrejades en qualsevol ordre.
   L'estructura és de les places, no de les preguntes: si en treus o en mous una, la 4a i la
   4b continuen al seu lloc. **Opció de l'anterior** canvia l'estructura d'una plaça. A la 4b,
   la separa (1, 2, 3, 4, 5); a qualsevol altra, la converteix en una alternativa de
   l'anterior. Una opció compta una sola vegada als punts, i als minuts es compta la més
   llarga.
7. **Durada.** A dalt de l'examen tries **1 h 30** o **50 min**. A 50 min, cada pregunta fa
   servir la seva versió de 50 min: menys apartats i els punts repartits de nou. Si no en té,
   hi va sencera i la targeta ho diu amb l'etiqueta «sencera». El comptador compara els
   minuts amb la durada triada. El `.tex` que baixes ja surt net per a aquesta durada: no hi
   ha els apartats que es treuen, i els punts hi són escrits tal com surten. El que diu el
   `.tex` és exactament el que surt al PDF.
8. A cada targeta: **Enunciat** i **Solució** obren el PDF, i **.tex** baixa aquella pregunta
   sola. Tot segueix la durada triada (i, si n'hi ha, la tria feta).
9. A baix: **prova-N.tex** baixa el cos de l'examen per a la carpeta d'exàmens (vegeu més
   avall). Cada pregunta hi porta la seva etiqueta: `\encapcalament{Q4a}`. Les solucions hi
   van a dins, i les fa sortir l'interruptor `\solucionstrue` del teu `main.tex`. **Tot en
   un** baixa l'examen en un sol fitxer, preàmbul inclòs, per si no vols carpeta —sempre sense
   solucions—. El comptador es posa verd quan l'examen fa 10 punts.

### La carpeta d'exàmens

Es prepara un sol cop. A la columna dels temes, l'apartat **Entorn** baixa els tres fitxers:

```
examens/
  main.tex            \input de la prova que vulguis compilar
  headers.tex         paquets i format de pàgina
  defs.tex            macros del banc, amb el segell de versió
  capsalera.tex       la capçalera del teu centre (la poses tu)
  logo-institut.png   el teu logo (el poses tu)
  prova-1.tex         cos de l'examen, baixat del lloc
  prova-2.tex         …
```

**El banc no porta cap dada de cap centre**: ni logo, ni segell, ni departament, ni casella de
nota. Aquí, `\capsaleraexamen` no escriu res, i per això els PDF del banc i el lloc web no
ensenyen cap capçalera. Si a la carpeta hi ha un `capsalera.tex` que la redefineixi, `main.tex`
l'incorpora tot sol i la capçalera surt només quan compiles tu.

Per fer un examen: tria les preguntes, baixa `prova-N.tex`, posa'l a la carpeta i compila
`main.tex`. Per al full del professorat, canvia `\solucionsfalse` per `\solucionstrue`.

Si el `defs.tex` que tens és d'una altra versió que l'examen, LaTeX avisa al registre: «aquest
defs.tex no és el que va generar l'examen». Aleshores, torna a baixar `headers.tex` i
`defs.tex` des d'**Entorn**.

L'examen queda desat a l'adreça, i es pot guardar als marcadors i recuperar exactament igual:

```
index.html#analisi:ana-26j-q1,algebra:alg-26j-q2,probabilitat:pro-26j-q3,analisi:ana-26j-q4a|geometria:geo-26j-q4b
```

La coma separa preguntes i la barra uneix les opcions d'una mateixa pregunta. Un examen de
50 min porta el prefix `50min/` (`index.html#50min/limits-punt:q001,…`). Les adreces desades
abans continuen funcionant: són exàmens d'1 h 30.

Les targetes PAU porten un accent taronja, la procedència i la llista d'unitats que la classe
ha d'haver fet per poder resoldre la pregunta sencera («cal haver fet: u7 · u8 · u12»).

---

## Com està fet

El projecte segueix cinc principis. Totes les decisions de disseny en surten.

1. **Font única.** Les úniques fonts són `pregunta.tex` i `meta.json` de cada pregunta. Els
   PDF de `out/` i `cataleg.js` són fitxers generats, i no s'editen mai a mà.
2. **Un sol format i una sola plantilla.** Totes les preguntes compilen amb
   `build/headers.tex` (paquets) i `build/defs.tex` (macros), que són també els que es baixen
   des d'**Entorn**. L'assemblatge d'un examen el fa `build/embolcall.tex`, i és la
   mateixa plantilla per al build (Python) i per al lloc (JavaScript). Una prova
   n'assegura la paritat byte a byte.
3. **Validació que falla tancada.** Si una pregunta no compleix alguna regla, o no compila, el
   build falla i no escriu res: ni un sol PDF ni el catàleg. Els PDF es compilen en una
   carpeta temporal i només es copien a `out/` quan tot és correcte. Val més no publicar que
   publicar un banc inconsistent.
4. **Lloc sense dependències.** És HTML, CSS i JavaScript sense cap llibreria. El catàleg
   incrusta el codi LaTeX de cada pregunta, així que el lloc no fa cap petició i funciona
   obert com a fitxer local.
5. **Identificadors estables.** Els codis (`q001`, `ana-26j-q1`) són permanents. Les adreces
   desades i els exàmens ja muntats en depenen.

```
 pregunta.tex ─┐                      ┌─► out/enunciat.pdf, out/solucio.pdf
 meta.json    ─┼─► build/build.py ───┼─► out/enunciat-curt.pdf, out/solucio-curt.pdf
 temes.json   ─┤   (valida, compila)  │    (només si té versió de 50 min)
 headers.tex  ─┤                      └─► cataleg.js ──► index.html + assets/app.js
 defs.tex     ─┤                                          (tria, previsualitza, munta
 pau/convocatories.json ─┘                                 prova-N.tex i l'entorn)
```

---

## Estructura

```
index.html                 la pàgina (única)
assets/app.js              lògica del lloc: examen, opcions, variants, assemblatge, descàrregues
assets/style.css           estil (clar i fosc)
cataleg.js                 GENERAT: preguntes, format (headers i defs) i plantilles
temes.json                 unitats i temes (slugs estables)
build/
  build.py                 valida, compila els PDF i genera cataleg.js
  headers.tex              paquets i format de pàgina (congelat)
  defs.tex                 macros del banc (congelat)
  main.tex                 plantilla de la carpeta d'exàmens
  embolcall.tex            plantilla d'assemblatge (compartida amb app.js)
  prova_validacio.py       comprova que cada regla fa fallar el build
  prova_sortida.py         comprova que un build que falla no escriu res
  prova_paritat.py         comprova que el lloc i el build munten el mateix .tex
u7/<tema>/<q001>/          preguntes del banc: pregunta.tex, meta.json, out/
u8/<tema>/<q001>/          una carpeta per unitat, amb els seus temes
pau/convocatories.json     registre de convocatòries PAU i les seves sèries (amb font)
pau/<bloc>/<codi>/         preguntes PAU: pregunta.tex, meta.json, out/
.github/workflows/         Action que prova, compila i desa els fitxers generats
handout.md                 feina feta i feina pendent
```

---

## Afegir una pregunta del banc

1. Copia una carpeta existent, per exemple `u7/bolzano-biseccio/q002/`, amb el codi següent
   lliure: `u7/bolzano-biseccio/q003/`.
2. Edita `pregunta.tex` i `meta.json`. No toquis res de `out/`.
3. Puja-ho al repositori. Amb `git push`, l'Action s'executa sola. Si ho puges per `_uploads`,
   llança-la a mà (vegeu «GitHub i compilació»). L'Action valida, compila i desa els PDF. Si
   alguna cosa falla, no es desa res, i la pestanya **Actions** en diu el motiu exacte.

Un tema nou s'afegeix primer a `temes.json` i després se'n crea la carpeta.

Per oferir-hi una tria en lloc d'un apartat fix, substitueix l'`\apartat{…}` i el seu cos per
un `\begin{tria}{id}…\end{tria}` amb els `\itemtria{id}{punts}` que calguin (vegeu «Tries:
quan un apartat ofereix més d'un ítem», més amunt). El primer ítem declarat és el defecte:
si només n'hi ha un, la tria es comporta com un apartat normal.

## Afegir una pregunta PAU

Les preguntes PAU viuen a `pau/<bloc>/<codi>/`, on el bloc és `algebra`, `geometria`,
`analisi` o `probabilitat`. El codi és el mateix identificador del repositori `pau`:

```
pau/analisi/ana-26j-q1/     →  bloc ana · convocatòria 26j · exercici q1
```

Del codi, el build en treu la convocatòria (`26j`). A `pau/convocatories.json` hi busca la
sèrie, i escriu la procedència just sota la capçalera de la pregunta:

```latex
\encapcalament{Pregunta 3}
\procedencia{PAU juny 2026, sèrie 1}
```

Tres convencions que cal respectar:

- **L'enunciat és literal**, en la forma de vosaltres de la PAU.
- **La solució és el criteri d'avaluació oficial**, i cada apartat acaba amb la seva pauta
  oficial («*Pauta oficial:* 0,25 per…»). Si el criteri oficial conté una errada, es
  corregeix i es deixa una *Nota del banc* que ho digui.
- Els apartats es numeren a), b), c)…, com la resta del banc, encara que l'original digui
  1.1, 1.2…

El procediment complet per importar una convocatòria és a `handout.md`.

---

## Les regles

| # | Regla | Qui la fa complir |
|---|---|---|
| 1 | Les fonts són `pregunta.tex` i `meta.json`. `out/` i `cataleg.js` són **generats**: no s'editen mai. Un build complet n'esborra els PDF que ja no genera cap font. | l'Action els sobreescriu |
| 2 | Tota pregunta val **2,50 punts**. Cada apartat és múltiple de **0,25**. | `build.py` |
| 3 | La puntuació s'escriu **només** a `\apartat{...}`. Enlloc més. L'opcional és la de 50 min: `\apartat[1,25]{0,75}`. Les dues puntuacions sumen 2,50. | `build.py` la llegeix del `.tex` |
| 4 | Una pregunta és **només el cos**: sense `\documentclass`, `\usepackage` ni `\begin{document}`. | `build.py` |
| 5 | Hi ha **un sol format**: `build/headers.tex` i `build/defs.tex`. Un paquet nou s'afegeix allà i es recompila tot. | `build.py` |
| 5b | Cap pregunta no escriu un **color**: les gràfiques dibuixen amb `\colorgrafica`, que es defineix a `defs.tex` i es pot canviar des de la carpeta d'exàmens. | `prova_paritat.py` |
| 6 | Els codis `q001`, `q002`… són **permanents**: mai es renumeren ni es reaprofiten. | tu |
| 7 | `\end{solucio}`, `\begin{nomesllarg}` i `\end{nomesllarg}` van **sols a la seva línia**. | `build.py` |
| 8 | Tota graella de TikZ declara el pas: `grid` sempre amb `step=1` (o el que calgui). Sense, TikZ fa passos d'1 cm i la graella queda desquadrada respecte dels enters. | `build.py` |
| 9 | La línia «PAU juny 2026, sèrie 1» **no s'escriu mai a mà**: la posa el build a partir del codi de la pregunta i de `pau/convocatories.json`. | `build.py` |
| 10 | Una sèrie entra al registre **només amb font**. Una dada sense font no s'imprimeix en un examen. | `build.py` |
| 11 | La versió de 50 min la decideix **qui escriu la pregunta**: quins apartats es treuen (`nomesllarg`) i com es reparteixen els punts. Amb versió de 50 min, `meta.json` porta `minuts_curt`; sense, no el porta. | `build.py` |
| 12 | Un `\begin{tria}{id}…\end{tria}` substitueix l'apartat sencer i n'ofereix diversos `\itemtria{id}{punts}` —cossos complets, amb la seva pròpia solució—, dels quals se'n materialitza sempre **exactament un**. | `build.py` |
| 13 | Els identificadors d'una tria i dels seus ítems són **permanents**, com `q001`: mai es renumeren ni es reaprofiten. | tu |
| 14 | Sense selecció, es materialitza el **primer ítem declarat** (o el de `[defecte-curt=id]` a 50 min, si n'hi ha). Aquest defecte és l'únic que `build.py` garanteix que sumi 2,50 a cada modalitat; una combinació que el professor triï lliurement al lloc es valida allà, en viu, no en temps de build. | `build.py` i `app.js` |
| 15 | Una tria no pot ser dins d'un `nomesllarg`. | `build.py` |
| 16 | Una alternativa ha de canviar el que l'alumne decideix (un altre cas, una altra tècnica o el raonament a la inversa), no només els nombres de l'enunciat. Canviar un nombre val si canvia el cas: un 0/0 que passa a ser 3/0. | tu |

A més, el build comprova: que els slugs de `temes.json` siguin únics; que cada tema sigui a
la carpeta de la seva unitat; que el format dels codis sigui correcte (`q001` al banc,
`ana-26j-q1` a la PAU); que el prefix d'una PAU correspongui al seu bloc; i que la
convocatòria existeixi al registre.

## Macros de `defs.tex`

| Escrius | Surt |
|---|---|
| `\begin{apartats} … \end{apartats}` | llista a) b) c) |
| `\apartat{0,75}` | **a)** *(0,75 punts)* |
| `\apartat[1,25]{0,75}` | 0,75 punts a l'examen d'1 h 30 i 1,25 al de 50 min |
| `\begin{nomesllarg} … \end{nomesllarg}` | un apartat sencer, amb la seva solució, que només surt a l'examen d'1 h 30; els de després es tornen a lletrejar sols |
| `\begin{graella}{3} \sa … & \sa … \end{graella}` | i) ii) iii) en columnes, amb els `\lim` en mode display |
| `\si{-1\le x\le 2}` dins de `cases` | «si −1 ≤ x ≤ 2», amb el signe ben espaiat |
| `\begin{solucio} … \end{solucio}` | només apareix a la versió amb solucions, en blau |
| `\procedencia{…}` | la línia PAU; **només la fa servir el build** |

Tota la resta és LaTeX normal.

### Tries: quan un apartat ofereix més d'un ítem

`\apartat[x]{y}` i `nomesllarg` trien entre **dues** coses (la durada). Quan calen **més de
dues** —quants ítems i quins, o una alternativa sencera per al mateix apartat—, s'usa una
tria, que substitueix l'apartat de cap a peus:

```latex
\begin{tria}{determina-a}
\itemtria{amb-reflexio}{1}{1,25}
Considera la funció …
\begin{solucio} … \end{solucio}

\itemtria{sense-reflexio}{0,5}
Considera la funció, una mica més curta …
\begin{solucio} … \end{solucio}
\end{tria}
```

`\begin{tria}{id}` porta un identificador de tria (com un slug de tema) i, opcionalment,
`[defecte-curt=id-item]` si el defecte de 50 min no ha de ser el primer ítem. Cada
`\itemtria{id}{punts}` (o `\itemtria{id}{punts-1h30}{punts-50min}`, com `\apartat[x]{y}`) és
un cos complet, amb la seva pròpia solució. Sense tocar res, es materialitza sempre el
primer ítem declarat —el `.tex` és idèntic al d'abans que existissin les tries—, i cada
plaça de l'examen pot triar-ne un altre des de la seva carta. Com `nomesllarg`, `tria` i
`itemtria` només són a les fonts: `materialitza()` els resol abans que `defs.tex` en vegi
cap, i el `.tex` que es baixa ja porta un `\apartat{…}` normal amb el cos triat.

El build compila, a més, l'enunciat i la solució de **cada ítem, tot sol**, a
`out/tries/<id-tria>/<id-item>/`: al lloc, cada tria té el seu propi Enunciat i Solució, de
només l'alternativa triada, perquè no cal triar-la a cegues.



## `meta.json`

Una pregunta del banc:

```json
{
  "titol": "Teorema de Bolzano, bisecció i punt de tall de dues corbes",
  "temes_secundaris": [],
  "dificultat": "●●○",
  "origen": [112, 113, 114, 120],
  "minuts": 14,
  "etiquetes": ["Bolzano", "bisecció"]
}
```

`origen` són els exercicis del llibre que inspiren la pregunta. `dificultat` és `●○○`, `●●○`
o `●●●`. El tema principal és la carpeta on viu la pregunta. `minuts` és el temps a l'examen
d'1 h 30. Si la pregunta té versió de 50 min, `minuts_curt` n'és el temps (per exemple,
`"minuts": 20, "minuts_curt": 11`).

Una pregunta PAU no té `origen` ni `temes_secundaris`. En lloc d'això té `unitats`, que diu
fins on ha d'haver arribat la classe per poder-la fer sencera. Si la llista és buida, el
build avisa.

```json
{
  "titol": "Funció a trossos amb exponencial i paràbola: continuïtat, àrea i tangent",
  "unitats": ["u7", "u8", "u12"],
  "dificultat": "●●○",
  "minuts": 22,
  "etiquetes": ["continuïtat amb paràmetre", "àrea", "recta tangent"]
}
```

---

## Proves

```
python3 build/prova_validacio.py   # 29 avaries provocades: cadascuna ha de fer fallar el build
python3 build/prova_sortida.py     # un build que falla no escriu res (no cal TeX)
python3 build/build.py             # valida i compila (cal TeX Live)
python3 build/prova_paritat.py     # el .tex del lloc = el del build, byte a byte (cal Node)
```

Opcions de `build.py`:

- `--nomes-cataleg` revalida i regenera el catàleg sense compilar.
- `--pregunta RUTA` compila només les preguntes que la contenen. El catàleg sempre les inclou
  totes.
- `--headers FITXER` compila amb uns altres paquets, per exemple si a l'entorn en falten.
  Aquests PDF no són definitius i el build ho avisa. El catàleg porta sempre
  `build/headers.tex` i `build/defs.tex`, que són els que el lloc posa als `.tex`.
- `--tot` recompila tots els PDF. Sense aquesta opció, el build només recompila els PDF el
  document dels quals ha canviat: cada PDF porta a les metadades l'empremta del document que
  l'ha produït i de la versió de `pdflatex`, i si coincideix, el reutilitza. Canviar
  `headers.tex` o `defs.tex` ho recompila tot. Els PDF són reproduïbles (data i identificador
  fixos): la mateixa font dona el mateix fitxer, byte a byte.

## GitHub i compilació

L'Action `.github/workflows/compila.yml` s'executa sola quan canvia una font. Primer executa
les proves del validador i la de sortida, després el build complet, després la prova de
paritat, i finalment desa els PDF i el catàleg amb un commit propi. Si mentrestant algú ha fet
push a la branca, el bot incorpora aquell commit i torna a provar-ho, fins a tres cops. També es
pot llançar a mà, des de **Actions → Compila el banc → Run workflow**.

**Canvis que arriben per `_uploads`.** Els lliuraments es pugen com a ZIP a la carpeta
`_uploads`, i un workflow d'extracció els descomprimeix a l'arrel. Aquest commit del bot **no**
dispara «Compila el banc», perquè GitHub no encadena workflows. Per això, després de cada
pujada que canviï fonts, cal llançar el build a mà. Els fitxers de `.github/workflows/` no poden
arribar per aquesta via, perquè el bot no hi té permís: es creen i s'editen des de la web de
GitHub.

**Els PDF i `cataleg.js` només els desa l'Action.** Si fas un build al Codespace, no en facis
commit: `git restore cataleg.js '*.pdf'` els deixa com eren. Si no, el commit del bot els
tornaria a modificar i el següent `git pull` donaria conflictes. Abans de començar a treballar,
sempre `git pull`.

El repositori ha de ser **privat**, perquè conté les solucions. Amb el pla gratuït de GitHub,
les Actions en repositoris privats consumeixen minuts d'una quota mensual; cada build en
gasta uns pocs.

GitHub Pages no serveix per publicar el lloc. Amb el pla gratuït només publica repositoris
públics, i amb un pla de pagament el lloc publicat seria igualment públic, amb les solucions.
Per això el lloc està pensat per obrir-se en local: baixant el repositori (Code → Download
ZIP) i fent doble clic a `index.html`.

### Veure el lloc des del Codespace

1. Al terminal del Codespace: `python3 -m http.server 8000`.
2. A la pestanya **Ports**, el port 8000 → icona del globus («Open in Browser»).

El port és **privat** per defecte: només hi pot entrar qui ha creat el Codespace, identificat
a GitHub. No el canviïs a «Public». Per aturar el servidor, `Ctrl+C` al terminal.

## Procedència i drets

- Els enunciats de la PAU i els criteris d'avaluació oficials són de l'Oficina d'Accés a la
  Universitat (Consell Interuniversitari de Catalunya). S'hi reprodueixen per a ús docent
  dins d'aquest repositori privat.
- La classificació de les preguntes PAU prové del repositori `pau`, i la seqüenciació
  d'exercicis del llibre, del solucionari de l'alumnat (`sol-main`).
- Els números d'`origen` remeten als exercicis del llibre de text; el banc no en reprodueix
  els enunciats.
