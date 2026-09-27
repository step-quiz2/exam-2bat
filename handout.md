# Handout · Banc de preguntes de Matemàtiques II

**Data:** 22 de setembre de 2026 · **Estat:** 64 preguntes (24 de la unitat 7, 18 de la unitat
8, 12 de la unitat 9, 5 de la unitat 10 i 5 de la PAU) · 1.200 minuts d'examen al banc · 29 comprovacions del validador, 10 de sortida del build i 59 de
paritat

Aquest document explica tota la feina feta fins avui i tota la feina pendent, amb prou
detall perquè qualsevol persona pugui reprendre el projecte sense haver seguit les converses
on es va construir. El README descriu com és el projecte; aquest document explica com hi hem
arribat i cap on ha d'anar.

---

## 1. Resum

El projecte ha passat per cinc sessions. La primera va avaluar un `main.tex` fet per una
altra IA i en va treure les lliçons. La segona va construir l'arquitectura: el build, el lloc
web, l'Action de GitHub i les proves. La tercera va completar la unitat 7, amb 13 preguntes
verificades. La quarta va obrir la secció PAU i hi va importar l'examen sencer de juny de
2026. La cinquena va revisar el projecte sencer, en va corregir quatre errors, va fixar les
prioritats i va afegir els exàmens amb opcions (1, 2, 3, 4a i 4b). La sisena va donar aire al
format, va crear les dues modalitats d'examen, d'1 h 30 i de 50 min, i va reescriure a mida PAU
totes les preguntes de la u7, amb dues de noves. La setena va tancar la u7 i va fer la u8
sencera: sis temes i nou preguntes. La vuitena va canviar la manera de lliurar els exàmens: el
lloc dona el cos de la prova per a la carpeta del professorat. La novena va completar la u7
amb una tercera variant de cada tema, i la desena va fer el mateix amb la u8. L'onzena i la dotzena van fer la u9,
amb quatre temes i tres variants de cadascun, i la tretzena va obrir la u10. La màquina
funciona de punta a punta. El que queda és
sobretot contingut: la u9, que acaba el 22 de novembre, els 56 exercicis PAU pendents i la
resta d'unitats.

---

## 2. Com hem arribat aquí

### 2.1 Sessió 1 · Avaluació del `main.tex` original

El punt de partida va ser un examen de límits i continuïtat, generat per una altra IA a
partir dels PNG del solucionari (`sol-main`). La valoració va ser de notable alt (≈7,5/10).

- **Matemàticament, impecable.** Es van verificar totes les respostes, i no n'hi havia cap
  d'errònia.
- **Bona alineació** amb els 23 exercicis assignats a les quatre setmanes de la unitat 7. Hi
  havia dues excepcions: un límit (polinomi entre exponencial) exigia la jerarquia d'infinits,
  que no era a cap exercici assignat; i hi faltaven radicals, valor absolut i logaritme a
  trossos.
- **Defectes de disseny.** Qui triava l'opció 4b no s'examinava de Bolzano, que era tota la
  quarta setmana. L'examen tenia uns 26 ítems, 55-70 minuts, massa just per a una sessió de 55.
- **Defectes de LaTeX.** `\text{si } -1` produïa un signe menys mal espaiat; l'`array` posava
  els `\lim` en estil de text; hi havia un `\displaystyle` en línia i una col·lisió de notació
  ($f$ per a dues funcions); el tractament barrejava «escolliu» i «determina»; la graella era
  massa clara; el separador quedava orfe; i les solucions eren comentaris morts després de
  `\end{document}`.
