# Handout · Banc de preguntes de Matemàtiques II

**Data:** 27 de setembre de 2026 · **Estat:** 68 preguntes (24 de la unitat 7, 18 de la unitat
8, 12 de la unitat 9, 9 de la unitat 10 i 5 de la PAU), 60 amb tries · 1.276 minuts d'examen al banc · 38 comprovacions del validador, 14 de sortida del build i 77 de
paritat

Aquest document explica tota la feina feta fins avui i tota la feina pendent, amb prou
detall perquè qualsevol persona pugui reprendre el projecte sense haver seguit les converses
on es va construir. El README descriu com és el projecte; aquest document explica com hi hem
arribat i cap on ha d'anar.

---

## 1. Resum

El projecte ha passat per catorze sessions. La primera va avaluar un `main.tex` fet per una
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
amb quatre temes i tres variants de cadascun, i la tretzena va obrir la u10. La catorzena, a
partir d'un exemple concret d'edició a mà en un projecte Overleaf, va introduir les **tries**:
un apartat pot oferir més d'una alternativa, triable des de la carta, sense deixar de ser el
mateix apartat de sempre quan no se'n toca res. La quinzena, arran d'una captura de pantalla
del professor, va tancar el forat més gros que havien deixat les tries: es triava una
alternativa sense poder-la llegir. Ara cada ítem té el seu propi Enunciat i Solució
compilats, com qualsevol pregunta. La setzena hi va afegir contingut nou i verificat a **totes
les 24 preguntes de la u7**, a més de treure dues coses que el professor ja no necessitava (la
nota de la tria i el botó «amb solucions»). La dissetena, arran d'una crítica del professor
(setze d'aquelles alternatives només canviaven els nombres) i dels enunciats PAU de 2023 a 2026,
les va substituir per alternatives que canvien el cas, la tècnica o el sentit del raonament. La divuitena
va fer que el build esborri els PDF que ja no genera cap font, perquè els 60 orfes que havia deixat
la dissetena feien fallar l'Action, i va posar tries a les 18 preguntes de la u8, amb el mateix
criteri. La dinovena va fer el mateix amb les 12 de la u9, i va fer plegables les unitats de la
llista de temes. La vintena va començar a completar la u10, a partir del solucionari del llibre i
del full de feina de Classroom, amb els exercicis que els alumnes hauran practicat de debò. La vint-i-unena hi va afegir les asímptotes, i va deixar congelat el tema de
funcions a trossos fins que s'hagi fet la setmana 17. La màquina
funciona de punta a punta. El que queda és
sobretot contingut: la u9, que acaba el 22 de novembre, els 56 exercicis PAU pendents, la
resta d'unitats, i estendre les tries a la u10.

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

### 2.14 Sessió 14 · Les tries: preguntes més granulars i configurables

El professor va portar un exemple concret, no una petició abstracta: un projecte Overleaf amb
`prova-1.tex` (baixat del lloc, sense tocar) i `examen-sencer.tex` (editat a mà). La comparació,
un cop resseguida fins a les fonts, deia tres coses:

- **Q1** (`limits-infinit/q002`), apartat a): d'1 límit (0,75 punts a 1 h 30) a 4 límits
  (2 punts), cobrint la tipologia sencera (grau del numerador més gran, igual i més petit, als
  dos infinits).
- **Q1**, apartat b): «determina $a$» sense la reflexió sobre $a=0$, amb un objectiu diferent
  (0,5 punts en lloc d'1,25).
- **Q3** (`limits-grafica/q001`), apartat b): «classifica la discontinuïtat» substituïda per
  «calcula quatre imatges», **amb el mateix cost** (1,25 punts) — el canvi més net dels tres,
  perquè no barreja cap redistribució de punts.

El lloc només oferia dues palanques —quin tema, quina variant— i, dins d'una pregunta, la
duplicitat 1 h 30 / 50 min via `nomesllarg` i `\apartat[x]{y}`. Cap de les dues permetia triar
quants ítems calculadors dur un apartat, ni bescanviar-ne el contingut sencer per un altre amb
un cost diferent. El professor ho havia hagut de resoldre a mà, a Overleaf.

**Disseny.** Mirant els tres canvis junts, els dos primers («quants ítems» i «amb subtasca o
sense») i el tercer («una alternativa sencera, mateix cost») van resultar ser **el mateix
mecanisme**: triar exactament un cos complet, amb la seva pròpia solució i el seu propi cost,
d'entre uns quants de declarats. Un `\begin{tria}{id}…\end{tria}` en substitueix l'apartat
sencer; cada `\itemtria{id}{punts}` és un ítem permanent, com `q001`. La primera versió del
disseny preveia també triar-ne uns quants d'una llista compartida (com una `graella` amb
comptador), amb els seus propis punts per ítem i un repartiment automàtic; revisant-ho a
l'hora d'implementar-ho, cap dels tres exemples el necessitava —tots tres es descriuen com
«un cos sencer en lloc d'un altre»— i la versió simple, sense combinatòria, ho cobreix tot amb
molta menys superfície de disseny. Es guarda com a ampliació natural, no com a feina feta.

Per triar-ne l'abast: la tria és **només per a preguntes del banc**, mai per a PAU (l'enunciat
hi ha de ser literal, com ja diu el README). I els ítems es preparen i es verifiquen **sempre
com fins ara**, pel mateix `build.py`; el lloc només ofereix triar entre els que ja hi ha, no
escriure'n cap al vol sense passar-hi. Ho va confirmar el professor explícitament.

**Implementació.** `\begin{tria}`/`\itemtria` són marques només de les fonts, com `nomesllarg`:
`defs.tex` no en veu mai cap. `materialitza()` (build.py i app.js, ara amb un tercer paràmetre
`seleccio`) les resol abans que res més hi toqui, triant sempre exactament un ítem —el primer
declarat per defecte, o el de `[defecte-curt=id]` a 50 min— i deixant, en el seu lloc, un
`\apartat{…}` normal amb el cos triat. Sense cap `seleccio`, el resultat és **idèntic byte a
byte** al d'abans que existissin les tries: comprovat amb les dues preguntes pilot abans i
després de la migració, a totes dues modalitats. `app.js` hi afegeix, per plaça de l'examen, un
`seleccio` (buit per defecte) i un selector per tria a la carta, amb els punts de cada
alternativa a la durada triada; l'adreça en desa la selecció amb un sufix nou
(`~id-tria=id-ítem`, separat per `;`) que no toca les adreces d'abans, sense cap tria.

**Migració pilot.** `u7/limits-infinit/q002` i `u7/limits-grafica/q001` —les preguntes de
l'exemple— reescrites amb tries, amb els mateixos defectes d'abans i el contingut exacte que el
professor havia escrit a mà com a alternatives (`quatre-tipus`, `sense-reflexio`,
`avalua-imatges`), més un tercer ítem intermedi (`dos-tipus`) a `limits-infinit-tipus` per no
deixar-ho en una simple opció binària. La resta del banc no es toca: la migració és **opcional
i incremental**, com la resta d'apartats de 50 min a la sessió 6.

**Verificació.** Paritat de la `materialitza()` amb tries, Python contra JavaScript executat de
debò amb Node, en 14 combinacions. Una prova d'integració amb jsdom (clics reals sobre el DOM),
8 casos: hi va sortir un error de càlcul **de la pròpia prova** —l'apartat `nomesllarg` de
`limits-infinit/q002` segueix comptant a 1 h 30 encara que es triï `quatre-tipus`, cosa que a
50 min no passa perquè aquell apartat hi desapareix— i, corregit, tots vuit hi passen. Nou casos
nous a `prova_validacio.py` (38 en total) i disset comprovacions noves a `prova_paritat.py` (77
en total), incloent-hi `triaCanvia` com una acció més. Compilació real amb `pdflatex` (amb un
preàmbul reduït, perquè aquest entorn no té `lmodern` ni `babel`-català): les dues preguntes
migrades i quatre combinacions més, totes a una pàgina i sense errors; tot el banc (246 PDF)
recompilat sense cap regressió.

En el procés es van trobar i corregir tres errors propis, cap d'ells detectat fins que es va
provar de debò (vegeu la secció 4): un `defecte-curt` que apuntés a un ítem inexistent feia
petar `punts_del_tex` amb un `KeyError` en lloc de donar un error net; un `\itemtria` amb
l'identificador mal format desapareixia en silenci en lloc de fer fallar el build; i una tria
sense cap ítem feia petar la construcció del catàleg amb un `IndexError`, també abans d'arribar
al missatge d'error que ja s'havia registrat correctament.

### 2.15 Sessió 15 · Cap tria a cegues: una previsualització per ítem

El professor va provar les tries al lloc real (amb els PDF de la sessió 14, ja amb els
paquets oficials) i va enviar una captura: la carta de `limits-grafica/q001` amb «avalua
imatges» triat, i cap manera de veure'n l'enunciat ni la solució —l'Enunciat i la Solució de
la carta seguien mostrant sempre el defecte, tal com deia la nota de sota del selector. Amb
paraules seves, triar així «és horrible»: en un examen real, triar una alternativa que no es
pot llegir ni verificar no és acceptable.

**Per què no s'havia resolt a la sessió 14.** Es va deixar apuntat com a limitació coneguda
(secció 5, «No verificat») en lloc de resoldre's, perquè la solució que s'hi va descartar
—compilar LaTeX en directe al navegador— hauria trencat el principi 4 del projecte («lloc
sense dependències… funciona obert com a fitxer local»): calia un motor LaTeX en JavaScript,
una dependència nova i grossa, o un servidor que compilés a petició, que el lloc no ha tingut
mai. Cap de les dues coses és necessària: cada ítem d'una tria és, com qualsevol pregunta, un
cos que **build.py ja sap compilar sol**.