- **Un error que no es va detectar llavors:** la graella de la gràfica estava desquadrada
  respecte dels enters. Es va descobrir a la sessió 3 (vegeu l'apartat 4).

### 2.2 Sessió 2 · Arquitectura i primer lloc

Decisions del professor: els PDF els compila GitHub Actions (vàlid amb el pla gratuït); la
unitat mínima és una pregunta de 2,5 punts amb apartats múltiples de 0,25; i els exàmens no
porten capçalera.

Es va construir: `build.py` (validar, compilar, generar el catàleg), el preàmbul compartit,
la plantilla d'assemblatge única, el lloc (`index.html`, `app.js`, `style.css`), l'Action,
les dues bateries de proves i el README. Les cinc preguntes de l'examen original es van
migrar al format nou, corregides.

Abans de lliurar, es van trobar i tancar set errors del codi propi (vegeu l'apartat 4). El
més subtil: `String.replace` de JavaScript interpreta `$$` i `$'`, que són habituals en
LaTeX, i corrompia el `.tex` en silenci.

### 2.3 Sessió 3 · La unitat 7 completa

Es van omplir els tres temes buits (`limits-infinit`, `limits-trossos` i `parametres-ab`) i
es va afegir una segona variant als altres cinc: vuit preguntes noves. Cada enunciat es va
calibrar amb els exercicis reals del llibre, i cada `origen` diu la veritat. Es van cobrir
les llacunes detectades a la sessió 1. Per a l'exercici 114, es va seguir el conveni del
llibre: després d'una bisecció, tabula per dècimes.

Totes les respostes es van verificar per dos camins. En fer-ho, es va descobrir que
**SymPy 1.14 calcula malament** $\lim_{x\to-\infty}2^{x}$: diu $+\infty$. Es va contrastar
numèricament.

Es van corregir dos errors del `build.py`, i el més greu de tot el projecte: **la graella
TikZ desquadrada**. Afectava la pregunta de gràfiques que ja era publicada i l'examen
original.

### 2.4 Sessió 4 · La secció PAU

Es va analitzar el repositori `pau`: 62 preguntes, cadascuna amb enunciat (`-e`), pistes del
professor (`-p`) i **criteri d'avaluació oficial** (`-s`). Les 62 valen 2,5 punts amb
apartats múltiples de 0,25, i per tant encaixen al banc sense excepcions. La sessió 5 va
trobar que dues d'aquestes entrades són el mateix exercici: són 61 exercicis diferents
(vegeu 7.6).

La sèrie només apareix a la capçalera del criteri oficial del **primer exercici** de cada
document. D'allà se'n van treure set. Les de juny de 2023 les va confirmar el professor: van
ser les sèries 1 i 5, per aquest ordre, i no la 4 que deia l'exemple inicial. Les de
setembre de 2023 i juny de 2024 provenen d'una rèplica pública.

Troballa estructural: **cap pregunta PAU es pot fer sencera al final de la unitat 7.** Totes
les que toquen límits, continuïtat o Bolzano ho barregen amb derivades, monotonia o àrees.
Per això el professor va triar una **secció PAU per blocs** (Àlgebra, Geometria, Anàlisi i
Probabilitat), i cada pregunta indica fins a quina unitat cal haver arribat.

Es va importar l'examen sencer de juny de 2026, sèrie 1: exercicis 1, 2, 3, 4A i 4B. Es van
verificar 32 resultats dels criteris oficials, i es va trobar una errada al document oficial:
$D(4{,}5)=6{,}85$, quan el valor correcte és 6,875. Es va corregir amb una *Nota del banc*.

### 2.5 Sessió 5 · Revisió i correccions

Una revisió completa del codi, de les dades i de les 18 preguntes, contrastada amb els
repositoris `pau` i `sol` i amb el full de programació del curs.

- **Codi.** És net i està ben estructurat. S'hi van trobar quatre errors, tots corregits
  (vegeu l'apartat 4). El catàleg podia portar un preàmbul de prova i un build fallit deixava
  PDF escrits a `out/`. A més, una adreça mal formada deixava la pàgina en blanc, i el push del
  bot fallava si la branca avançava durant el build. Cada correcció té la seva prova, i s'ha
  comprovat que la prova falla amb el codi antic.
- **Contingut.** Es va fer una segona verificació independent de les 18 preguntes i no s'hi
  va trobar cap error. Tots els `origen` són dins dels 23 exercicis assignats a la u7.
- **Compilació real.** Per primera vegada es va compilar amb `lmodern` i `babel` català, els
  mateixos paquets que instal·la l'Action. Les 18 preguntes ocupen una pàgina i no hi ha cap
  *Overfull*. L'examen PAU de juny de 2026 baixat del lloc compila en 2 pàgines, i la versió
  amb solucions, en 5.
- **Repositori `pau`.** `pro-25s-q3ab` i `ana-25s-q3c` són el mateix exercici: els tres PDF
  (`-e`, `-p`, `-s`) tenen el mateix text. Hi ha 61 exercicis diferents, no 62, i en queden 56
  per importar (vegeu 7.6).
- **Programació del curs.** El full «2Bat - Unitats i feina Classroom» dona els títols de les
  unitats 1 a 6 i l'ordre real del curs, que no és el numèric (vegeu 7.4 i 7.5).
- **Repositori real (`step-quiz/exam2bat`).** Els lliuraments s'hi apliquen pujant el ZIP a
  `_uploads`, i un workflow d'extracció en fa commit. Aquest bot no pot escriure a
  `.github/workflows/`, i per això `compila.yml` no hi ha arribat mai: al Codespace, `git
  status` el mostrava com a fitxer no seguit. L'Action «Compila el banc» no s'havia executat
  mai, i els PDF del repositori són els del ZIP complet (vegeu 7.1).
- **Exàmens amb opcions, a petició del professor.** Fins aquí, l'examen era una llista de
  temes, i cada tema hi sortia com a molt un cop. Això no permetia muntar ni l'examen de la PAU
  de juny de 2026, on la 1 i la 4a són totes dues d'anàlisi: l'adreça en perdia la 4a sense
  avisar. Ara l'examen és una llista de preguntes. Un clic a un tema hi afegeix una pregunta,
  i cada targeta té ▲ ▼ per moure-la, ✕ per treure-la i «Opció de l'anterior» per convertir-la
  en una alternativa de la pregunta anterior. Les etiquetes (1, 2, 3, 4a, 4b) es deriven de
  l'ordre i surten tal qual al `.tex`: «Pregunta 4a». Les adreces antigues continuen valent.
  Després, també a petició del professor, l'estructura de la PAU (1, 2, 3, 4a, 4b) va passar a
  ser la **per defecte**, per a preguntes dels temes, de la PAU o combinades. L'estructura és
  de les places, no de les preguntes: treure o moure preguntes no desfà la 4a i la 4b.

### 2.6 Sessió 6 · Format i modalitats d'examen

El professor va detectar dos problemes en un examen muntat amb el banc:

- **El format era massa compacte.** Hi havia 7 pt entre preguntes i 5 pt entre apartats, i les
  fórmules destacades quedaven enganxades al text quan la línia d'abans era curta.
- **Les preguntes eren massa llargues.** Un examen de quatre preguntes de la u7 li costaria
  150 minuts a l'alumnat. El lloc n'estimava 56, i la PAU en dona 90 per a quatre exercicis.
  Un exercici PAU té 2 o 3 apartats, i cada apartat és **una sola tasca** d'uns 7 minuts; les
  preguntes del banc tenien apartats que eren llistes (set límits, la continuïtat en tres
  punts).

Es va fer una prova pilot (format, i una pregunta a mida PAU en les dues modalitats), el
professor la va aprovar, i es va implementar:

- **Format**, al preàmbul i per a tot el banc: `\bigskip` entre preguntes i entre apartats,
  més aire entre els subapartats d'una graella, i les fórmules destacades sempre amb el mateix
  espai. Amb el preàmbul oficial, les 19 preguntes continuen ocupant una pàgina.
- **Dues modalitats.** El banc es pensa per a l'examen d'1 h 30. La versió de 50 min la decideix
  qui escriu la pregunta: `\apartat[1,25]{0,75}` dona la puntuació de 50 min, i un bloc
  `nomesllarg` treu un apartat sencer. El build valida que totes dues puntuacions sumin 2,50,
  exigeix `minuts_curt` i compila els PDF de 50 min. Al lloc, un selector «1 h 30 / 50 min»
  canvia els punts, els minuts, els PDF i el `.tex`. Una pregunta sense versió de 50 min hi va
  sencera, amb l'etiqueta «sencera».
- **La pregunta pilot**, `limits-punt/q001`, reescrita: tres tasques (0/0, límit que no
  existeix, funció a trossos), uns 20 minuts; a 50 min, dues tasques de 1,25 punts, uns 11
  minuts. Els seus límits a l'infinit, que a més no eren del tema, són ara la segona variant
  de `limits-infinit` (`q002`), amb un apartat de paràmetre nou. El límit
  $\lim_{x\to+\infty}\frac{x^3+2x}{3^x}$ (jerarquia d'infinits) queda reservat: no és a cap
  exercici assignat (vegeu 2.1).
- **El `.tex` baixat surt net**, a petició del professor. Abans de muntar l'examen, el lloc i
  el build passen cada pregunta per `materialitza()`: a 50 min, fora els blocs `nomesllarg` i
  els punts de 50 min escrits directament; a 1 h 30, cap marca de 50 min. El que diu el `.tex`
  és exactament el que surt al PDF, i el preàmbul ja no sap res de modalitats.
- **Reescriptura de les 12 preguntes restants de la u7**, amb dos patrons per a la versió de
  50 min. En el primer, tres apartats petits (0,75 + 0,75 + 1) i a 50 min en queden dos
  d'1,25. En el segon, un apartat gran i un de petit (1,5 + 1), i a 50 min queda el gran sol,
  de 2,5 punts. Les llistes de subapartats es redueixen a 2 o 4 elements, i les funcions i les
  fraccions van en mode destacat. El que sobrava ha fet **dues preguntes noves**:
  `limits-infinit/q003` (tres límits de la q001 i un apartat nou de dos paràmetres) i
  `parametres-ab/q002` (l'apartat de paràmetres de `continuitat-trossos/q001`, que era d'aquest
  tema, i un apartat nou). La resta queda reservada (vegeu 7.4).

### 2.7 Sessió 7 · La unitat 8

- **`limits-trossos/q002`**, la segona variant que faltava a la u7: una altra funció a trossos
  amb paràmetre, amb la mateixa estructura que la q001. La u7 queda amb 17 preguntes i tots
  els temes amb dues variants, llevat dels que en tenen tres.
- **La unitat 8, sencera.** Els 16 exercicis assignats a les setmanes 5 a 7 surten de tres
  seccions del llibre, i d'aquí els **sis temes**: TVM i derivada en un punt (30, 31, 32, 37),
  funció derivada per definició (87, 88), regles de derivació (86, 92, 93), regla de la cadena
  (93, 97), recta tangent i normal (21, 40, 41, 46) i tangents amb condicions (54, 58). La
  secció de derivabilitat del llibre no té cap exercici assignat, i per això el banc no hi té
  tema.
- **Nou preguntes**, una per tema i dues per als tres temes que més surten als exàmens (regles,
  recta tangent i tangents amb condicions). Totes a mida PAU, amb versió de 50 min, i amb
  funcions semblants a les del llibre però mai les mateixes.
- **Ela geminada.** El punt volat es componia com un símbol solt i quedava separat
  («paral · lela»). El preàmbul ara l'acosta amb una mica de kerning, i això arregla també
  «anul·la» i «cancel·la» de la u7.

### 2.8 Sessió 8 · La carpeta d'exàmens

El professor ja tenia una carpeta pròpia per als exàmens, amb `main.tex`, `headers.tex`,
`defs.tex` i el logo del centre, i el seu `defs.tex` era una còpia del preàmbul del banc d'un
lliurament anterior: anava quedant enrere a cada canvi de macros. El banc s'hi ha adaptat.

- **El format del banc es parteix en dos**, com el tenia ell: `build/headers.tex` (paquets) i
  `build/defs.tex` (macros). Continuen sent la font única: els fan servir el build, el lloc i
  la seva carpeta. `build/preambul.tex` desapareix.
- **El banc no porta cap dada del centre.** El lloc és accessible, i per això ni el logo, ni el
  segell, ni el departament, ni la casella de nota hi poden ser. A `defs.tex`,
  `\capsaleraexamen` no escriu res, i els PDF del banc surten sense capçalera. La capçalera de
  debò viu en un `capsalera.tex` de la carpeta del professorat, que `main.tex` incorpora amb
  `\IfFileExists` si el troba: així surt només quan compila ell, a Overleaf. Del seu entorn,
  el banc sí que adopta `microtype` i `fancyhdr`, que no diuen res de cap centre.
- **El lloc dona `prova-N.tex`**: el cos de l'examen, sense preàmbul, amb les solucions a dins.
  Qui decideix si surten és l'interruptor `\solucionstrue` del seu `main.tex`, i per això ara
  n'hi ha prou amb un sol fitxer per a les dues versions. El número surt d'un camp al costat del
  botó.
- **Una secció «Entorn»** al lloc baixa `main.tex`, `headers.tex` i `defs.tex` sempre al dia.
- **Segell de versió.** `build.py` calcula un identificador del format i l'afegeix al
  `defs.tex` que es publica. Cada examen comença amb `\bancrequereix{...}`: si el `defs.tex`
  és d'una altra versió, LaTeX avisa al registre.
- **Les preguntes es diuen `Q1`, `Q2`, `Q4a`** al `.tex`, a petició del professor. A les
  targetes del lloc continuen dient «Pregunta 4a».
- Es manté el fitxer «tot en un», ara amb el nom `examen-sencer.tex`.

### 2.9 Sessió 9 · Tercera variant de tots els temes de la u7

Set preguntes noves, una per a cada tema que només en tenia dues: `limits-grafica/q003`,
`limits-punt/q003`, `limits-trossos/q003`, `continuitat-trossos/q003`, `parametres-ab/q003`,
`domini-discontinuitats/q003` i `bolzano-biseccio/q003`. Amb les tres que ja hi havia a
`limits-infinit`, la unitat queda amb **tres variants per tema**: se'n poden muntar tres
exàmens diferents sense repetir cap pregunta.

- Cada variant fa les mateixes tasques que les germanes, amb funcions i números diferents, i
  cap no repeteix un exercici del llibre.
- La gràfica de `limits-grafica/q003` és nova: asímptota horitzontal $y=0$ a l'esquerra, salt
  finit en $x=0$, discontinuïtat evitable en $x=2$, asímptota vertical en $x=4$ i una segona
  asímptota horitzontal $y=2$ a la dreta.
- Totes porten la versió de 50 min i compilen en una pàgina.
- Dues comprovacions de la prova de paritat suposaven que `limits-punt` tenia dues variants;
  ara en compten tres.

A més, el professor va enviar la seva carpeta d'exàmens amb dos retocs fets a mà, i el banc
els ha adoptat perquè no es perdin a la descàrrega següent:

- **`\colorgrafica`**: el color de les gràfiques passa a ser una macro de `defs.tex`, blava per
  defecte. Les tres preguntes amb gràfica i la figura de la PAU ja no escriuen cap color, i una
  comprovació de la prova de paritat vigila que cap pregunta nova no en torni a escriure. Es pot
  canviar des de la carpeta, amb `\renewcommand{\colorgrafica}{...}` al `capsalera.tex`.
- **`main.tex`** porta les dues línies de l'interruptor de solucions, una comentada, per
  commutar-les sense escriure res.

El seu `capsalera.tex` no es toca: és seu, i no és al repositori.

### 2.10 Sessió 10 · Tercera variant de tots els temes de la u8

Nou preguntes noves, fins a deixar els sis temes amb tres variants: dues per a «TVM i derivada
en un punt», dues per a «Funció derivada per definició», dues per a «Regla de la cadena» i una
per a cadascun dels altres tres.

- Les variants fan les mateixes tasques que les germanes, amb funcions i números diferents, i
  cap no repeteix un exercici del llibre.
- `tvm-derivada-punt/q003` és l'única amb context: la posició d'un objecte, amb velocitat
  mitjana i velocitat instantània. Serveix per si es vol una pregunta més aplicada.
- `recta-tangent/q003` treballa la tangent a una exponencial i una tangent de pendent donat amb
  paràmetre, que és el que demana l'exercici 45 del llibre.
- Tots els resultats, comprovats amb SymPy a més del càlcul escrit a la solució.

### 2.11 Sessió 11 · La unitat 9

Els 16 exercicis assignats a les setmanes 8 a 10 surten de tres seccions del llibre, i d'aquí
els **quatre temes**: monotonia i extrems relatius, extrems amb paràmetres i gràfiques,
curvatura i punts d'inflexió, i optimització. Les seccions de teoremes i de la regla de
l'Hôpital no tenen cap exercici assignat, i per tant el banc no hi té tema, igual que amb la
derivabilitat de la u8.

- **Vuit preguntes**, dues per tema. Falta la tercera variant de cadascun.
- `extrems-parametres/q002` treballa una capacitat que la PAU demana sovint: llegir els extrems
  de $f$ a la **gràfica de $f'$**. Porta una figura nova.
- Les dues d'optimització segueixen el patró de la PAU: plantejar la funció, trobar-ne l'extrem
  i **justificar-lo**. Una és geomètrica (rectangle sota una paràbola) i l'altra, de context
  (capsa sense tapa).
- Tots els resultats, comprovats amb SymPy a més del càlcul escrit a la solució.

### 2.12 Sessió 12 · Tercera variant de la u9

Quatre preguntes, una per tema, amb casos que les altres dues variants no tocaven:

- `monotonia-extrems/q003`: $f(x)=x^4-4x^3$ té un punt crític en $x=0$ que **no és extrem**,
  perquè la derivada s'hi anul·la sense canviar de signe. A més, el criteri de la derivada
  segona hi falla ($f''(0)=0$) i cal tornar al signe de $f'$.
- `extrems-parametres/q003`: dos paràmetres alhora, a partir d'un punt i d'un extrem, i un
  raonament sobre si una cúbica pot tenir exactament un extrem (no pot).
- `curvatura-inflexio/q003`: una cúbica, un logaritme i el fet que tota funció polinòmica de
  grau 3 té exactament un punt d'inflexió.
- `optimitzacio/q003`: un prat amb un costat al riu, que és el problema d'optimització més
  clàssic i el més senzill dels tres.

### 2.13 Sessió 13 · La unitat 10

Els 16 exercicis assignats a les setmanes 11, 12 i 17 donen **cinc temes**: domini i punts de
tall, asímptotes i branques infinites, i l'estudi complet de tres famílies de funcions
(racional, polinòmica i a trossos). La secció de simetries i periodicitat no té cap exercici
assignat, i per tant el banc no hi té tema.

- **Cinc preguntes**, una per tema: ja permeten muntar un examen sencer de la unitat. En
  falten dues variants de cadascun.
- Les tres preguntes d'estudi complet porten **la gràfica dibuixada a la solució**, i per això
  el full del professorat serveix de model del que ha de sortir a l'alumnat.
- El repartiment d'apartats hi és important: a la versió de 50 min es treu la curvatura, però
  mai el dibuix. Un examen curt de representació sense gràfica no tindria sentit.
- `estudi-racional/q001` és la més difícil del banc fins ara (●●●): asímptota obliqua, dues
  branques i un extrem a cada costat.

---

## 3. Decisions preses

| Decisió | Origen | Per què |
|---|---|---|
| PDF compilats per GitHub Actions | Professor | El navegador no compila LaTeX; és gratuït |
| Pregunta de 2,5 punts, apartats múltiples de 0,25 | Professor | 4 preguntes = 10 punts; coincideix exactament amb la PAU |
| Exàmens sense capçalera | Professor | Preferència del professor |
| Repositori privat | Proposta acceptada | Conté solucions; en públic, GitHub Pages les exposaria |
| Solucions dins de cada pregunta (`\ifsolucions`) | Disseny | Dues versions a partir d'un sol font |
| Plantilla d'assemblatge única per a Python i JS | Disseny | El `.tex` baixat i el compilat no poden divergir |
| Catàleg amb el LaTeX incrustat | Disseny | El lloc funciona obert com a fitxer, sense servidor |
| L'adreça guarda codis estables, no posicions | Disseny | Les seleccions desades no es poden trencar |
| Secció PAU per blocs | Professor | No es pot fer cap PAU sencera al final de la u7, i no calen encara els temes de les altres unitats |
| Juny de 2023 = sèries 1 i 5 | Professor | Dada confirmada amb els originals |
| Enunciats PAU literals (vosaltres) | Disseny, **revisable** | Fidelitat a l'examen real |
| Solució PAU = criteri oficial + pauta | Disseny | Autoritat i utilitat per corregir; les errades es corregeixen amb nota |
| Apartats PAU numerats a), b), c) | Disseny | Coherència dins d'un examen muntat |
| Primer la u8, després la PAU | Professor | La u8 acaba l'1 de novembre; la PAU no té data |
| El filtre PAU segueix l'ordre real del curs | Proposta acceptada | El curs fa u7–u10, u13, u14, u1–u6, u11 i u12: l'ordre numèric enganyaria |
| La u4 (Vectors a l'espai) es fa dins de la u5 | Professor | Manera habitual de programar-la |
| Lliurament per canvis, a partir de l'estat del repositori | Proposta acceptada | Substituir el repositori per un ZIP pot desfer canvis fets entre sessions |
| Els PDF i el catàleg només els desa l'Action | Disseny | Si també se'n fa commit en local, xoquen amb el commit del bot |
| `--preambul` només canvia la compilació | Disseny | El catàleg ha de portar sempre el preàmbul oficial |
| L'examen és una llista de preguntes; un tema hi pot sortir més d'un cop | Professor | Un examen com el de la PAU té dues preguntes d'anàlisi (1 i 4a) |
| Per defecte, l'estructura de la PAU: 1, 2, 3, 4a, 4b | Professor | L'alumnat fa la 1, la 2 i la 3 i tria entre la 4a i la 4b; val per a temes, PAU i exàmens combinats |
| L'estructura és de les places, no de les preguntes | Disseny | Treure o moure preguntes no desfà la 4a i la 4b |
| «Opció de l'anterior» canvia l'estructura d'una plaça; els números es deriven de l'estructura | Disseny | Mai hi pot haver números repetits ni forats |
| Cada pregunta, a mida d'un exercici PAU: 2 o 3 apartats d'una sola tasca, uns 20 minuts | Professor | Un examen d'1 h 30 són quatre preguntes, com la PAU |
| Dues modalitats, 1 h 30 i 50 min; el banc es pensa per a la d'1 h 30 | Professor | Els exàmens de classe són d'una d'aquestes dues durades |
| La versió de 50 min la decideix qui escriu la pregunta (`\apartat[..]{..}` i `nomesllarg`) | Proposta acceptada | Els punts s'han de repartir a mà en múltiples de 0,25, i un apartat sovint depèn de l'anterior |
| Les preguntes PAU també poden entrar a l'examen de 50 min | Professor | Amb una versió de 50 min feta a mà, o senceres |
| Format: `\bigskip` entre preguntes i apartats; fórmules destacades amb el mateix aire | Professor | Els exàmens eren difícils de llegir |
| El `.tex` baixat surt net: el que diu és el que surt al PDF | Professor | Per poder-lo editar abans de compilar-lo |
| Dos patrons de versió de 50 min: dos apartats d'1,25, o un de sol de 2,5 | Disseny | Els punts queden rodons i cada versió és una tasca coherent |
| La u8 no té tema de derivabilitat | Disseny | Cap exercici assignat d'aquella secció; el banc no surt mai dels exercicis assignats |
| La u9 no té tema de teoremes ni de la regla de l'Hôpital | Disseny | Mateix criteri: no hi ha cap exercici assignat d'aquestes seccions |
| A la u10, la versió de 50 min treu la curvatura, mai la gràfica | Disseny | Una pregunta de representació sense dibuix no té sentit |
| Dues variants per als temes de la u8 que més surten als exàmens | Disseny | Regles de derivació, recta tangent i tangents amb condicions |
| El lloc dona el cos de l'examen (`prova-N.tex`), no un fitxer sencer | Professor | La capçalera, el logo i el curs viuen a la seva carpeta |
| Les preguntes es diuen `Q1`, `Q2`, `Q4a` al `.tex` | Professor | Més curt al full de l'examen |
| El format del banc es parteix en `headers.tex` i `defs.tex` | Proposta acceptada | És la partició que ja feia servir el professor, i continua sent font única |
| El `defs.tex` publicat porta un segell de versió | Disseny | Un `defs.tex` desfasat avisava en silenci, o fallava de qualsevol manera |
| Cap dada del centre al banc: logo, segell, departament i casella de nota viuen a `capsalera.tex`, fora del repositori | Professor | El lloc és accessible i no ha de mostrar res de l'institut |
| El color de les gràfiques és `\colorgrafica`, blau, i cap pregunta no n'escriu cap | Professor | Es canvia en un sol lloc, i des de la carpeta d'exàmens |
| Les opcions compten una vegada als punts; dels minuts, la més llarga | Disseny | L'alumne en respon una |

---

## 4. Errors trobats i corregits

| Error | On | Correcció |
|---|---|---|
| `\text{si } -1` espaia el menys com a binari | Examen original | Macro `\si{…}` |
| Graella TikZ desquadrada (passos d'1 cm absolut) | Original i `limits-grafica/q001` | `step=1` i **regla 8** al validador |
| `replace` de JS interpretava `$$`, `$'` i `$&` | `app.js` | Substituts en forma de funció |
| La numeració de les targetes no coincidia amb la del `.tex` si hi havia un tema buit | `app.js` | Numeració només de temes amb preguntes |
| L'adreça guardava posicions | `app.js` | Codis estables (`tema:q002`) |
| Text del catàleg sense escapar dins de l'HTML | `app.js` | `esc()` |
| Botons il·legibles en mode fosc | `style.css` | Token `--sobre-acc` |
| «4 preguntas» (castellà) | `app.js` | «preguntes» |
| La barra inferior partia «10,00 / punts» al mòbil | `style.css` | Talls només als separadors |
| El build petava amb avisos amb accents (sortida T1 de `pdflatex`) | `build.py` | Descodificació tolerant |
| `--pregunta` generava un catàleg mutilat | `build.py` | Només limita la compilació |
| La prova de paritat depenia que un tema real fos buit | `prova_paritat.py` | Tema buit sintètic |
| Fórmules llargues en línia desbordaven | 2 preguntes | Passades a mode destacat |
| $D(4{,}5)=6{,}85$ en lloc de 6,875 | **Criteri oficial** PAU 2026 | Valor correcte i *Nota del banc* |
| `--preambul` escrivia el preàmbul de prova al catàleg, i els `.tex` baixats en sortien sense `babel` | `build.py` | El catàleg porta sempre `build/preambul.tex`, i el build avisa que aquells PDF no són definitius |
| Un build fallit deixava a `out/` els PDF que ja havia compilat | `build.py` | Es compila en una carpeta temporal i es copia a `out/` només si no hi ha cap error |
| Una adreça amb un `%` solt, o amb `#__proto__` o `#constructor`, deixava la pàgina en blanc | `app.js` | Descodificació tolerant i `PER_TEMA` sense prototip |
| El push del bot era rebutjat si la branca avançava durant el build | `compila.yml` | `git pull --rebase` i fins a tres intents |
| La prova «una pregunta del banc no porta cap línia de procedència» no comprovava res: tallava el `.tex` per un comentari del preàmbul que cita `\begin{document}` | `prova_paritat.py` | Es talla per la línia exacta `\begin{document}` |

---

## 5. Què està verificat i què no

**Verificat:**

- Les respostes de les 13 preguntes de la u7, amb càlcul simbòlic i un segon mètode per a
  tots els límits a l'infinit.
- 32 resultats dels criteris oficials de juny de 2026, per un mètode independent.
- `prova_validacio.py`: 29 avaries provocades, cadascuna rebutjada pel build. Les 8 de la
  sessió 6 són de les modalitats.
- `prova_sortida.py`: 9 comprovacions, sense TeX (un `pdflatex` fals al PATH). Un build que
  falla, per validació o per compilació, no toca cap fitxer. Un de correcte els escriu tots,
  `--pregunta` només escriu els de la pregunta indicada i `--preambul` no arriba al catàleg.
  També s'ha confirmat amb el `pdflatex` real.
- `prova_paritat.py`: 53 comprovacions. El lloc (executant l'`app.js` real) i el build
  munten el mateix `.tex`, byte a byte, també amb preguntes PAU, amb la procedència al lloc
  exacte i amb opcions (1, 2, 3, 4a, 4b). Tres adreces mal formades s'ignoren sense que la
  pàgina peti. Les accions de les targetes (afegir, moure, treure, marcar opció, canviar de
  variant) donen les etiquetes, els punts i l'adreça esperats. Cinc clics donen per defecte
  1, 2, 3, 4a i 4b, també en un examen que combina temes i PAU. A 50 min, el lloc i el build
  munten el mateix `.tex`, i els minuts i l'adreça segueixen la modalitat.
- En un Chromium real: selecció, variants, adreça, recàrrega, descàrregues, secció PAU,
  adreces mal formades i l'examen de la PAU de 2026 muntat amb clics (1, 2, 3, 4a, 4b), també
  a 390 px d'amplada. El seu `main.tex` compila en 2 pàgines, i el de solucions en 5, sense cap
  *Overfull*. També un examen combinat (Límits en un punt, Anàlisi, Bolzano, Probabilitat i
  Geometria), amb ✕ i ▲ entremig: 2 pàgines i 4 amb solucions, sense cap *Overfull*.
- Sessió 13: les 64 preguntes compilen en les dues modalitats (246 PDF, tots d'una pàgina).
  Els estudis de la u10, verificats amb SymPy, i les tres gràfiques de les solucions,
  revisades sobre el PDF compilat: asímptotes, extrems i talls hi coincideixen amb l'estudi.
- Sessió 12: les 59 preguntes compilen en les dues modalitats (226 PDF, tots d'una pàgina), i
  els resultats de les quatre variants noves estan verificats amb SymPy.
- Sessió 11: les 55 preguntes compilen amb el preàmbul oficial en les dues modalitats (210 PDF,
  tots d'una pàgina). Els resultats de la u9, verificats amb SymPy, i les dues figures noves,
  revisades sobre el PDF compilat.
- Sessió 10: les 47 preguntes compilen amb el preàmbul oficial en les dues modalitats (178 PDF,
  tots d'una pàgina), i les 32 derivades i límits nous de la u8 estan verificats amb SymPy.
- Sessió 9: les 38 preguntes compilen amb el preàmbul oficial en les dues modalitats (142 PDF,
  tots d'una pàgina). Els resultats de les set variants noves, comprovats amb SymPy a més del
  càlcul de la solució, i la gràfica nova, revisada sobre el PDF compilat.
- Sessió 8: la carpeta d'exàmens sencera, muntada amb els fitxers que dona el lloc i el logo
  del professor: compila en 3 pàgines sense solucions i en 4 amb solucions, sense cap
  *Overfull*. Amb un `defs.tex` d'una altra versió, LaTeX escriu l'avís al registre. Sense
  `capsalera.tex`, la carpeta compila igualment i els exàmens surten sense capçalera; amb el
  fitxer, la capçalera hi surt. Cap PDF del banc no en porta, i dues comprovacions de la prova
  de paritat vigilen que ni els fitxers de format ni el catàleg tinguin dades del centre.
- Sessió 7: les 31 preguntes compilen amb el preàmbul oficial en les dues modalitats (114 PDF,
  tots els enunciats d'una pàgina). Cada resultat nou de la u8, comprovat amb SymPy a més del
  càlcul de la solució. Un examen de mostra de la u8 fa uns 68 minuts dels 90 a la modalitat
  llarga, i uns 42 dels 50 a la curta.
- Sessió 6: el build real amb el preàmbul oficial i el format nou: 21 preguntes i 74 PDF, tots
  els enunciats d'una pàgina, també els de 50 min. En Chromium, el selector de durada. L'examen
  de cinc preguntes de la u7 fa 15 apartats i uns 72 minuts a 1 h 30, i 10 apartats i uns 44
  minuts a 50 min. Els `.tex` baixats no porten cap marca de l'altra modalitat i compilen.
- La compilació amb el preàmbul oficial, amb `lmodern` i `babel` català (sessió 5). Les 18
  preguntes ocupen una pàgina, sense cap *Overfull*. El `main.tex` baixat de l'examen de 2026
  compila en 2 pàgines, i el de solucions, en 5.
- El pas de desar de l'Action, simulat amb un remot local i un clon superficial en quatre
  casos. Sense canvis, no fa res. En un push normal, desa. Si la branca ha avançat, incorpora el
  commit nou i desa. Si hi ha un conflicte, falla sense desar res.

**No verificat en aquest entorn:**

- El visor de PDF incrustat, perquè el navegador sense pantalla no en té. Si un navegador no
  el mostra, cada targeta té un enllaç per obrir el PDF en una pestanya.

---

## 6. Inventari

### 6.1 Unitat 7 · Límits i continuïtat (24 preguntes)

Tres variants per tema: se'n poden muntar tres exàmens diferents. Totes a mida PAU, amb la
versió de 50 min. Els minuts són estimacions (1 h 30 · 50 min) i s'han de calibrar amb dades
reals (vegeu 7.4).

| Tema | Codi | Títol | 1 h 30 | 50 min | Minuts | Dif. | Llibre |
|---|---|---|---|---|---|---|---|
| Bolzano i bisecció | `q001` | Teorema de Bolzano, bisecció i punt de tall de dues corbes | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 112, 113, 114, 120 |
| Bolzano i bisecció | `q002` | Bolzano per assolir un valor, arrel amb error menor que una dècima i punt de tall | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 20 · 10 | ●●○ | 43, 113, 114, 120 |
| Bolzano i bisecció | `q003` | Bolzano i bisecció en una cúbica, i tall entre un logaritme i una recta | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 112, 113, 114, 120 |
| Continuïtat de funcions a trossos | `q001` | Continuïtat d'una funció a trossos amb exponencial i racional, punt per punt | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 16 · 11 | ●●○ | 103 |
| Continuïtat de funcions a trossos | `q002` | Continuïtat d'una funció a trossos amb logaritme i d'una funció amb valor absolut | 1,25 + 1,25 | 2,50 | 20 · 11 | ●●● | 93, 102 |
| Continuïtat de funcions a trossos | `q003` | Continuïtat d'una funció a trossos amb exponencial i racional: tres punts | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 16 · 11 | ●●○ | 103 |
| Domini i discontinuïtats | `q001` | Domini, classificació de discontinuïtats i construcció d'una racional | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 47, 93, 94 |
| Domini i discontinuïtats | `q002` | Dominis amb radical i logaritme, discontinuïtats d'una racional amb Ruffini i funció inventada | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 47, 93, 94 |
| Domini i discontinuïtats | `q003` | Domini i continuïtat d'arrels i logaritmes, i discontinuïtats d'una funció racional | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 47, 93, 94 |
| Límits a partir d'una gràfica | `q001` | Límits i continuïtat llegits sobre una gràfica | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 16 · 10 | ●○○ | 44, 66, 68, 92 |
| Límits a partir d'una gràfica | `q002` | Límits i continuïtat sobre una gràfica amb un angle, un forat i una asímptota | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 44, 66, 68, 92 |
| Límits a partir d'una gràfica | `q003` | Límits i continuïtat a partir d'una gràfica amb dues asímptotes horitzontals | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 44, 66, 68, 92 |
| Límits de funcions a trossos | `q001` | Límits d'una funció a trossos amb paràmetre i indeterminació 0/0 | 0,75 + 1,25 + 0,50 | 1,00 + 1,50 | 18 · 12 | ●●○ | 76, 88, 90 |
| Límits de funcions a trossos | `q002` | Límits d'una funció a trossos amb un paràmetre: 0/0, laterals i infinit | 0,75 + 1,25 + 0,50 | 1,00 + 1,50 | 18 · 12 | ●●○ | 76, 88, 90 |
| Límits de funcions a trossos | `q003` | Límits d'una funció a trossos amb paràmetre: 0/0, laterals en el tall i infinit | 0,75 + 1,25 + 0,50 | 1,00 + 1,50 | 18 · 12 | ●●○ | 76, 88, 90 |
| Límits en l'infinit | `q001` | Límits en l'infinit: racionals, exponencials i un paràmetre | 0,75 + 0,75 + 1,00 | 1,25 + 1,25 | 16 · 10 | ●●○ | 45, 46, 48 |
| Límits en l'infinit | `q002` | Límits en l'infinit de funcions racionals i un paràmetre | 0,75 + 0,75 + 1,00 | 1,25 + 1,25 | 16 · 10 | ●●○ | 46, 48 |
| Límits en l'infinit | `q003` | Límits en l'infinit: mateix grau, radicals i dos paràmetres | 0,75 + 0,75 + 1,00 | 1,25 + 1,25 | 16 · 10 | ●●○ | 45, 46, 48 |
| Límits en un punt | `q001` | Límits en un punt: indeterminació 0/0, límits laterals i funció a trossos | 0,75 + 0,75 + 1,00 | 1,25 + 1,25 | 20 · 11 | ●●○ | 76, 88, 90 |
| Límits en un punt | `q002` | Límits en un punt: 0/0 amb Ruffini i límits infinits amb laterals | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 70, 76 |
| Límits en un punt | `q003` | Límits en un punt: 0/0 amb Ruffini i una funció a trossos | 0,75 + 0,75 + 1,00 | 1,25 + 1,25 | 18 · 11 | ●●○ | 70, 76, 88 |
| Paràmetres per a la continuïtat | `q001` | Paràmetres de continuïtat amb exponencial i logaritme, i un paràmetre amb dues solucions | 1,50 + 1,00 | 2,50 | 20 · 12 | ●●○ | 40, 102, 106 |
| Paràmetres per a la continuïtat | `q002` | Paràmetres de continuïtat en una funció a tres trossos i en una de dos | 1,50 + 1,00 | 2,50 | 18 · 11 | ●●○ | 40, 106 |
| Paràmetres per a la continuïtat | `q003` | Paràmetres de continuïtat: un sistema de dues equacions i un cas amb dues solucions | 1,50 + 1,00 | 2,50 | 20 · 12 | ●●○ | 40, 102, 106 |

### 6.2 Unitat 8 · Derivades (18 preguntes)

Sis temes, de les tres seccions del llibre amb exercicis assignats a les setmanes 5 a 7, amb
tres variants cadascun. La secció de derivabilitat no en té cap d'assignat, i per això el banc
no hi té tema.

| Tema | Codi | Títol | 1 h 30 | 50 min | Minuts | Dif. | Llibre |
|---|---|---|---|---|---|---|---|
| Funció derivada per definició | `q001` | Funció derivada per definició: un polinomi, una arrel i una racional | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 87, 88 |
| Funció derivada per definició | `q002` | Funció derivada per definició: polinomi, arrel decreixent i racional | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 87, 88 |
| Funció derivada per definició | `q003` | Funció derivada per definició: cub, racional i arrel | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 87, 88 |
| Recta tangent i normal | `q001` | Rectes tangent i normal, i una tangent amb un paràmetre | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 16 · 10 | ●○○ | 40, 41 |
| Recta tangent i normal | `q002` | Rectes tangent i normal en el tall amb l'eix d'abscisses, i tangent a x ln x | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 21, 46 |
| Recta tangent i normal | `q003` | Rectes tangent i normal a una exponencial, i una tangent de pendent donat | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 40, 41, 45 |
| Regla de la cadena | `q001` | Regla de la cadena: potències, exponencials, logaritmes i trigonomètriques | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 93, 97 |
| Regla de la cadena | `q002` | Regla de la cadena: potències, exponencials, logaritmes i arrels | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 93, 97 |
| Regla de la cadena | `q003` | Regla de la cadena: potències, exponencials de base 2, logaritmes i arrels | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 93, 97 |
| Regles de derivació | `q001` | Regles de derivació: sumes, productes i quocients | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 16 · 10 | ●○○ | 86, 92, 93 |
| Regles de derivació | `q002` | Regles de derivació: arrels, exponencials, logaritmes, productes i quocients | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 16 · 10 | ●○○ | 86, 92, 93 |
| Regles de derivació | `q003` | Regles de derivació: potències, arrels, logaritmes, productes i quocients | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 16 · 10 | ●○○ | 86, 92, 93 |
| TVM i derivada en un punt | `q001` | Taxa de variació mitjana i derivada en un punt per definició | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●○○ | 30, 32, 37 |
| TVM i derivada en un punt | `q002` | TVM i derivada en un punt d'una funció racional | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 31, 32, 37 |
| TVM i derivada en un punt | `q003` | Velocitat mitjana i velocitat instantània per definició | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●○○ | 30, 31, 37 |
| Tangents amb condicions | `q001` | Tangents paral·leles a una recta donada i tangents horitzontals | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 54 |
| Tangents amb condicions | `q002` | Tangent a una racional, triangle amb els eixos i tangents paral·leles | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 54, 58 |
| Tangents amb condicions | `q003` | Tangents horitzontals i tangents paral·leles a rectes donades | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 54 |

### 6.3 Unitat 9 · Aplicacions de les derivades (12 preguntes)

Quatre temes, de les tres seccions del llibre amb exercicis assignats a les setmanes 8 a 10:
creixement i extrems (39, 41, 42, 44, 50, 51, 58), concavitat (66, 67, 70) i optimització (77,
79, 86, 87). Les seccions de teoremes i de la regla de l'Hôpital no en tenen cap d'assignat, i
per això el banc no hi té tema. Tres variants per tema.

| Tema | Codi | Títol | 1 h 30 | 50 min | Minuts | Dif. | Llibre |
|---|---|---|---|---|---|---|---|
| Curvatura i punts d'inflexió | `q001` | Curvatura i punts d'inflexió d'un polinomi de grau 4 i d'una exponencial | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 66, 67 |
| Curvatura i punts d'inflexió | `q002` | Coeficients d'una cúbica a partir d'un punt, una inflexió i un extrem | 1,50 + 1,00 | 2,50 | 20 · 12 | ●●○ | 70 |
| Curvatura i punts d'inflexió | `q003` | Curvatura d'una cúbica i d'un logaritme, i el punt d'inflexió del grau 3 | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 66, 67 |
| Extrems amb paràmetres i gràfiques | `q001` | Paràmetre a partir d'un extrem, una funció inventada i el nombre màxim d'extrems | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 39, 44, 58 |
| Extrems amb paràmetres i gràfiques | `q002` | Extrems llegits a la gràfica de la derivada | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 39, 41 |
| Extrems amb paràmetres i gràfiques | `q003` | Dos paràmetres a partir d'un extrem, una funció inventada i un raonament sobre el grau | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●●○ | 39, 44, 58 |
| Monotonia i extrems relatius | `q001` | Monotonia i extrems d'una cúbica, amb la derivada segona | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 42, 50, 51 |
| Monotonia i extrems relatius | `q002` | Monotonia i extrems d'una funció racional, i extrems en un interval tancat | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 42, 50, 51 |
| Monotonia i extrems relatius | `q003` | Monotonia amb un punt crític que no és extrem, i el criteri de la derivada segona | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 42, 50, 51 |
| Optimització | `q001` | Optimització: rectangle inscrit sota una paràbola | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 86, 87 |
| Optimització | `q002` | Optimització: capsa sense tapa a partir d'un cartró quadrat | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 77, 79 |
| Optimització | `q003` | Optimització: prat rectangular amb un costat al riu | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●○○ | 77, 86 |

### 6.4 Unitat 10 · Representació de funcions (5 preguntes)

Cinc temes, de les cinc seccions del llibre amb exercicis assignats a les setmanes 11, 12 i 17:
domini i recorregut (43, 45, 100), asímptotes (62, 63, 38), representació (41, 84, 88, 91),
funcions a trossos (108, 37) i els problemes de context (123, 124). La secció de simetries i
periodicitat no en té cap d'assignat, i per això el banc no hi té tema. Una variant per tema;
en falten dues (vegeu 7.4).

| Tema | Codi | Títol | 1 h 30 | 50 min | Minuts | Dif. | Llibre |
|---|---|---|---|---|---|---|---|
| Asímptotes i branques infinites | `q001` | Asímptotes de funcions racionals i gràfica a partir d'unes asímptotes donades | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 62, 63, 38 |
| Domini i punts de tall | `q001` | Domini de racionals, radicals i logaritmes, i punts de tall | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●○○ | 43, 45, 100 |
| Estudi i gràfica d'una funció a trossos | `q001` | Estudi i gràfica d'una funció a trossos amb asímptota horitzontal | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 108, 37 |
| Estudi i gràfica d'una funció polinòmica | `q001` | Estudi i gràfica de x³−3x²+4: talls amb arrel doble, extrems i inflexió | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 75, 78, 84, 88 |
| Estudi i gràfica d'una funció racional | `q001` | Estudi i gràfica de x²/(x−1): asímptota obliqua, extrems i curvatura | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 22 · 13 | ●●● | 41, 63, 75, 91 |

### 6.5 Registre de convocatòries PAU

| Codi | Convocatòria | Sèrie | Font |
|---|---|---|---|
| `23j` | juny 2023 | 1 | Confirmat pel professor: el juny de 2023 es van publicar les sèries 1 i 5, per aquest ordre. |
| `23j2` | juny 2023 | 5 | Confirmat pel professor; coincideix amb el catàleg del repositori pau. |
| `23s` | setembre 2023 | 2 | examenselectivitat.cat (Matemàtiques 2023, setembre, sèrie 2). El tall del criteri oficial no conserva la capçalera. |
| `24i` | juny 2024 | 5 | Capçalera del criteri oficial: ana-24i-q1-s.pdf. |
| `24j` | juny 2024 | 1 | examenselectivitat.cat: juny 2024 = sèries 1 i 5; la 5 és la 24i. El tall del criteri oficial no conserva la capçalera. |
| `24s` | setembre 2024 | 3 | Capçalera del criteri oficial: ana-24s-q1-s.pdf. |
| `25i` | juny 2025 | 4 | Capçalera del criteri oficial: ana-25i-q1-s.pdf. |
| `25j` | juny 2025 | 1 | Capçalera del criteri oficial: ana-25j-q1-s.pdf. |
| `25s` | setembre 2025 | 3 | Capçalera del criteri oficial: ana-25s-q1-s.pdf. |
| `26j` | juny 2026 | 1 | Capçalera del criteri oficial: ana-26j-q1-s.pdf. |
| `26j2` | juny 2026 | 5 | Capçalera del criteri oficial: ana-26j2-q1-s.pdf. |

### 6.6 Seguiment de les 62 entrades PAU (61 exercicis)

Ordenades de la més recent a la més antiga, que és l'ordre d'importació recomanat.

| Codi | Convocatòria | Bloc | Títol (catàleg del repositori `pau`) | Estat |
|---|---|---|---|---|
| `ana-26j2-q1` | juny 2026 · s5 | Anàlisi | Paràbola i hipèrbola: punts de tall i àrea entre corbes | pendent |
| `alg-26j2-q2` | juny 2026 · s5 | Àlgebra | Matrius M, N: invertibilitat de MN i NM | pendent |
| `pro-26j2-q3` | juny 2026 · s5 | Probabilitat | Lectura i esport: prob. total, Bayes i extrems de f(x) | pendent |
| `ana-26j2-q4a` | juny 2026 · s5 | Anàlisi | f(x) a partir de la gràfica de f'(x): tangent, extrems, àrea | pendent |
| `geo-26j2-q4b` | juny 2026 · s5 | Geometria | Braç robòtic: distància, pla i punt de xoc | pendent |
| `ana-26j-q1` | juny 2026 · s1 | Anàlisi | Funció a trossos amb exponencial i paràbola: continuïtat i àrea | ✅ importada |
| `alg-26j-q2` | juny 2026 · s1 | Àlgebra | Sistema de tres plans amb paràmetre m | ✅ importada |
| `pro-26j-q3` | juny 2026 · s1 | Probabilitat | Entrades de concert: sorteig i web; Bolzano amb decibels | ✅ importada |
| `ana-26j-q4a` | juny 2026 · s1 | Anàlisi | Optimització: barana circular i quadrada de 10 m | ✅ importada |
| `geo-26j-q4b` | juny 2026 · s1 | Geometria | Pla PQR, àrea del triangle i tetraedre de volum 1 | ✅ importada |
| `ana-25j-q1` | juny 2025 · s1 | Anàlisi | f(x)=(x²−2x)/(x−1): asímptotes, tangents, pendent | pendent |
| `alg-25j-q2` | juny 2025 · s1 | Àlgebra | Sistema lineal amb paràmetre p | pendent |
| `pro-25j-q3` | juny 2025 · s1 | Probabilitat | Peces ferro/acer: prob. total, binomial i màxim f(p) | pendent |
| `ana-25j-q4a` | juny 2025 · s1 | Anàlisi | Vela semiparabòlica: cost del material | pendent |
| `geo-25j-q4b` | juny 2025 · s1 | Geometria | Pla perpendicular a x+y=0 i recta mediadora | pendent |
| `ana-25s-q1` | setembre 2025 · s3 | Anàlisi | Optimització: terreny triangular A(m) mínim | pendent |
| `alg-25s-q2` | setembre 2025 · s3 | Àlgebra | Sistema lineal amb paràmetre m | pendent |
| `pro-25s-q3ab` | setembre 2025 · s3 | Probabilitat | Sesamoïditis: probabilitat total i Bayes | pendent · **mateix exercici que `ana-25s-q3c`** (7.6) |
| `ana-25s-q3c` | setembre 2025 · s3 | Anàlisi | Trobar a, b, c de f(x)=ax³+bx²+cx per condicions | pendent · **mateix exercici que `pro-25s-q3ab`** (7.6) |
| `ana-25s-q4a` | setembre 2025 · s3 | Anàlisi | Vitrall Sagrada Família: sin(x/4) i cos(x/4) | pendent |
| `geo-25s-q4b` | setembre 2025 · s3 | Geometria | Plans paral·lels a 2x−y+z=5 i distàncies | pendent |
| `ana-25i-q1` | juny 2025 · s4 | Anàlisi | f(x)=√(1+x³): domini, derivada, tangent | pendent |
| `alg-25i-q2` | juny 2025 · s4 | Àlgebra | Sistema amb plans π₁,π₂,π₃ (paràmetre a) | pendent |
| `pro-25i-q3` | juny 2025 · s4 | Probabilitat | Filtre de correu brossa: prob. total, Bayes i integral | pendent |
| `ana-25i-q4a` | juny 2025 · s4 | Anàlisi | Optimització: ampolla cilindre + mitja esfera | pendent |
| `alg-25i-q4b` | juny 2025 · s4 | Àlgebra | Matrius que commuten; invertibilitat; A⁻¹=A | pendent |
| `ana-24s-q1` | setembre 2024 · s3 | Anàlisi | f(x)=3x¹³+5x³+2: Bolzano i monotonia | pendent |
| `alg-24s-q2` | setembre 2024 · s3 | Àlgebra | Sistema lineal amb paràmetre m | pendent |
| `ana-24s-q3` | setembre 2024 · s3 | Anàlisi | Àrees del logotip: cúbica i paràbola | pendent |
| `pro-24s-q4` | setembre 2024 · s3 | Probabilitat | Arrítmia i monitor Holter: prob. total i Bayes | pendent |
| `ana-24s-q5` | setembre 2024 · s3 | Anàlisi | Rectangle inscrit en y=e^(−2x): àrea màxima i tangent | pendent |
| `geo-24s-q6` | setembre 2024 · s3 | Geometria | Recta perpendicular a un pla i plans paral·lels | pendent |
| `ana-24j-q1` | juny 2024 · s1 | Anàlisi | f(x)=2·ln(x)/x: extrems, asímptotes, tangent | pendent |
| `alg-24j-q2` | juny 2024 · s1 | Àlgebra | Sistema lineal amb paràmetre k | pendent |
| `ana-24j-q3` | juny 2024 · s1 | Anàlisi | Àrea d'un terreny: cúbica i recta PR | pendent |
| `pro-24j-q4` | juny 2024 · s1 | Probabilitat | Boles B,A,Y,E,S,F,A,N,S: sense i amb reemplaçament | pendent |
| `ana-24j-q5` | juny 2024 · s1 | Anàlisi | Optimització: cobert de fusta adossat a una paret | pendent |
| `geo-24j-q6` | juny 2024 · s1 | Geometria | Pla mediador i triangle isòsceles | pendent |
| `ana-24i-q1` | juny 2024 · s5 | Anàlisi | f(x)=−2+10(x−1)·ln(x): Bolzano, monotonia, límits | pendent |
| `alg-24i-q2` | juny 2024 · s5 | Àlgebra | Matriu invertible i equació matricial PX+Q=2R | pendent |
| `ana-24i-q3` | juny 2024 · s5 | Anàlisi | Paràboles f_a: tangent i àrea entre corbes | pendent |
| `pro-24i-q4` | juny 2024 · s5 | Probabilitat | La Rut i els problemes: prob. total, Bayes, binomial | pendent |
| `ana-24i-q5` | juny 2024 · s5 | Anàlisi | Optimització: decorat rectangle + semicercles | pendent |
| `geo-24i-q6` | juny 2024 · s5 | Geometria | Posició relativa de rectes i perpendicular comuna | pendent |
| `alg-23s-q1` | setembre 2023 · s2 | Àlgebra | Matriu inversa via (A−2I)²=3I | pendent |
| `ana-23s-q2` | setembre 2023 · s2 | Anàlisi | f(x)=1/x: tangent i triangle d'àrea constant | pendent |
| `alg-23s-q3` | setembre 2023 · s2 | Àlgebra | Sistema lineal amb paràmetre m | pendent |
| `ana-23s-q4` | setembre 2023 · s2 | Anàlisi | Bolzano i àrea entre f(x) i h(x) | pendent |
| `geo-23s-q5` | setembre 2023 · s2 | Geometria | Perpendicular comuna de dues rectes i distància | pendent |
| `ana-23s-q6` | setembre 2023 · s2 | Anàlisi | Optimització: trapezi isòsceles d'àrea màxima | pendent |
| `ana-23j2-q1` | juny 2023 · s5 | Anàlisi | Àrea de la regió delimitada per f(x)=−x²+x+6 i g(x)=−9x+3x² | pendent |
| `alg-23j2-q2` | juny 2023 · s5 | Àlgebra | Sistema lineal amb paràmetre k | pendent |
| `geo-23j2-q3` | juny 2023 · s5 | Geometria | Posició relativa de rectes a l'espai segons m i distància | pendent |
| `ana-23j2-q4` | juny 2023 · s5 | Anàlisi | Optimització: torre de comunicacions i cost del cablejat | pendent |
| `alg-23j2-q5` | juny 2023 · s5 | Àlgebra | Família de matrius 2×2 amb a, b ∈ ℝ | pendent |
| `ana-23j2-q6` | juny 2023 · s5 | Anàlisi | Funció racional: paràmetres a, b per extrem relatiu | pendent |
| `ana-23j-q1` | juny 2023 · s1 | Anàlisi | Polinomi cúbic determinat per condicions sobre f, f', f'' | pendent |
| `alg-23j-q2` | juny 2023 · s1 | Àlgebra | Producte de matrius A·B i propietat idempotent | pendent |
| `ana-23j-q3` | juny 2023 · s1 | Anàlisi | Funció f'(x) per trams i recta tangent a f' | pendent |
| `alg-23j-q4` | juny 2023 · s1 | Àlgebra | Sistema lineal amb paràmetre λ | pendent |
| `ana-23j-q5` | juny 2023 · s1 | Anàlisi | Optimització: jardí rectangular adossat a un mur | pendent |
| `geo-23j-q6` | juny 2023 · s1 | Geometria | Plans perpendiculars i punt més proper a una recta | pendent |

---

## 7. Feina pendent

### 7.1 Com s'apliquen els lliuraments

Des de la sessió 5, cada sessió parteix de l'estat actual del repositori i lliura només els
fitxers de font que canvia. Tot es fa des de la web de GitHub; no cal el Codespace.

- **A l'inici de la sessió**, el professor baixa el repositori de GitHub (Code → Download ZIP)
  i el puja a la conversa. No serveix el ZIP de la sessió anterior, perquè pot no incloure
  canvis fets després.
- **Al final**, la sessió lliura un ZIP amb només els fitxers de font que canvien,
  **directament a l'arrel del ZIP** i amb els camins del repositori (`build/build.py`,
  `README.md`…). No hi ha cap carpeta que els emboliqui, perquè l'extractor descomprimeix el ZIP
  tal com ve a l'arrel del repositori. Mai no porta PDF, ni `cataleg.js`, ni res de
  `.github/workflows/`.
- **Per aplicar-lo**, el professor puja el ZIP a la carpeta `_uploads` (Add file → Upload
  files). Un workflow del repositori el descomprimeix a l'arrel i en fa commit, amb el missatge
  «Auto-extract uploaded zip».
- **Després, cal llançar el build a mà** des d'Actions → Compila el banc → Run workflow.
  GitHub no encadena els workflows: un commit fet pel bot d'extracció no dispara cap altre
  workflow, tampoc «Compila el banc».
- **Els workflows** (`.github/workflows/`) no poden arribar per `_uploads`, perquè el bot no té
  permís per escriure-hi. Es creen i s'editen des de la web de GitHub, enganxant-ne el
  contingut.

**A la sessió 5**, `compila.yml` es va crear des de la web, i l'Action va sortir en verd per
primera vegada: set passos, amb tots els PDF compilats amb el preàmbul oficial. L'últim
lliurament de la sessió és l'apartat 11.

### 7.2 Dades del professor

- **Unitats 1 a 6: resolt.** Els títols surten del full de programació i la u4 la va confirmar
  el professor. Són Matrius (u1), Determinants (u2), Sistemes d'equacions (u3), Vectors a
  l'espai (u4, que es fa dins de la u5), Rectes i plans en l'espai (u5) i Angles i distàncies
  a l'espai (u6). S'han d'afegir a `temes.json`, i llavors es poden omplir les `unitats`
  d'`alg-26j-q2` i de `geo-26j-q4b`. Mentre no hi siguin, les targetes diuen «per definir» i el
  build n'avisa. Una PAU que necessiti vectors ha de dir `u5`, no `u4`.
- **Pendent de confirmar: els exercicis 30 i 34 de la u9.** Són a les setmanes 9 i 10, però al
  solucionari no surten a cap secció d'aplicacions de la derivada: el 34 hi apareix com un
  exercici de domini d'un logaritme, i el 30 no s'hi troba. Els altres catorze sí que encaixen.
- **Pendent de confirmar: l'exercici 92 de la u8.** Surt a les setmanes 5 i 7, tant al full de
  programació com a `tasques.js` del repositori `sol`. Cal saber si és volgut abans de
  calibrar els temes de la u8.
- Opcionalment, **confirmar amb els originals** les sèries de `23s` (2) i `24j` (1), que avui
  provenen d'una rèplica pública.

### 7.3 Importació PAU: 56 exercicis en 10 convocatòries

Es fa després de la u8 (decisió de la sessió 5).

| Convocatòria | Sèrie | Pendents |
|---|---|---|
| `26j2` juny 2026 | 5 | 5 |
| `25j` juny 2025 | 1 | 5 |
| `25s` setembre 2025 | 3 | 5 exercicis (6 entrades al repositori `pau`; vegeu 7.6) |
| `25i` juny 2025 | 4 | 5 |
| `24s` setembre 2024 | 3 | 6 |
| `24j` juny 2024 | 1 | 6 |
| `24i` juny 2024 | 5 | 6 |
| `23s` setembre 2023 | 2 | 6 |
| `23j2` juny 2023 | 5 | 6 |
| `23j` juny 2023 | 1 | 6 |

Ritme proposat: **dues convocatòries per sessió**, unes onze preguntes, en cinc sessions.
Algunes preguntes tenen figures (per exemple, la gràfica de $f'(x)$ de `ana-26j2-q4a`) que
s'han de refer en TikZ; compten el doble de feina.

Les preguntes anteriors a 2025 segueixen el format antic, en què es triaven 4 qüestions de
6. Continuen sent de 2,5 punts i hi encaixen igual.

### 7.4 Contingut del banc, en l'ordre del calendari

L'ordre de les unitats el fixa la programació del curs: el full «2Bat - Unitats i feina
Classroom» i, per a les setmanes ja programades, `tasques.js` del repositori `sol`. No és
l'ordre numèric.

| Unitat | Setmanes | Última data límit |
|---|---|---|
| u7 Límits i continuïtat | 1–4 | 11 d'octubre de 2026 · **feta**, reescrita a la sessió 6 |
| u8 Derivades | 5–7 | 1 de novembre de 2026 · **feta** |
| u9 Aplicacions de les derivades | 8–10 | 22 de novembre de 2026 · **feta** |
| u10 Representació de funcions | 11–12 i 17 | 6 de desembre de 2026 i 10 de gener de 2027 · **oberta**, una variant per tema |
| u13 Probabilitat | 13–14 | 20 de desembre de 2026 |
| u14 Distribucions de probabilitat | 15–16 | 3 de gener de 2027 |
| u1 Matrius | 18–19 | 24 de gener de 2027 |
| u2 Determinants | 20–22 | 14 de febrer de 2027 |
| u3 Sistemes d'equacions | 23–25 | 7 de març de 2027 |
| u5 Rectes i plans en l'espai (amb la u4) | 26–30 | 11 d'abril de 2027 |
| u6 Angles i distàncies a l'espai | 31–32 | 25 d'abril de 2027 |
| u11 Integrals | 33–34 | 9 de maig de 2027 |
| u12 La integral definida | 35–36 | 23 de maig de 2027 |

- **Calibrar els minuts** amb dades reals, a partir del primer examen de la u7. Ara són
  estimacions: uns 16–20 minuts per pregunta a 1 h 30 i uns 10–12 a 50 min.
- **Segona i tercera variant dels cinc temes de la u10**, que ara en tenen una.
- **Temes i preguntes de la u13**, la següent per calendari (20 de desembre). Després, les
  unitats en l'ordre de la taula.
- **Versions de 50 min per a les preguntes PAU**, on tingui sentit: quin apartat es treu i com es
  reparteixen els punts.
- La u7, la u8 i la u9 tenen tres variants per tema: se'n poden muntar tres exàmens de cada
  unitat sense repetir cap pregunta.
- **Material reservat** de la reescriptura, per si cal:
  - $\lim_{x\to+\infty}\frac{x^3+2x}{3^x}$ (jerarquia d'infinits), de l'antiga `limits-punt/q001`.
    No és a cap exercici assignat.
  - Lectures de límits a l'infinit i en $x=4$ de les gràfiques de `limits-grafica/q001` i `q002`.
  - Els tres límits de $\frac{2x}{\sqrt{x^2+5}}$ de l'antiga `limits-punt/q002`: només
    demanaven substituir, massa directes per a un apartat.

### 7.5 Millores del lloc

- **Filtre de preguntes PAU per unitats fetes.** Amb 29 preguntes d'anàlisi, recórrer-les amb
  ◀ ▶ serà feixuc: és la millora més necessària quan avanci la importació. El filtre ha de
  seguir l'**ordre real del curs** de la taula de 7.4, no l'ordre numèric: «fins a la u9» vol
  dir u7, u8 i u9, però «fins a la u1» inclou també la u10, la u13 i la u14. Aquesta seqüència
  s'ha de desar com a dada, per exemple a `temes.json`, i no s'ha de deduir dels números. Un
  cop existeixi, la u1 i les altres unitats noves s'hi afegeixen en l'ordre del curs.
- **Conservar els visors PDF oberts.** Ara cada clic torna a pintar totes les targetes: els
  `iframe` es recreen i els PDF es tornen a carregar. Amb molts visors oberts es notarà.
- Al mòbil, llista de temes plegable. Ara la llista queda sencera abans de l'examen.
- Els noms de les unitats apareixen en passar el ratolí per sobre, i això no funciona en
  pantalles tàctils. Cal mostrar-los d'una altra manera.

### 7.6 Decisions obertes

- **Com s'importa l'exercici 3 de setembre de 2025.** El repositori `pau` el té dues vegades,
  com a `pro-25s-q3ab` i com a `ana-25s-q3c`. És un sol exercici de 2,5 punts: a) i b) de
  probabilitat, i c) de derivades. Si s'importen totes dues entrades, un examen el podria
  portar dues vegades. Si només s'importen a) i b), sumen 1,5 punts i el build les rebutja.
  La proposta és importar-lo **una sola vegada**, al bloc de probabilitat i amb els tres
  apartats. Cal triar el codi abans, perquè serà permanent:
  - `pro-25s-q3ab` manté l'identificador del repositori `pau`, però suggereix que només té
    els apartats a) i b);
  - `pro-25s-q3` descriu millor l'exercici, però trenca la regla que el codi és el del
    repositori `pau`.
- **Fer els PDF reproduïbles.** pdfTeX hi escriu la data i un identificador. Per això cada
  build reescriu tots els PDF encara que no canviïn, i el commit del bot els toca tots cada
  vegada. Amb `SOURCE_DATE_EPOCH` i `FORCE_SOURCE_DATE=1` fixos a l'Action, dos builds
  idèntics no canvien cap PDF (comprovat a la sessió 5). Caldria fer el mateix amb el camp
  `generat` del catàleg, que ara canvia a cada build.
- **Instruccions de les opcions.** El `.tex` només diu «Pregunta 4a» i «Pregunta 4b»; no hi
  afegeix cap frase del tipus «responeu-ne una», perquè depèn del tractament (el punt
  següent). Mentrestant, el professor l'escriu al `.tex`.
- **Tractament de vosaltres o de tu.** Si un examen barreja preguntes PAU (literals, amb
  vosaltres) amb preguntes del banc (amb tu), hi conviuen les dues formes.
- Si s'hi incorporen les **pistes** del repositori `pau` (els PDF `-p`), com una tercera vista
  al costat de l'enunciat i la solució.
- Si mai el repositori es fa públic, caldrà revisar els drets dels enunciats i dels criteris
  PAU, i decidir-ne la llicència.

---

## 8. Riscos i limitacions coneguts

- **Els workflows no poden arribar per `_uploads`.** El bot d'extracció no té permís per
  escriure a `.github/workflows/`, i un push des del Codespace, amb el permís per defecte,
  tampoc. Es creen i s'editen des de la web de GitHub.
- **El build no es dispara sol després d'una pujada a `_uploads`.** El commit del bot
  d'extracció no activa cap altre workflow: cal llançar «Compila el banc» a mà (7.1).
- **Fitxers generats per una altra via.** Els PDF i `cataleg.js` només els ha de generar
  l'Action. Si n'arriben per `_uploads` o des del Codespace, poden no coincidir amb les fonts.
  A més, si arriben mentre l'Action treballa, el pas de desar xoca i falla sense desar res
  (simulat a la sessió 5).
- **PDF no reproduïbles.** Cada build reescriu tots els PDF encara que no canviïn (vegeu 7.6).
- **GitHub Pages publicaria les solucions.** Amb el pla gratuït, Pages només publica
  repositoris públics. Amb GitHub Pro publica repositoris privats, però el lloc publicat és
  públic: qualsevol persona amb l'adreça veuria les solucions. Només GitHub Enterprise Cloud
  permet un lloc privat. Per veure el lloc des de GitHub sense publicar res, vegeu el README
  («Veure el lloc des del Codespace»).
- **Quota de minuts.** Les Actions en repositoris privats consumeixen minuts del pla
  gratuït. Cada build instal·la TeX Live i en gasta uns pocs.
- **Ubuntu 26 a partir del 19 d'octubre de 2026.** `ubuntu-latest` hi passarà, amb un TeX Live
  nou que podria canviar la compaginació sense fer fallar el build. A la sessió 5 es va
  recomanar fixar `runs-on: ubuntu-24.04` i passar a `actions/checkout@v5`, que també treu
  l'avís de Node 20. Són dues línies de `compila.yml`, que es canvien des de la web.
- **Visor de PDF.** Depèn del navegador; hi ha l'enllaç alternatiu.
- **SymPy 1.14** s'equivoca amb límits d'exponencials a $-\infty$. Qualsevol verificació ha de
  tenir un segon mètode.

---

## 9. Procediment per importar una convocatòria PAU

És el procediment que es va seguir amb juny de 2026.

1. **Llegir els originals com a imatge, no com a text.** El text dels PDF perd les fórmules
   (`e2x –1` vol dir $e^{2x-1}$), i hi ha funcions a trossos que no hi surten. Cal renderitzar
   `data/<codi>-e.pdf` i `data/<codi>-s.pdf` i llegir-los.
2. **Transcriure l'enunciat literalment** a `pau/<bloc>/<codi>/pregunta.tex`, amb les macros
   del banc: `\apartat{}` amb la puntuació oficial, `\si{}` a les funcions a trossos, i TikZ
   amb `step=1` si hi ha figures.
3. **Transcriure el criteri oficial** a cada `solucio`, i acabar cada apartat amb
   «*Pauta oficial:* …».
4. **Verificar tots els resultats** per un mètode independent, amb càlcul simbòlic i un segon
   camí per als límits a l'infinit. Si el criteri oficial s'equivoca, corregir-ho i deixar una
   *Nota del banc*.
5. **Escriure el `meta.json`**: títol, unitats necessàries, dificultat, uns 22 minuts i
   etiquetes.
6. **Compilar** amb `python3 build/build.py --pregunta pau/`. Cada enunciat ha d'ocupar una
   pàgina, i no hi pot haver cap *Overfull*: les fórmules llargues en línia han de passar a mode
   destacat. Si a l'entorn falten paquets, s'afegeix `--preambul` amb un preàmbul reduït, i el
   build avisa que aquells PDF no són definitius.
7. **Passar les proves**: `prova_validacio.py`, `prova_sortida.py` i `prova_paritat.py`.
8. **Fer un PDF de revisió del lot** perquè el professor el contrasti amb els originals.
9. **Lliurar només les fonts**, pel mètode de 7.1. Mai PDF ni `cataleg.js`.

Si el repositori `pau` incorpora convocatòries noves, s'han d'afegir a
`pau/convocatories.json` amb la seva font. La sèrie es troba a la capçalera del criteri oficial
del primer exercici.

---

## 10. Trampes tècniques ja conegudes

| Trampa | Com s'evita |
|---|---|
| `String.replace` amb una cadena interpreta `$$`, `$'`, `$&` | Sempre un substitut en forma de funció |
| `grid` de TikZ fa passos d'1 cm absolut | `step=1` explícit (regla 8) |
| `pdflatex` escriu els accents en T1, no en UTF-8 | Descodificació tolerant de la sortida |
| El paquet `comment` exigeix `\end{solucio}` sol a la línia | Regla 7 |
| Una macro amb `@` definida fora de `\makeatletter` | Tot el bloc dins de `\makeatletter … \makeatother` |
| `\si` xoca amb `siunitx` si mai s'hi carrega | El build fallaria en voler redefinir-la; caldria reanomenar-la |
| `grep [ÈE]` no funciona amb UTF-8 | Fer servir Python amb normalització Unicode |
| El commit del bot podria tornar a disparar l'Action | Filtre de camins, `[skip ci]` i `GITHUB_TOKEN` |
| `decodeURIComponent` llança una excepció amb un `%` solt | `try/catch`: l'adreça es llegeix sense descodificar (regla 5 d'`app.js`) |
| Un objecte `{}` troba `__proto__` i `constructor` com si fossin temes | `PER_TEMA` es crea amb `Object.create(null)` |
| Si la branca avança durant el build, el push del bot és rebutjat | `git pull --rebase` i fins a tres intents |
| pdfTeX escriu la data i un identificador a cada PDF | `SOURCE_DATE_EPOCH` (pendent, 7.6) |
| Provar el build sense TeX | Un `pdflatex` fals al PATH, com fa `prova_sortida.py` |
| Moure o treure una pregunta podria desfer la 4a i la 4b | L'estructura és de les places: només es mouen les preguntes |
| El preàmbul cita `\begin{document}` en un comentari | Per trobar el cos del `.tex`, cal buscar la línia exacta, no el text |
| Un retoc fet a mà en un fitxer baixat es perd a la descàrrega següent | Si val la pena, ha de pujar al banc: `\colorgrafica` en va sortir |
| Una fórmula destacada després d'una línia curta queda enganxada (TeX hi posa l'espai «curt») | El preàmbul iguala `\abovedisplayshortskip` a l'espai normal |
| En un Chromium sense pantalla, obrir un PDF el descarrega | Una prova que baixa el `.tex` no ha d'obrir cap visor abans |

---

## 11. Aquest lliurament

És el lliurament de la sessió 13. Parteix del de la sessió 12, que ja és al repositori.

| Fitxer | Canvi |
|---|---|
| `temes.json` | Els cinc temes de la u10 |
| `u10/*/q001` | **Noves**: cinc preguntes, una per tema |
| `README.md`, `handout.md` | Estat, inventari de la u10 i sessió 13 |

No porta cap PDF ni `cataleg.js`, i no toca cap workflow. Després de pujar-lo a `_uploads`,
cal fer **Run workflow**.