**Disseny i implementació.** `cos_dun_item()` (build.py) n'aïlla el cos i els punts, amb el
mateix mètode de retall per posicions que ja feia servir `materialitza()` per triar-lo.
`construeix()` el compila com una miniatura d'una sola pregunta —`\begin{apartats}
\apartat{punts} …cos… \end{apartats}`, amb la capçalera «Alternativa»— a
`out/tries/<id-tria>/<id-item>/`, i el catàleg hi porta les rutes de cada ítem (`pdf`,
`pdf_solucio`, i les de 50 min, deduplicades quan el cos no hi difereix, exactament com ja fa
`pdf_curt` a la pregunta sencera). Al lloc, cada tria té ara els seus propis botons
**Enunciat**/**Solució** —reaprofitant `mostra()` amb una clau composta
`pregunta:tria`, sense cap funció nova—, que mostren l'ítem **triat**, no el defecte; si el
visor ja és obert i es canvia l'ítem, s'actualitza sol, sense haver de tornar a clicar.

**Verificació.** Compilades i revisades visualment totes dues previsualitzacions de
`limits-grafica/q001` amb el preàmbul reduït d'aquest entorn —«avalua imatges» hi surt
exactament com la captura del professor l'hauria de tenir, amb l'enunciat i la solució
completa, en blau—. Quatre casos nous a la prova d'integració amb jsdom, incloent-hi que
canviar d'ítem amb el visor obert l'actualitza sol i que la tria que no s'ha tocat no obre res.
Tot el banc (268 PDF, catorze més que abans per a les dues preguntes migrades) recompilat
sense cap regressió.

En revisar els efectes secundaris, es va trobar que `prova_sortida.py` comptava «246 PDF» amb
un patró (`*/*/*/out/*.pdf`) que no arribava mai a `out/tries/…`: no fallava —perquè no
comprovava res d'allò que no veia—, però deixava de provar una part real del que ara escriu el
build. Corregit als dos llocs on hi apareixia el patró, i afegit un cas nou, paral·lel al de
`--pregunta` que ja hi havia, que demostra que també escriu les previsualitzacions de cada
ítem.

### 2.16 Sessió 16 · Tries a tota la unitat 7, i dues supressions

El professor va confirmar que la sessió 15 funcionava «perfecte» i va demanar estendre les
tries a tota la u7 —no unes quantes preguntes més, totes—, més dues supressions: la frase de
la nota de sota del selector («ja mostren la selecció feta…»), que li semblava soroll, i el
botó «amb solucions» del peu de pàgina, que no feia servir.

**Les supressions**, primer perquè eren ràpides i no interferien amb la resta: la nota es
treu sencera d'`app.js` (i la variable `personalitzada`, que només servia per decidir-la, ja
no cal); el botó, d'`index.html` i de les tres línies d'`app.js` que hi feien referència (el
`disabled` en pintar i els dos `onclick`). Cap altre lloc en depenia.

**Contingut nou a les 22 preguntes que encara no en tenien** (`bolzano-biseccio`,
`continuitat-trossos`, `domini-discontinuitats`, `limits-grafica/q002-q003`,
`limits-infinit/q001,q003`, `limits-punt`, `limits-trossos` i `parametres-ab`; les altres
dues ja en tenien des de la 14). Cada tria hi és nova —no és el mateix mecanisme repetit amb
un altre nom—: quantes tasques de límits o continuïtat calculadores dur, quin punt de
substitució directa preguntar dins la mateixa branca d'una funció a trossos, quina funció
(polinòmica, exponencial, logarítmica) fer servir per a la mateixa demostració de Bolzano o
el mateix estudi de continuïtat amb paràmetres, o quina lectura fer sobre la mateixa gràfica.
Cada funció, límit i solució nova es va verificar numèricament amb Python (i amb SymPy els
casos amb factoritzacions) **abans** d'escriure-la al `.tex`, mai després.

**Mètode.** Amb 22 preguntes per davant, calia una disciplina que aguantés l'escala: per a
cada pregunta, es desa l'original, s'escriu la migració, i es passa **immediatament** per
`materialitza()` a totes dues modalitats (comparació byte a byte amb l'original) i per
`punts_del_tex()`, abans de tocar la següent. Aquesta disciplina —no la vista, ni la
intuïció— és la que va detectar els dos errors propis d'aquesta sessió, tots dos en el primer
tema (`bolzano-biseccio` i `continuitat-trossos`) i cap als dos temes següents: primer, una
edició mal feta a `continuitat-trossos/q001` que va barrejar l'enunciat d'un apartat amb la
solució d'un altre (es va refer el fitxer sencer, no pedaçar-lo); després, l'ordre dels
arguments de `\itemtria{id}{1h30}{50min}` invertit a `continuitat-trossos/q002` (havia
transcrit l'ordre literal del claudàtor `[50min]{1h30}` sense capgirar-lo). Els 22 fitxers
migrats després ja no en van tenir cap.

En acabar-ho tot, dues bateries pròpies van necessitar-se al dia, no perquè fallessin sinó
perquè dues de les seves fixtures assumien un contingut que ja no hi era: `prova_sortida.py`
trencava la puntuació d'una pregunta injectant-hi `\apartat[2,5]{1,5}`, que ja no existeix a
`parametres-ab/q001` (ara hi ha `\itemtria{original}{1,5}{2,5}`), i el cas de `--pregunta`
esperava exactament 4 PDF de `limits-punt/q001`, que ara en té 10 perquè ja té una tria; s'ha
mogut aquest segon cas a una pregunta de la u8 encara sense tries (`derivada-definicio/q001`),
per no barrejar-lo amb el cas ja existent que prova `--pregunta` amb tries. La prova
d'integració amb jsdom (no formal al repositori) tenia el mateix problema en dos llocs
(assumia que `limits-infinit/q003` i el tema «Límits en un punt» no tenien tries), corregits
de la mateixa manera.

**Verificació.** Les 24 preguntes, validades i compilades de debò amb el preàmbul reduït
d'aquest entorn: 436 PDF (abans, 268), cap error, cap *Overfull*, totes a una pàgina, els
mateixos punts per defecte d'abans de tocar-les. Les tres bateries formals (38/11/77) i la
integració amb jsdom, totes en verd després de posar-les al dia.

### 2.17 Sessió 17 · Alternatives que canvien el cas, no els nombres

El professor va revisar les tries de la sessió 16 i en va fer una crítica precisa: algunes li
agradaven molt, però en altres «l'única cosa que fas és canviar els nombres de l'enunciat, però
en el fons estàs preguntant el mateix». I hi va afegir l'excepció que ho aclareix tot: canviar
un nombre sí que és pertinent quan canvia el cas, com un límit que passa de ser una
indeterminació 0/0 a ser directament 3/0. Comptades una per una, 8 de les 24 preguntes tenien
una alternativa que canviava la tasca, i 16 eren la mateixa pregunta amb altres nombres (tot
`bolzano-biseccio`, `domini-discontinuitats`, `limits-punt`, `limits-trossos` i
`parametres-ab`, més `continuitat-trossos/q002`).

**La PAU com a referència.** El professor va passar el recull d'enunciats PAU de 2023 a 2026:
62 enunciats dels quatre blocs. La u7 només surt als d'anàlisi, sempre com un apartat d'un
exercici mixt, de 0,5 a 1,25 punts. Hi surt Bolzano per a un valor i no per a una arrel
(23s-q4), localitzar una arrel amb una precisió donada i dir quantes n'hi ha exactament (24i-q1,
24s-q1), límits a la frontera del domini de funcions no racionals per fer-ne l'esbós (24i-q1,
24j-q1), el domini de $\sqrt{1+x^3}$ (25i-q1) i la continuïtat amb un sol paràmetre que hi entra
al quadrat, amb un valor que un enganxament dona i l'altre descarta (26j-q1). Cap no demana un
límit 0/0 per factoritzar, i els sistemes en $a$ i $b$ que hi surten són de derivades, no de
continuïtat.

**El criteri**, que ara és la regla 16 del README: una alternativa ha de canviar el que l'alumne
decideix (un altre cas, una altra tècnica o el raonament a la inversa), no només les xifres.

**Les 16 alternatives noves** porten identificadors nous. La regla 13 no deixa reaprofitar
`alternativa` ni `dos-limits` per a un contingut diferent, i una adreça desada que en porti un
cau al defecte.

| Tema | Què demana ara l'alternativa |
|---|---|
| `limits-punt` | q001, un k/0 amb tots dos laterals $+\infty$ (`quocient-k-zero`); q002, valor absolut, amb un límit de laterals finits i diferents i un altre que sí que existeix (`valor-absolut`); q003, el conjugat (`conjugat`) |
| `limits-trossos` | Un segon límit en un punt de l'**altra** branca, on la fórmula de la primera donaria un valor trampa (`altra-branca`) |
| `bolzano-biseccio` | q001, trobar l'interval en lloc de verificar-lo (`troba-interval`); q002, comptar arrels, exactament tres (`tres-arrels`); q003, les hipòtesis, amb $\frac1{x-1}$ a $[0,2]$ (`hipotesis`) |
| `domini-discontinuitats` | Un factor comú que **no** fa evitable la discontinuïtat (`factor-doble`), i una segona tria a l'apartat de domini, amb taules de signes i condicions combinades (`domini-funcions`, ítem `signes-i-condicions`) |
| `continuitat-trossos/q002` | Una discontinuïtat dins d'una branca, que no és cap enganxament (`branca-interna`) |
| `parametres-ab` | q001, un paràmetre al quadrat amb un valor descartat (`un-parametre`); q002, condicions incompatibles, «cap valor» (`incompatible`); q003, una discussió segons $k$ (`discussio-k`) |

**Tres adaptacions de la proposta**, fetes en llegir les preguntes senceres abans d'escriure-hi.
(1) A `limits-trossos`, el `nomesllarg` de totes tres preguntes ja demanava els límits a
$\pm\infty$, i l'alternativa proposada, un límit a $-\infty$, s'hi hauria repetit a 1 h 30. Es va
canviar per un punt de l'altra branca, que conserva la idea: decidir quina branca mana.
(2) A `limits-punt/q001`, el `nomesllarg` ja tenia un 2/0 amb laterals oposats, i per això
l'alternativa és el cas k/0 en què tots dos laterals coincideixen. (3) A `parametres-ab`, el
`nomesllarg` de q001 i q003 ja demanava «tots els valors de $m$» d'una equació de segon grau, i
l'alternativa de q001 es va dissenyar perquè hi aportés una cosa nova: creuar dues condicions i
descartar-ne un valor.

**Verificació.** Totes les funcions, límits, dominis i valors de paràmetres es van comprovar amb
SymPy abans d'escriure'ls. Cada fitxer es va verificar just després d'escriure'l: el defecte és
idèntic byte a byte a totes dues durades, no hi ha cap error, i la pregunta suma 2,50 punts amb
cada ítem triat. Tot el banc es va compilar amb el preàmbul reduït: 464 PDF, cap error ni
*Overfull*. Les tres bateries (38/11/77) i la integració amb jsdom passen sense haver-les de tocar.

**PDF orfes.** Aquesta és la primera sessió que retira ítems d'una tria. El build copia els PDF
a `out/`, però no n'esborra mai cap, i l'Action només fa `git add` dels que existeixen. Per tant,
les previsualitzacions dels 16 ítems retirats es quedarien al repositori. Es van donar per
inofensius, perquè el catàleg no hi apunta, i la neteja es va proposar com a opcional. No ho eren:
van fer fallar l'Action (secció 2.18).

### 2.18 Sessió 18 · El build ja no deixa PDF orfes, i tries a tota la unitat 8

**La fallada.** El primer Run workflow després de la sessió 17 es va aturar al pas «Un build que
falla no escriu res», amb el missatge «un build correcte escriu els 524 PDF: 464 de 524 escrits».
La prova fa un build complet sobre una còpia del repositori i comprova que s'han reescrit tots
els PDF de `out/`. Al repositori hi havia els 60 PDF de previsualització dels 16 ítems retirats a
la sessió 17 (2 o 4 per ítem), que ja no genera cap font: $524-464=60$. Es va reproduir aquí
afegint-hi aquests 60 fitxers, i va sortir el mateix missatge. La sessió 17 els havia donat per
inofensius, i n'havia proposat la neteja com a opcional i per després del Run workflow. A la
màquina de treball la prova passava perquè no hi havia els PDF de la sessió 16. En aquell moment,
la neteja manual amb `git rm` ho va resoldre.

**L'arranjament permanent.** Un build complet, i només si no hi ha hagut cap error, esborra de
`out/` els PDF que no surten al catàleg que acaba de generar, i també les carpetes que hi queden
buides. Amb `--pregunta` o `--nomes-cataleg` no n'esborra cap, perquè aquell build no ha mirat
totes les fonts. `prova_sortida.py` en té tres comprovacions noves (14 en total): un build fallit
no esborra cap orfe, un build complet sí (i també les carpetes buides), i `--pregunta` no. Es van
fer dos controls: amb els 60 orfes reals, la prova passa; i amb l'esborrat desactivat, la
comprovació nova falla.

Queda una limitació. El pas «Desa» de l'Action només fa `git add` dels fitxers que existeixen, de
manera que un esborrat fet a la màquina de l'Action no arriba al repositori. L'Action ja no falla,
però els orfes s'hi quedarien. Es resol amb una línia de `compila.yml` (secció 11), que cal
canviar a mà perquè el bot no pot escriure a `.github/workflows/`. La línia nova es va provar en
un repositori simulat: registra els canvis, els PDF nous i els esborrats, i deixa fora les fonts.

**Tries a la u8.** Les 18 preguntes, amb el criteri de la regla 16 des del principi: cap
alternativa no és un canvi de nombres.

| Tema | Què demana l'alternativa |
|---|---|
| `derivada-definicio` | q001, reconèixer un límit com la derivada d'una funció en un punt (`reconeix-limit`); q002, una funció contínua i no derivable, $\lvert x-3\rvert$ (`no-derivable`); q003, la derivabilitat d'una funció a trossos per la definició, que aquesta vegada sí que ho és (`trossos-derivable`) |
| `tvm-derivada-punt` | q001, $f'(a)$ en un punt qualsevol per la definició, i on la tangent és horitzontal (`derivada-general`); q002, la TVM a la inversa, trobant l'interval (`tvm-inversa`); q003, velocitats mitjanes en intervals cada vegada més petits, com a aproximació de la instantània (`aproximacio-numerica`) |
| `regles-derivacio` | q001, les regles amb valors, sense fórmules (`regles-amb-valors`); q002, reescriure com a suma de potències per no fer servir el quocient (`simplifica-abans`); q003, trobar l'error d'un alumne (`troba-error`) |
| `regla-cadena` | q001, la cadena amb valors (`composicio-amb-valors`); q002, les propietats dels logaritmes abans de derivar (`log-propietats`); q003, descompondre una composició de tres funcions (`composicio-triple`) |
| `recta-tangent` | q001, les tangents en $x=a$ i $x=-a$ són paral·leles, i per què (`tangents-simetriques`); q002, el punt on la tangent passa per un punt donat (`tangent-per-punt`); q003, les dues tangents des d'un punt exterior (`punt-exterior`) |
| `tangent-condicions` | q001, quins pendents són possibles (`pendents-possibles`); q002, cap tangent de pendent positiu (`pendent-negatiu`); q003, les tangents que passen per l'origen (`tangents-per-origen`) |

Les de `recta-tangent` i `tangent-condicions` segueixen patrons de la PAU: la tangent en un punt
genèric (23s-q2), la que passa per un punt donat (24i-q3) i el punt on té un pendent donat
(25j-q1, 26j-q1). Abans d'escriure-les, es va llegir cada pregunta sencera, per no repetir cap
altre apartat i per no fer servir un nom de funció que ja designés una altra funció a la mateixa
pregunta. Per això `regles-derivacio/q001` i `regla-cadena/q001` parlen de $u$ i $v$, i
`derivada-definicio/q002` de $g$.

**Verificació.** Totes les matemàtiques es van comprovar amb SymPy abans d'escriure-les. Cada
fitxer té el defecte idèntic byte a byte i suma 2,50 punts amb cada ítem, a totes dues durades.
Tot el banc es va compilar amb el preàmbul reduït: 608 PDF (144 de nous), cap error ni
*Overfull*, i cinc previsualitzacions de la u8 revisades a ull. Les bateries (38/14/77) i la
integració amb jsdom passen. Dues proves depenien d'una pregunta de la u8 sense tria (el cas 4 de
`prova_sortida.py` i el cas 7 de la prova amb jsdom), i ara fan servir `u9/monotonia-extrems/q001`.

### 2.19 Sessió 19 · Tries a la unitat 9, i unitats plegables

**Unitats plegables.** El professor va demanar que la llista de temes es pogués plegar i
desplegar per unitats. El títol de cada unitat és ara un botó que plega o desplega els seus temes
(amb `aria-expanded`). Plegada, la unitat diu quantes preguntes seves hi ha a l'examen, perquè no
es perdin de vista. L'estat es desa a la memòria del navegador (`localStorage`), i no a l'adreça,
perquè és una preferència de qui fa els exàmens, no part de l'examen. Si el navegador no la deixa
fer servir, com fan alguns amb un fitxer local, tot surt desplegat com abans, i una memòria mal
formada tampoc no trenca res. En tornar a pintar la llista, el focus torna al títol clicat, per a
qui navega amb el teclat. La prova amb jsdom en té dotze comprovacions noves.

**La u9 a la PAU.** De 2023 a 2026, la u9 és el bloc que més hi surt. Hi ha optimització en nou
exercicis, sovint amb el model donat («comproveu que el cost ve donat per…»); paràmetres a partir
de condicions (23j-q1, 23j2-q6, 25s-q3c); monotonia i extrems d'una funció donada (24j-q1,
25i-q1), o raonats sense calcular els punts crítics (24i-q1); i els punts crítics d'una funció
llegits a la gràfica de la seva derivada (26j2-q4a).

**Tries a la u9**, amb el criteri de la regla 16:

| Tema | Què demana l'alternativa |
|---|---|
| `curvatura-inflexio` | q001, una $f''$ que s'anul·la sense canviar de signe: cap inflexió (`falsa-inflexio`); q002, els coeficients a partir de la recta tangent en el punt d'inflexió, com a la 23j-q1 (`tangent-inflexio`); q003, creuar les taules de $f'$ i $f''$: on és alhora creixent i còncava (`creix-i-corba`) |
| `extrems-parametres` | q001, per a quins valors del paràmetre no hi ha cap extrem (`sense-extrems`); q002, la curvatura de $f$ llegida a la gràfica de $f'$ (`curvatura-de-fprima`); q003, els paràmetres a partir d'un context de beneficis, amb un màxim i una inflexió, com a la 25s-q3c (`beneficis-context`) |
| `monotonia-extrems` | q001, exactament una solució: Bolzano per a l'existència i monotonia per a la unicitat, com a la 24s-q1 (`una-sola-arrel`); q002, monotonia sense derivar, i per què l'argument no sempre serveix, com a la 24i-q1 (`sense-derivar`); q003, un quocient amb logaritme, com a la 24j-q1 (`quocient-logaritme`) |
| `optimitzacio` | q001, un altre objectiu, el perímetre en lloc de l'àrea (`perimetre-maxim`); q002, quins volums són possibles, i de quantes maneres (`volums-possibles`); q003, un costat de tanca més car, que fa que el prat òptim sigui quadrat (`tanca-mes-cara`) |

**El parany de l'optimització.** Els apartats hi van encadenats: el model, l'optimització i, al
`nomesllarg`, «justifica que el valor trobat és un màxim». Una alternativa que canviés el model
trencaria la cadena. Per això la tria va al pas d'optimitzar, i a totes tres el valor que es troba
continua sent un màxim en un punt on s'anul·la la derivada, perquè el `nomesllarg` hi continuï
tenint sentit. Es va descartar, per exemple, un màxim a la frontera del domini, que hauria deixat
sense sentit la justificació amb la derivada segona. Pel mateix motiu, l'alternativa de
`curvatura-inflexio/q002` dona una funció que també té un extrem en $x=3$, que és el que demana
el seu `nomesllarg`.

**Una prova que ja no depèn de les tries.** El cas 4 de `prova_sortida.py` esperava exactament 4
PDF d'una pregunta concreta, i cada vegada que aquella pregunta rebia una tria calia moure'l a una
altra (de la u7 a la u8, i de la u8 a la u9). Ara comprova que `--pregunta` només escriu PDF
d'aquella pregunta i que hi són els quatre de base, tant si té tries com si no.

**Verificació.** Totes les matemàtiques es van comprovar amb SymPy abans d'escriure-les, i cada
fitxer té el defecte idèntic byte a byte i 2,50 punts amb cada ítem, a totes dues durades. Les 12
preguntes de la u9 es van compilar de debò, una per una, amb el preàmbul reduït: 144 PDF (96 de
nous), cap error ni *Overfull*. El build complet ja no cap en el límit de cinc minuts per ordre de
l'entorn de treball, però la u7 i la u8 no han canviat des de la compilació completa de la sessió
18, i el build complet de `prova_sortida.py`, amb el `pdflatex` fals, confirma que el banc escriu
704 PDF. Les bateries (38/14/77) i la integració amb jsdom passen, i el cas 4 reescrit té la seva
prova de control: si `--pregunta` escrivís PDF d'altres preguntes, fallaria.

### 2.20 Sessió 20 · La u10 amb els exercicis practicats de debò, i domini i punts de tall

**El material.** El professor va passar dos recursos. El primer és el solucionari de Santillana de
la unitat 10 sencera: pàgines 377–460 del llibre, exercicis 1 a 124, amb enunciats, solucions i
gràfiques. El segon és el full de feina de Classroom, on les caselles D12 i D13 diuen quins
exercicis hauran practicat els alumnes abans de l'examen. Es va mantenir la regla de sempre (el
banc no surt dels exercicis practicats), i el solucionari s'usa com a font de tipus d'exercici i de
funcions, no per copiar-ne els enunciats.

**Els exercicis practicats, corregits.** La sessió 13 comptava 16 exercicis assignats, de les
setmanes 11, 12 i 17. El full diu que la setmana 17 (84, 108, 123 i 124) cau al gener, després de
l'examen, i que els practicats abans són **12**: el 37, el 38, el 43, el 45, el 62 i el 63 (setmana
11), i el 41, el 75, el 78, el 88, el 91 i el 100 (setmana 12). Llegits al solucionari:

| Tema | Exercicis practicats |
|---|---|
| `domini-talls` | 43 (dominis de totes les famílies), 45 (domini i talls), 100 (funcions amb radicals) |
| `asimptotes` | 62 (branques infinites de polinomis), 63 (asímptotes verticals, horitzontals i obliqües), 38 (dibuixar una funció a partir de propietats) |
| `estudi-racional` | 41 i 91 (estudis complets), 63, 75, 78 |
| `estudi-polinomica` | 75, 78, 88 (coeficients a partir d'un extrem, una inflexió i un punt), 62 |
| `estudi-trossos` | **cap** |

Tres conseqüències. `estudi-polinomica/q001` citava el 84 i ara cita el 75, el 78 i el 88. El tema
`estudi-trossos` no té cap exercici practicat al darrere: la seva q001 cita el 108 (setmana 17) i
el 37, però el 37 no és de funcions a trossos, sinó que demana llegir les característiques de $f$ a
la gràfica de $f'$. Queda pendent de decidir què se'n fa (7.4). La proposta de la sessió anterior
d'aprofitar el 123 i el 124 com a models de context queda retirada, perquè són de la setmana 17.

**El solucionari té errors.** Al 41 diu que $f'(x)<0$ fa la funció creixent; al 75a, $y'>0$ on ha
de dir $y'<0$; al 75d li falta el punt crític $x=18$; i al 78b dona $\mathrm{Dom}=\mathbb{R}$ per a
$\frac{x-2}{x+2}$. Serveix de referència, però tot es continua verificant amb SymPy.

**Domini i punts de tall, complet.** Dues variants noves, q002 i q003, amb l'estructura de la
q001 i funcions dels tipus del 43, el 45 i el 100: un denominador sense zeros, un logaritme d'un
polinomi de segon grau, una exponencial amb exponent fraccionari i els talls d'una funció amb
radical. Hi ha una tria a cadascuna de les tres preguntes: un zero del numerador que **no** és un
tall, perquè no és del domini (q001, `tall-fals`); jutjar l'error d'un alumne que simplifica abans
de trobar el domini (q002, `error-simplificar`); i el domini segons un paràmetre, amb la diferència
entre $<$ i $\le$ per a una arrel (q003, `domini-parametre`).

**Verificació.** Totes les matemàtiques es van comprovar amb SymPy. Les tres preguntes tenen el
defecte idèntic, 2,50 punts amb cada ítem, i compilen de debò a una pàgina, sense errors. Les
bateries (38/14/77) i la integració amb jsdom passen, i el banc complet escriu 736 PDF.

### 2.21 Sessió 21 · Asímptotes, i el tema de funcions a trossos, congelat

**La decisió sobre les funcions a trossos.** El professor va decidir deixar
`estudi-trossos/q001` tal com és (sense tria i amb el seu `origen`) i no ampliar el tema fins que
s'hagi fet la setmana 17. La pregunta es pot continuar fent servir, però cap exercici practicat abans
de l'examen no la sosté (2.20).

**Asímptotes, complet.** Dues variants noves, q002 i q003, amb l'estructura de la q001 i funcions
dels tipus del 62, el 63 i el 38: dues asímptotes verticals i una d'horitzontal (una de les dues
variants amb $y=0$), una obliqua trobada dividint, i dibuixar una funció a partir de propietats
donades. En una de les funcions els dos laterals de l'asímptota vertical valen $+\infty$; l'altra té
una asímptota obliqua. Les dues gràfiques noves es van revisar a ull: els extrems, $(-2,-3)$ i
$(0,1)$, i les branques que s'acosten a les asímptotes hi són on toca.

Hi ha una tria a cadascuna de les tres preguntes. A la q001 (`forat-no-asimptota`), un zero del
denominador que **no** és una asímptota, perquè el factor es cancel·la i el límit és finit. A la q002
(`talla-asimptota`), una gràfica que talla la seva asímptota horitzontal, i per què una vertical no es
pot tallar. A la q003 (`branques-polinomi`), les branques infinites d'un polinomi, i per què cap
polinomi de grau 2 o més no té asímptotes, com a l'exercici 62.

**Verificació.** Totes les matemàtiques es van comprovar amb SymPy, inclosos els punts on les
gràfiques surten del marc. Les tres preguntes tenen el defecte idèntic i 2,50 punts amb cada ítem, i
compilen de debò a una pàgina, també les solucions amb gràfica. Les bateries (38/14/77) i la
integració amb jsdom passen, i el banc complet escriu 768 PDF.

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
| Una tria substitueix l'apartat sencer: `\begin{tria}` amb `\itemtria` complets, mai una llista d'ítems parcials | Disseny, a partir d'un exemple del professor | Els tres canvis de l'exemple («quants ítems», «amb subtasca o sense» i «una alternativa sencera») són el mateix cas: un cos complet en lloc d'un altre |
| Sense selecció, es materialitza sempre el primer ítem declarat | Disseny | El `.tex` de les preguntes que ja hi eren no canvia ni un byte |
| Les tries són només per a preguntes del banc, mai per a PAU | Professor, seguint una regla ja existent | L'enunciat PAU ha de ser literal |
| Els ítems d'una tria es preparen i es verifiquen sempre pel build, com qualsevol pregunta | Professor | El lloc només ofereix triar-los, no escriure'n cap al vol sense passar-hi |
| Una tria no pot ser dins d'un `nomesllarg` | Disseny | Encara no es controla bé com afecta el recompte de punts d'`app.js`; es fa fallar el build en lloc de deixar-ho a mig fer |
| Cada ítem d'una tria té la seva previsualització compilada pel build, no compilada en directe al navegador | Disseny | Compilar LaTeX al navegador exigiria un motor nou (una dependència grossa) o un servidor; el build ja sap compilar-ne el cos |
| Una alternativa ha de canviar el cas, la tècnica o el sentit del raonament, no només els nombres (regla 16) | Professor | Una tria amb la mateixa pregunta i altres xifres no aporta res a l'examen |
| Les alternatives noves porten identificadors nous; els retirats no es reaprofiten | Regla 13 | Una adreça desada que en porti un de vell cau al defecte, i no a un contingut diferent |
| `estudi-trossos` es queda com està (la q001, sense tria) i no s'amplia fins que s'hagi fet la setmana 17 | Professor | Cap exercici practicat abans de l'examen no el sosté |
| Per a la u10, els exercicis practicats són els de les setmanes 11 i 12 del full de Classroom; la setmana 17 és posterior a l'examen | Professor | El banc no surt dels exercicis que els alumnes hauran practicat |
| El solucionari del llibre és una referència, no la veritat: tot es verifica amb SymPy | Disseny | S'hi han trobat quatre errors (2.20) |
| Les unitats de la llista de temes es pleguen des del seu títol, i l'estat es desa al navegador, no a l'adreça | Professor (el plegat) i disseny (on es desa) | És una preferència de qui fa els exàmens, no part de l'examen |
| A optimització, la tria va al pas d'optimitzar i no al model, i el valor trobat continua sent un màxim en un punt crític | Disseny | Els apartats hi van encadenats, i el `nomesllarg` justifica el màxim amb la derivada |
| El cas 4 de `prova_sortida.py` no depèn de si la pregunta té tries | Disseny | Si no, calia moure'l cada vegada que una unitat rebia tries |
| Un build complet esborra de `out/` els PDF que ja no genera cap font; un build amb `--pregunta`, no | Disseny, arran d'una fallada (2.18) | `out/` és generat i ha de reflectir les fonts; un build parcial no les ha mirades totes |

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
| Un `defecte-curt` que apuntés a un ítem inexistent ja registrava l'error, però després petava amb un `KeyError` en lloc de continuar net | `build.py` | Es descarta i cau al primer ítem, un cop registrat l'error |
| Un `\itemtria` amb l'identificador mal format no feia `match` i el seu contingut desapareixia en silenci, en lloc de fer fallar el build | `build.py` | Comptatge laxa (`\itemtria\b`) contra el comptatge estricte: si no coincideixen, error |
| Una tria sense cap `\itemtria` ja registrava l'error, però petava amb un `IndexError` en construir el catàleg (`t.ordre[0]` d'una llista buida) | `build.py` | Es descarten del catàleg les tries sense ítems; l'error ja enviat atura el build igualment |
| `prova_sortida.py` comptava els PDF amb un patró de quatre nivells fixos (`*/*/*/out/*.pdf`): no veia mai els de `out/tries/…`, i per tant no en provava res | `prova_sortida.py` | Patró recursiu (`*/*/*/out/**/*.pdf`) als dos llocs on apareixia |
| Els PDF orfes dels ítems retirats es van donar per inofensius, i en feien fallar `prova_sortida.py` (464 de 524) | `build.py` | Un build complet esborra els PDF que ja no genera cap font (2.18) |

| La u10 comptava com a practicats els exercicis de la setmana 17 (84, 108, 123 i 124), posterior a l'examen, i `estudi-polinomica/q001` citava el 84 | `meta.json`, handout | Corregit amb el full de Classroom; `estudi-trossos` queda pendent (7.4) |

---

## 5. Què està verificat i què no

**Verificat:**

- Les respostes de les 13 preguntes de la u7, amb càlcul simbòlic i un segon mètode per a
  tots els límits a l'infinit.
- 32 resultats dels criteris oficials de juny de 2026, per un mètode independent.
- `prova_validacio.py`: 38 avaries provocades, cadascuna rebutjada pel build. Les 8 de la
  sessió 6 són de les modalitats, i les 9 de la sessió 14 són de les tries.
- `prova_sortida.py`: 14 comprovacions, sense TeX (un `pdflatex` fals al PATH). Un build que
  falla, per validació o per compilació, no toca cap fitxer. Un de correcte els escriu tots, i esborra els
  que ja no genera cap font (608, comptats amb un patró recursiu que ara arriba a `out/tries/…`),
  `--pregunta` només escriu els de la pregunta indicada —també les previsualitzacions de tria,
  quan n'hi ha— i `--preambul` no arriba al catàleg. També s'ha confirmat amb el `pdflatex` real.
- `prova_paritat.py`: 77 comprovacions. El lloc (executant l'`app.js` real) i el build
  munten el mateix `.tex`, byte a byte, també amb preguntes PAU, amb la procedència al lloc
  exacte, amb opcions (1, 2, 3, 4a, 4b) i amb tries triades amb `triaCanvia`. Tres adreces mal
  formades s'ignoren sense que la
  pàgina peti. Les accions de les targetes (afegir, moure, treure, marcar opció, canviar de
  variant, triar un ítem) donen les etiquetes, els punts i l'adreça esperats. Cinc clics donen per defecte
  1, 2, 3, 4a i 4b, també en un examen que combina temes i PAU. A 50 min, el lloc i el build
  munten el mateix `.tex`, i els minuts i l'adreça segueixen la modalitat.
- En un Chromium real: selecció, variants, adreça, recàrrega, descàrregues, secció PAU,
  adreces mal formades i l'examen de la PAU de 2026 muntat amb clics (1, 2, 3, 4a, 4b), també
  a 390 px d'amplada. El seu `main.tex` compila en 2 pàgines, i el de solucions en 5, sense cap
  *Overfull*. També un examen combinat (Límits en un punt, Anàlisi, Bolzano, Probabilitat i
  Geometria), amb ✕ i ▲ entremig: 2 pàgines i 4 amb solucions, sense cap *Overfull*.
- Sessió 19: les 12 tries de la u9, comprovades amb SymPy abans d'escriure-les, amb el defecte
  idèntic byte a byte i 2,50 punts amb cada ítem. Les 12 preguntes de la u9 compilades de debò
  (144 PDF, cap error ni *Overfull*), i el banc sencer amb el `pdflatex` fals (704 PDF). Les
  unitats plegables, amb dotze comprovacions noves a jsdom.
- Sessió 18: les 18 tries de la u8, comprovades amb SymPy abans d'escriure-les, amb el defecte
  idèntic byte a byte i 2,50 punts amb cada ítem. Tot el banc compilat (608 PDF, cap error ni
  *Overfull*). L'esborrat dels orfes, amb el cas real (60 orfes) i un control negatiu.
- Sessió 17: les 16 alternatives noves, comprovades amb SymPy abans d'escriure-les. Un cop
  escrites, cadascuna té el defecte idèntic byte a byte i suma 2,50 punts amb cada ítem triat,
  a totes dues durades. Tot el banc compilat amb el preàmbul reduït (464 PDF, cap error ni
  *Overfull*), i quatre previsualitzacions revisades a ull. Les bateries (38/11/77) i la
  integració amb jsdom passen sense canvis.
- Sessió 16: les 24 preguntes de la u7 amb tries, compilades amb el preàmbul reduït (436 PDF,
  168 de nous respecte de la sessió 15): cap error, cap *Overfull*, totes a una pàgina, els
  mateixos punts de defecte d'abans de migrar-les. Cada funció, límit i solució nous, verificats
  numèricament amb Python (i SymPy per a les factoritzacions) abans d'escriure'ls. Dues
  fixtures pròpies (`prova_sortida.py`) i dos supòsits de la prova d'integració amb jsdom
  necessitaven posar-se al dia perquè dues preguntes que fins ara servien de referència
  (`parametres-ab/q001`, `limits-punt/q001`) havien canviat de forma; corregits sense canviar
  què comprovaven.
- Sessió 15: les previsualitzacions de `limits-grafica/q001` i `limits-infinit/q002`
  compilades amb el preàmbul reduït i revisades visualment («avalua imatges» hi surt amb
  l'enunciat i la solució senceres, en blau). Quatre casos nous a la prova d'integració amb
  jsdom (12 en total): els botons Enunciat/Solució de cada tria mostren l'ítem triat, no el
  defecte; canviar d'ítem amb el visor obert l'actualitza sol; l'altra tria de la mateixa
  pregunta no s'hi veu afectada. Tot el banc (268 PDF, 22 de nous) recompilat sense cap
  regressió.
- Sessió 14: les dues preguntes migrades (`limits-infinit/q002`, `limits-grafica/q001`)
  compilen amb un preàmbul reduït (aquest entorn no té `lmodern` ni `babel`-català) amb el
  defecte de cada modalitat i amb quatre combinacions més, cadascuna a una pàgina i sense cap
  error — inclosa exactament la selecció que el professor havia fet a mà. Comprovat, també amb
  aquest preàmbul reduït, que les 64 preguntes recompilen sense cap regressió (246 PDF, abans
  de la sessió 15). Una
  prova d'integració amb jsdom (clics reals sobre el DOM, no formal al repositori), 8 casos, hi
  va detectar un error de càlcul de la pròpia prova (l'apartat `nomesllarg` de
  `limits-infinit/q002` segueix comptant a 1 h 30 en triar `quatre-tipus`); corregit, tots vuit
  hi passen.
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
- **Limitació de la sessió 14, resolta a la 15:** l'Enunciat i la Solució d'una carta amb
  tries mostraven sempre el defecte, mai la selecció feta —es triava a cegues—. Des de la
  sessió 15, cada tria té el seu propi Enunciat i Solució, de només l'ítem triat (2.15). El que
  en queda: l'Enunciat i la Solució **de la pregunta sencera**, més avall a la mateixa carta,
  continuen mostrant el defecte, perquè generar-ne un PDF a mida de cada combinació possible
  d'una pregunta amb més d'una tria (com `limits-infinit/q002`) creixeria amb el producte
  d'ítems de totes les seves tries, no només amb la suma. Amb els ítems previsualitzats un a
  un, per ara no calia.

---

## 6. Inventari

### 6.1 Unitat 7 · Límits i continuïtat (24 preguntes)

Tres variants per tema: se'n poden muntar tres exàmens diferents. Totes a mida PAU, amb la
versió de 50 min. Els minuts són estimacions (1 h 30 · 50 min) i s'han de calibrar amb dades
reals (vegeu 7.4). Els punts de la taula són sempre els del defecte: **les 24 preguntes**
ofereixen, a més, una tria en algun apartat (sessions 14 i 16, seccions 2.14 i 2.16), que no
hi canvia res mentre no es toqui des de la carta.

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

Les 18 preguntes ofereixen una tria en algun apartat (sessió 18, secció 2.18). Els punts de la
taula són els del defecte.

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

Les 12 preguntes ofereixen una tria en algun apartat (sessió 19, secció 2.19). Els punts de la
taula són els del defecte.

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

Cinc temes. Els exercicis practicats abans de l'examen són els de les setmanes 11 i 12 (2.20):
domini (43, 45, 100), asímptotes (62, 63, 38), representació (41, 75, 78, 88, 91) i llegir $f$ a la
gràfica de $f'$ (37). El tema de funcions a trossos no en té cap: el seu únic exercici, el 108, és de
la setmana 17. Domini i punts de tall i asímptotes ja tenen tres variants, totes amb tria. Els estudis de racionals i
de polinòmiques en tenen una (vegeu 7.4), i el de funcions a trossos es queda com està fins que s'hagi
fet la setmana 17 (2.21).

| Tema | Codi | Títol | 1 h 30 | 50 min | Minuts | Dif. | Llibre |
|---|---|---|---|---|---|---|---|
| Asímptotes i branques infinites | `q001` | Asímptotes de funcions racionals i gràfica a partir d'unes asímptotes donades | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 62, 63, 38 |
| Asímptotes i branques infinites | `q002` | Dues asímptotes verticals, una obliqua i una gràfica amb els dos laterals a +∞ | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 62, 63, 38 |
| Asímptotes i branques infinites | `q003` | Asímptota horitzontal y = 0, una obliqua i una gràfica a partir d'una asímptota obliqua | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 62, 63, 38 |
| Domini i punts de tall | `q001` | Domini de racionals, radicals i logaritmes, i punts de tall | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●○○ | 43, 45, 100 |
| Domini i punts de tall | `q002` | Domini de racionals, radicals i logaritmes, i talls d'una racional amb denominador sense zeros | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●○○ | 43, 45, 100 |
| Domini i punts de tall | `q003` | Domini amb exponencials i radicals, i talls d'una funció amb radical | 0,75 + 1,00 + 0,75 | 1,25 + 1,25 | 18 · 11 | ●○○ | 43, 45, 100 |
| Estudi i gràfica d'una funció a trossos | `q001` | Estudi i gràfica d'una funció a trossos amb asímptota horitzontal | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 108, 37 |
| Estudi i gràfica d'una funció polinòmica | `q001` | Estudi i gràfica de x³−3x²+4: talls amb arrel doble, extrems i inflexió | 1,00 + 0,75 + 0,75 | 1,25 + 1,25 | 20 · 12 | ●●○ | 75, 78, 88 |
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
- Llista de temes plegable: **fet** a la sessió 19, per unitats (2.19). Al mòbil, encara es
  podria plegar tota la llista d'un sol cop.
- Els noms de les unitats apareixen en passar el ratolí per sobre, i això no funciona en
  pantalles tàctils. Cal mostrar-los d'una altra manera.
- **Estendre les tries a la resta del banc.** Des de la sessió 16, les 24 preguntes de la u7
  ja en tenen, i des de la 17 totes canvien el cas, la tècnica o el sentit del raonament
  (regla 16). Des de la 18, també les 18 de la u8, i des de la 19, les 12 de la u9. Queda la u10: des de la 20, domini i punts de tall ja en té, i des de la 21, les
  asímptotes. Falten els estudis de racionals i de polinòmiques (el de funcions a trossos és congelat
  fins després de la setmana 17), amb el mateix mètode: llegir la
  pregunta sencera, verificar l'alternativa abans d'escriure-la i verificar el fitxer just
  després. A la u7 encara s'hi podrien afegir, com a ítems nous, els límits no racionals que surten
  a la PAU ($\frac{\ln x}{x}$, o $(x-1)\ln x$ a $0^+$) o una gràfica a la inversa: «dibuixa una
  funció compatible amb aquests límits».
- **PDF de la pregunta sencera amb una combinació concreta.** Des de la sessió 15, cada ítem
  ja té el seu propi PDF (2.15); el que encara falta és un PDF de tota la pregunta muntada amb
  una combinació concreta de totes les seves tries alhora, útil per a preguntes amb més d'una
  (com `limits-infinit/q002`). Creixeria amb el producte d'ítems de cada tria, no amb la suma:
  cal decidir si val la pena abans d'implementar-ho, o si previsualitzar-les una a una ja és
  suficient.
- **Ampliar `tria` a «triar-ne uns quants d'una llista»**, no només «triar-ne exactament un».
  Es va descartar a la sessió 14 (2.14) perquè cap exemple real ho demanava encara; si mai en
  calgués un, val la pena revisar primer si «un cos sencer diferent» ho continua resolent abans
  d'ampliar el mecanisme.

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
| Un PDF que ja no genera cap font (el d'un ítem retirat) fa fallar `prova_sortida.py` | Un build complet l'esborra (2.18); perquè l'esborrat arribi al repositori, el pas «Desa» ha de fer `git add -A` (secció 11) |

---

## 11. Aquest lliurament

És el lliurament de la sessió 21. Parteix del de la sessió 20, que ja és al repositori.

| Fitxer | Canvi |
|---|---|
| `u10/asimptotes/q002/`, `u10/asimptotes/q003/` | **Noves**: dues variants, `pregunta.tex` i `meta.json`, amb la gràfica a la solució |
| `u10/asimptotes/q001/pregunta.tex` | Tria nova, `forat-no-asimptota` |
| `README.md` | Estat |
| `handout.md` | Secció 2.21, i les seccions 3, 6.4, 7.5 i 11 |

No porta cap PDF ni `cataleg.js`. Després de pujar-lo a `_uploads`, cal fer **Run workflow**.
