/* ═══════════════════════════════════════════════════════════════════════
   Banc de preguntes — lògica del lloc.
   Vanilla. Cap dependència. Llegeix el global BANC de cataleg.js.

   L'EXAMEN
   És un marc de places que s'omplen per ordre: la primera pregunta triada
   va a la primera plaça, i així successivament. L'estructura diu quines
   places són una opció de l'anterior (l'alumne en respon una), i és de les
   PLACES, no de les preguntes: moure o treure preguntes no la desfà. Per
   defecte és la de la PAU: 1, 2, 3, 4a, 4b, vinguin d'on vinguin les
   preguntes (temes, PAU o totes dues coses). Els números no es guarden
   enlloc: es deriven de l'estructura, i per això mai no n'hi pot haver de
   repetits ni de forats.

   REGLES D'AQUEST FITXER
   1. L'assemblatge del .tex fa servir BANC.plantilla, el mateix fitxer
      que fa servir build/build.py. Aquí no hi ha cap plantilla escrita.
      El format viu a BANC.headers i BANC.defs (build/headers.tex i
      build/defs.tex): el lloc no en té cap còpia.
   2. Tot String.replace amb contingut LaTeX fa servir una FUNCIÓ com a
      substitut: amb una cadena, JavaScript interpretaria $$, $' i $&
      (freqüents en LaTeX) i corrompria el .tex sense avisar.
   3. Tot text que arriba del catàleg passa per esc() abans d'entrar a
      l'HTML: un títol com "f(x) per a x<2" no pot trencar la pàgina.
   4. L'adreça guarda codis estables (tema:q002), mai posicions.
   5. Cap adreça, per mal formada que sigui, pot trencar la pàgina: el que
      no s'entén s'ignora.
   6. Una mateixa pregunta no surt mai dues vegades en un examen.

   LA MODALITAT
   L'examen és d'1 h 30 (per defecte) o de 50 min. A 50 min, cada pregunta
   fa servir la seva versió de 50 min (punts, minuts i PDF propis) si en
   té; si no, hi va sencera. materialitza() deixa cada pregunta neta per a
   la modalitat: el .tex que es baixa diu exactament el que surt al PDF.

   LES TRIES
   Un apartat pot oferir més d'un ítem («tria»): 1 límit o 4, amb reflexió
   o sense, classificar la discontinuïtat o llegir imatges. build.py ja
   n'ha triat un per defecte per a cada modalitat —el .tex sense tocar res
   és idèntic al d'abans que existissin les tries—, i cada plaça de
   l'examen (`examen[k].seleccio`) hi pot dir un altre ítem, per tria de la
   pregunta, no de la pregunta i la tria d'una altra. materialitza() hi fa
   EXACTAMENT el mateix que build.py: un id que no existeix es descarta i
   es queda amb el defecte (regla 5).
   ═══════════════════════════════════════════════════════════════════════ */

// Sense prototip: així #__proto__ o #constructor no hi troben res. Amb {},
// hi trobarien les propietats d'Object i la pàgina petaria (regla 5).
const PER_TEMA = Object.create(null);
BANC.temes.forEach(t => { PER_TEMA[t.slug] = []; });
BANC.preguntes.forEach(p => { (PER_TEMA[p.tema] ||= []).push(p); });
Object.values(PER_TEMA).forEach(l => l.sort((a, b) => a.codi.localeCompare(b.codi)));

let examen = [];          // preguntes en ordre: { slug, i, seleccio }; i és
                           // l'índex dins PER_TEMA[slug]; seleccio (id de
                           // tria → id d'ítem) només hi porta les tries que
                           // el professor ha canviat del seu defecte
const visor = {};         // id de pregunta → 'enunciat' | 'solucio' | undefined

// estructura[k]: la plaça k és una opció de l'anterior? Per defecte, la de la
// PAU: la cinquena plaça és l'opció b de la quarta (1, 2, 3, 4a, 4b).
const estructura = [false, false, false, false, true];
const esOpcio = k => k > 0 && Boolean(estructura[k]);

let curt = false;         // modalitat: false = examen d'1 h 30, true = de 50 min
const durada = () => (curt ? 50 : 90);
const apartatsDe = q => (curt ? q.apartats_curt : q.apartats);
const minutsDe = q => (curt ? q.minuts_curt : q.minuts);
const pdfDe = (q, solucio) => (curt ? (solucio ? q.pdf_solucio_curt : q.pdf_curt)
                                    : (solucio ? q.pdf_solucio : q.pdf));

/** Idèntic a pdfDe(), però per a un ítem concret d'una tria: l'enunciat o la
 *  solució de NOMÉS aquesta alternativa, no de la pregunta sencera. Existeix
 *  perquè triar-la no sigui a cegues. */
const pdfDeItem = (it, solucio) => (curt ? (solucio ? it.pdf_solucio_curt : it.pdf_curt)
                                         : (solucio ? it.pdf_solucio : it.pdf));

/** L'ítem triat d'una tria: el de `seleccio` si en diu un i encara és un dels
 *  seus, si no el defecte de la modalitat actual. Mai en torna cap altra
 *  cosa (regla 5): una tria sense ítems no hauria d'existir (build.py ho
 *  rebutjaria), però es protegeix igualment. */
function itemTriat(t, seleccio) {
  const defecte = t.items.find(it => it.id === (curt ? t.defecte_curt : t.defecte_llarg)) || t.items[0];
  if (!seleccio || !Object.prototype.hasOwnProperty.call(seleccio, t.id)) return defecte;
  return t.items.find(it => it.id === seleccio[t.id]) || defecte;
}

/** Punts de cada apartat de `q`, després d'aplicar `seleccio`. Sense cap
 *  tria —la immensa majoria de preguntes— és exactament apartatsDe(q), sense
 *  cap càlcul de més. build.py construeix apartatsDe(q) posant primer els
 *  apartats normals i després les tries, en l'ordre en què hi apareixen: per
 *  això les últimes q.tries.length posicions són sempre les de les tries. */
function puntsSeleccio(q, seleccio) {
  const base = apartatsDe(q);
  const tries = q.tries || [];
  if (!tries.length) return base;
  const normals = base.length - tries.length;
  const deTries = tries.map(t => {
    const it = itemTriat(t, seleccio);
    return (curt ? it.curt : it.llarg) ?? 0;
  });
  return [...base.slice(0, normals), ...deTries];
}

// ── utilitats ────────────────────────────────────────────────────────
const $ = s => document.querySelector(s);
const num = n => n.toFixed(2).replace('.', ',');
const esc = s => String(s).replace(/[&<>"']/g,
  c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

function baixa(nom, text) {
  const url = URL.createObjectURL(new Blob([text], { type: 'text/plain;charset=utf-8' }));
  const a = Object.assign(document.createElement('a'), { href: url, download: nom });
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

/** Idèntic a munta() de build.py: mateixa plantilla, mateix ordre,
 *  cada marcador substituït un sol cop. */
function munta(cossos, solucions) {
  return BANC.plantilla
    .replace('%%SOLUCIONS%%', () => solucions ? '\\solucionstrue' : '\\solucionsfalse')
    .replace('%%PREAMBUL%%', () => BANC.preambul)
    .replace('%%COS%%', () => cossos.join('\n\n'));
}

/** Igual que a build.py: l'identificador d'una tria o d'un ítem és permanent,
 *  com q001 — minúscules, xifres i guions, començant per una lletra. */
const RE_TRIA = /\\begin\{tria\}\{([a-z][a-z0-9-]*)\}(?:\[defecte-curt=([a-z][a-z0-9-]*)\])?(.*?)\\end\{tria\}/gs;
const RE_ITEMTRIA = /\\itemtria\{([a-z][a-z0-9-]*)\}\{([^{}]*)\}(?:\{([^{}]*)\})?/g;

/** Idèntic a materialitza() de build.py: la versió d'una pregunta per a una
 *  modalitat i una selecció de tries, neta. Primer, cada tria es converteix
 *  en un \apartat{punts} normal amb el cos de l'ítem triat —el de `seleccio`
 *  per al seu identificador si n'hi ha i és un dels seus ítems, si no el
 *  defecte de la modalitat. Després, exactament com abans: a 50 min, fora
 *  els blocs nomesllarg i \apartat[x]{y} → \apartat{x}; a 1 h 30, fora només
 *  les línies del bloc i \apartat[x]{y} → \apartat{y}. */
function materialitza(tex, esCurt, seleccio) {
  seleccio = seleccio || Object.create(null);
  tex = tex.replace(RE_TRIA, (_, idTria, defecteCurt, cos) => {
    // Els punts es guarden tal com els ha escrit l'autor (la cadena bruta,
    // «0,5»): com amb \apartat[x]{y}, mai es recalculen, es reprodueixen.
    const posicions = [...cos.matchAll(RE_ITEMTRIA)];
    const ordre = posicions.map(p => p[1]);
    const bruts = Object.create(null);
    posicions.forEach(p => { bruts[p[1]] = [p[2], p[3]]; });   // id → [llarg, curt|undefined]
    if (!ordre.length) return '';
    const teDefecteCurt = defecteCurt !== undefined
      && Object.prototype.hasOwnProperty.call(bruts, defecteCurt);
    const defecte = (esCurt && teDefecteCurt) ? defecteCurt : ordre[0];
    let triat = seleccio[idTria];
    if (!Object.prototype.hasOwnProperty.call(bruts, triat)) triat = defecte;   // regla 5: mai trenca
    const [pLlarg, pCurt] = bruts[triat];
    const puntsBrut = esCurt ? (pCurt !== undefined ? pCurt : pLlarg) : pLlarg;
    const i = ordre.indexOf(triat);
    const inici = posicions[i].index + posicions[i][0].length;
    const final = i + 1 < posicions.length ? posicions[i + 1].index : cos.length;
    return `\\apartat{${puntsBrut.trim()}}` + cos.slice(inici, final);
  });
  const sortida = [];
  let dins = false;
  for (const linia of tex.split('\n')) {
    const net = linia.trim();
    if (net === '\\begin{nomesllarg}') { dins = true; continue; }
    if (net === '\\end{nomesllarg}') { dins = false; continue; }
    if (dins && esCurt) continue;
    sortida.push(linia);
  }
  return sortida.join('\n')
    .replace(/\\apartat\[([^\]]*)\]\{([^}]*)\}/g, (_, c, l) => `\\apartat{${esCurt ? c : l}}`)
    .replace(/\n{3,}/g, () => '\n\n');
}

/** Idèntic a cos_amb_capcalera() de build.py: capçalera, procedència PAU
 *  (si n'hi ha) i cos, ja net per a la modalitat de l'examen i la selecció
 *  de tries de la seva plaça. La procedència surt del catàleg, mai del .tex. */
const ambCapcalera = (q, etiqueta, seleccio) =>
  `\\encapcalament{${etiqueta}}\n`
  + (q.procedencia ? `\\procedencia{${q.procedencia}}\n` : '')
  + materialitza(q.tex, curt, seleccio).trim();

// ── l'examen ─────────────────────────────────────────────────────────
const preguntaDe = p => PER_TEMA[p.slug][p.i];

/** Les preguntes de l'examen, en ordre. */
const triades = () => examen.map(preguntaDe);

/** Variants d'un tema que ja són a l'examen, sense comptar la plaça `excepte`. */
const usades = (slug, excepte = -1) =>
  new Set(examen.filter((p, k) => k !== excepte && p.slug === slug).map(p => p.i));

/** Primera variant del tema que encara no és a l'examen, o -1. */
function primeraLliure(slug) {
  const u = usades(slug);
  return PER_TEMA[slug].findIndex((_, i) => !u.has(i));
}

/** Les places ocupades, agrupades per pregunta: cada grup és una pregunta i
 *  les seves opcions. La primera plaça sempre obre grup. */
function grups() {
  const g = [];
  examen.forEach((_, k) => { if (esOpcio(k)) g[g.length - 1].push(k); else g.push([k]); });
  return g;
}

/** Etiqueta de cada plaça: 1, 2, 3, 4a, 4b… */
function etiquetes() {
  const et = [];
  grups().forEach((g, n) => g.forEach((k, j) => {
    et[k] = `${n + 1}${g.length > 1 ? String.fromCharCode(97 + j) : ''}`;
  }));
  return et;
}

// ── estat a l'adreça ─────────────────────────────────────────────────
//   #analisi:ana-26j-q1,algebra:alg-26j-q2,analisi:ana-26j-q4a|geometria:geo-26j-q4b
//   #50min/limits-punt:q001,…   (examen de 50 min)
//   #limits-infinit:q002~limits-infinit-tipus=quatre-tipus;determina-a=sense-reflexio,…
// La coma separa preguntes; la barra uneix les opcions d'una mateixa
// pregunta (4a|4b); el ~ separa el codi de la selecció de tries, si n'hi ha
// alguna que no sigui la del defecte, i el ; hi separa cada tria=ítem. Les
// adreces antigues, sense cap d'aquests símbols, continuen valent tal qual:
// són exàmens d'1 h 30 sense cap tria personalitzada.
function llegeixHash() {
  let cru = location.hash.replace(/^#/, '');
  // Un % solt o una adreça retallada fan petar decodeURIComponent. Els slugs
  // i els codis són ASCII: si no es pot descodificar, es llegeix tal com és.
  try { cru = decodeURIComponent(cru); } catch { /* es queda sense descodificar */ }
  if (cru.startsWith('50min/')) { curt = true; cru = cru.slice('50min/'.length); }
  cru.split(',').forEach(grup => {
    let primera = true;
    grup.split('|').forEach(tros => {
      const [slug, codiSeleccio] = tros.split(':');
      const [codi, seleccioTxt] = (codiSeleccio || '').split('~');
      const llista = PER_TEMA[slug];
      if (!llista) return;
      let i = llista.findIndex(q => q.codi === codi);
      if (i >= 0 && usades(slug).has(i)) return;      // regla 6
      if (i < 0) i = primeraLliure(slug);              // codi desaparegut → la primera lliure
      if (i < 0) return;                               // tema buit o sense variants lliures
      // Un id de tria o d'ítem que ja no existeixi es descarta en pintar
      // (regla 5): aquí només cal separar-los, no validar-los.
      const seleccio = Object.create(null);
      (seleccioTxt || '').split(';').forEach(parell => {
        const [idTria, idItem] = parell.split('=');
        if (idTria && idItem) seleccio[idTria] = idItem;
      });
      estructura[examen.length] = !primera;            // la plaça que ocuparà
      examen.push({ slug, i, seleccio });
      primera = false;
    });
  });
}

function escriuHash() {
  const s = examen.map((p, k) => {
    const parells = Object.entries(p.seleccio || {});
    const sufix = parells.length ? '~' + parells.map(([t, id]) => `${t}=${id}`).join(';') : '';
    return (k ? (esOpcio(k) ? '|' : ',') : '') + `${p.slug}:${preguntaDe(p).codi}${sufix}`;
  }).join('');
  const h = (curt ? '50min/' : '') + s;
  history.replaceState(null, '', h ? '#' + h : location.pathname + location.search);
}

// ── accions ──────────────────────────────────────────────────────────
/** Un clic a un tema hi afegeix una pregunta: la primera variant lliure. */
function afegeix(slug) {
  const i = primeraLliure(slug);
  if (i < 0) return;
  examen.push({ slug, i, seleccio: Object.create(null) });
  pinta();
}

/** Treu la pregunta de la plaça k. Les de després pugen una plaça, i
 *  l'estructura es queda com era, perquè és de les places. */
function treu(k) {
  delete visor[preguntaDe(examen[k]).id];
  examen.splice(k, 1);
  pinta();
}

/** Intercanvia la pregunta de la plaça k amb la de la plaça k+pas.
 *  L'estructura no canvia: són les preguntes les que canvien de plaça. */
function mou(k, pas) {
  const j = k + pas;
  if (j < 0 || j >= examen.length) return;
  [examen[k], examen[j]] = [examen[j], examen[k]];
  pinta();
}

/** Converteix la plaça k en opció de l'anterior, o la hi torna a separar. */
function commutaOpcio(k) {
  if (k === 0) return;
  estructura[k] = !esOpcio(k);
  pinta();
}

/** Canvia, per a la pregunta de la plaça k, quin ítem s'usa a la tria
 *  `idTria`. Un id que no existeixi es descarta en pintar (regla 5): mai cal
 *  validar-lo aquí. */
function triaCanvia(k, idTria, idItem) {
  examen[k].seleccio[idTria] = idItem;
  pinta();
}

/** Passa a la variant següent (o anterior) del mateix tema que no sigui ja
 *  a l'examen (regla 6). Canvia de pregunta, i per tant la seva seleccio de
 *  tries es reinicia: la d'una variant no vol dir res per a una altra. */
function rota(k, pas) {
  const p = examen[k], n = PER_TEMA[p.slug].length, altres = usades(p.slug, k);
  for (let s = 1; s < n; s++) {
    const i = ((p.i + pas * s) % n + n) % n;
    if (altres.has(i)) continue;
    const obert = visor[preguntaDe(p).id];
    delete visor[preguntaDe(p).id];
    p.i = i;
    p.seleccio = Object.create(null);
    if (obert) visor[preguntaDe(p).id] = 'enunciat';
    pinta();
    return;
  }
}

function mostra(id, quin) {
  visor[id] = visor[id] === quin ? undefined : quin;
  pinta();
}

// ── pintat ───────────────────────────────────────────────────────────
// Unitats plegades a la llista de temes. És una preferència de qui fa els exàmens, no part de
// l'examen: no va a l'adreça, sinó a la memòria del navegador, si la hi deixa (obert com a
// fitxer local, alguns navegadors no la hi deixen; aleshores tot surt desplegat, com abans).
const plegades = new Set();
try { JSON.parse(localStorage.getItem('banc-plegades') || '[]').forEach(u => plegades.add(u)); }
catch { /* sense memòria del navegador: tot desplegat */ }
const desaPlegades = () => {
  try { localStorage.setItem('banc-plegades', JSON.stringify([...plegades])); } catch { /* res */ }
};

function pintaTemes() {
  const ul = $('#temes');
  ul.innerHTML = '';
  Object.entries(BANC.unitats).forEach(([u, info]) => {
    const temes = BANC.temes.filter(t => t.unitat === u);
    if (!temes.length) return;
    const plegada = plegades.has(u);
    // Plegada, la unitat encara diu quantes preguntes seves hi ha a l'examen.
    const triades = examen.filter(p => temes.some(t => t.slug === p.slug)).length;
    const cap = document.createElement('li');
    cap.className = 'grup' + (u === 'pau' ? ' grup-pau' : '');
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'grup-boto';
    b.setAttribute('data-unitat', u);
    b.setAttribute('aria-expanded', String(!plegada));
    b.title = plegada ? 'Desplega la unitat' : 'Plega la unitat';
    b.innerHTML = `<span class="fletxa" aria-hidden="true">${plegada ? '▸' : '▾'}</span>
      <span class="grup-text"><span class="grup-nom">${esc(info.nom)}</span> ${esc(info.subtitol)}</span>
      ${plegada && triades ? `<span class="grup-n">${triades} a l'examen</span>` : ''}`;
    b.onclick = () => {
      if (plegada) plegades.delete(u); else plegades.add(u);
      desaPlegades();
      pintaTemes();
      // El botó s'ha tornat a crear: el focus hi torna, per a qui navega amb el teclat.
      document.querySelector(`#temes .grup-boto[data-unitat="${u}"]`)?.focus();
    };
    cap.appendChild(b);
    ul.appendChild(cap);
    if (!plegada) temes.forEach(t => pintaTema(ul, t));
  });
}

function pintaTema(ul, t) {
  const n = PER_TEMA[t.slug].length;
  const dins = examen.filter(p => p.slug === t.slug).length;
  const li = document.createElement('li');
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'tema' + (dins ? ' tria' : '') + (n ? '' : ' buit');
  b.disabled = dins >= n;           // tema buit, o totes les variants ja hi són
  b.title = !n ? "Encara no hi ha cap pregunta d'aquest tema."
    : dins >= n ? "Totes les preguntes d'aquest tema ja són a l'examen."
    : t.descripcio;
  b.setAttribute('aria-label', `Afegeix una pregunta de ${t.nom} (${dins} de ${n} a l'examen)`);
  b.innerHTML = `<span class="marca" aria-hidden="true">${dins || (n ? '+' : '')}</span>
    <span class="tema-nom">${esc(t.nom)}</span>
    <span class="tema-n">${n}</span>`;
  b.onclick = () => afegeix(t.slug);
  li.appendChild(b);
  ul.appendChild(li);
}

function pintaCarta(k, etiqueta) {
  const p = examen[k], q = preguntaDe(p), llista = PER_TEMA[p.slug];
  const tema = BANC.temes.find(t => t.slug === p.slug);
  const esPau = Boolean(q.procedencia);
  const potRotar = llista.length - usades(p.slug, k).size > 1;
  const unitatsTxt = q.unitats.length
    ? q.unitats.map(u => `<abbr title="${esc(BANC.unitats[u]?.subtitol || '')}">${esc(u)}</abbr>`).join(' · ')
    : 'per definir';
  const punts = puntsSeleccio(q, p.seleccio);
  const div = document.createElement('div');
  div.className = 'carta' + (esPau ? ' pau' : '') + (esOpcio(k) ? ' opcio' : '');

  // Una tria per apartat: un <select> amb cada ítem i els seus punts a la
  // modalitat actual, i els seus propis Enunciat/Solució —de només aquella
  // alternativa, no de la pregunta sencera— perquè triar-la no sigui a
  // cegues. Sense cap tria (la immensa majoria de preguntes), això no pinta
  // res i la targeta queda exactament com abans.
  const tries = q.tries || [];
  const triesHtml = tries.map(t => {
    const actual = itemTriat(t, p.seleccio);
    const opcions = t.items.map(it =>
      `<option value="${esc(it.id)}"${it.id === actual.id ? ' selected' : ''}>`
      + `${esc(it.id.replace(/-/g, ' '))} (${num(curt ? it.curt : it.llarg)} punts)</option>`).join('');
    const clauVisor = `${q.id}:${t.id}`;
    const quinObert = visor[clauVisor];
    const visorHtml = quinObert ? (() => {
      const src = pdfDeItem(actual, quinObert === 'solucio');
      return `<div class="visor visor-tria">
        <iframe src="${esc(src)}#toolbar=0&amp;navpanes=0" title="${esc(t.id)}: ${esc(actual.id)}"></iframe>
        <div class="peu">Si el PDF no es veu incrustat,
          <a href="${esc(src)}" target="_blank" rel="noopener">obre'l en una pestanya</a>.</div>
      </div>`;
    })() : '';
    return `<div class="tria-apartat">
      <label><span>${esc(t.id.replace(/-/g, ' '))}:</span>
        <select data-tria="${esc(t.id)}">${opcions}</select></label>
      <span class="tria-visor-botons">
        <button type="button" class="secundari mini" data-tria-visor="${esc(clauVisor)}" data-quin="enunciat"
          aria-pressed="${quinObert === 'enunciat'}">Enunciat</button>
        <button type="button" class="secundari mini" data-tria-visor="${esc(clauVisor)}" data-quin="solucio"
          aria-pressed="${quinObert === 'solucio'}">Solució</button>
      </span>
      ${visorHtml}
    </div>`;
  }).join('');

  div.innerHTML = `
    <div class="carta-dalt">
      <span class="num">Pregunta ${esc(etiqueta)}</span>
      <span class="carta-tema">${esc(tema.nom)}</span>
      ${esPau ? `<span class="pau-badge">${esc(q.procedencia)}</span>` : ''}
      ${curt && !q.te_curt ? `<span class="sencera" title="No té versió de 50 min: hi va sencera.">sencera</span>` : ''}
      <span class="ordre">
        <button type="button" class="secundari" data-fer="amunt" aria-label="Puja-la" title="Puja-la" ${k === 0 ? 'disabled' : ''}>▲</button>
        <button type="button" class="secundari" data-fer="avall" aria-label="Baixa-la" title="Baixa-la" ${k === examen.length - 1 ? 'disabled' : ''}>▼</button>
        <button type="button" class="secundari" data-fer="treu" aria-label="Treu-la de l'examen" title="Treu-la de l'examen">✕</button>
      </span>
    </div>
    <div class="carta-titol">${esc(q.titol)}</div>
    ${tries.length ? `<div class="tries">${triesHtml}</div>` : ''}
    <div class="meta">
      <span>${punts.map(num).join(' + ')} = ${num(punts.reduce((s, a) => s + a, 0))} punts</span>
      <span>${esc(q.dificultat)}</span>
      <span>~${minutsDe(q)} min</span>
      ${esPau ? `<span>cal haver fet: ${unitatsTxt}</span>` : `<span>llibre: ${q.origen.map(esc).join(', ')}</span>`}
      <span>${esc(q.codi)}</span>
    </div>
    <div class="accions">
      <button type="button" class="secundari" data-fer="enunciat" aria-pressed="${visor[q.id] === 'enunciat'}">Enunciat</button>
      <button type="button" class="secundari" data-fer="solucio" aria-pressed="${visor[q.id] === 'solucio'}">Solució</button>
      <button type="button" class="secundari" data-fer="tex">.tex</button>
      ${k ? `<button type="button" class="secundari opcio-btn" data-fer="opcio" aria-pressed="${esOpcio(k)}"
        title="L'alumne respon aquesta pregunta o l'anterior: queden numerades com a 4a i 4b">Opció de l'anterior</button>` : ''}
      <span class="variant">
        <button type="button" class="secundari" data-fer="prev" aria-label="Variant anterior" ${potRotar ? '' : 'disabled'}>◀</button>
        <span>${p.i + 1}/${llista.length}</span>
        <button type="button" class="secundari" data-fer="next" aria-label="Variant següent" ${potRotar ? '' : 'disabled'}>▶</button>
      </span>
    </div>`;

  if (visor[q.id]) {
    const src = pdfDe(q, visor[q.id] === 'solucio');
    const v = document.createElement('div');
    v.className = 'visor';
    v.innerHTML = `<iframe src="${esc(src)}#toolbar=0&amp;navpanes=0" title="${esc(q.titol)}"></iframe>
      <div class="peu">Si el PDF no es veu incrustat,
        <a href="${esc(src)}" target="_blank" rel="noopener">obre'l en una pestanya</a>.</div>`;
    div.appendChild(v);
  }

  const fer = {
    enunciat: () => mostra(q.id, 'enunciat'),
    solucio:  () => mostra(q.id, 'solucio'),
    tex:      () => baixa(`${q.id.replace(/\//g, '-')}.tex`,
                          munta([ambCapcalera(q, `Q${etiqueta}`, p.seleccio)], false)),
    prev:     () => rota(k, -1),
    next:     () => rota(k, +1),
    amunt:    () => mou(k, -1),
    avall:    () => mou(k, +1),
    treu:     () => treu(k),
    opcio:    () => commutaOpcio(k),
  };
  div.querySelectorAll('button[data-fer]').forEach(b => { b.onclick = fer[b.dataset.fer]; });
  div.querySelectorAll('select[data-tria]').forEach(s => {
    s.onchange = () => triaCanvia(k, s.dataset.tria, s.value);
  });
  div.querySelectorAll('button[data-tria-visor]').forEach(b => {
    b.onclick = () => mostra(b.dataset.triaVisor, b.dataset.quin);
  });
  return div;
}

function pinta() {
  pintaTemes();

  const cont = $('#seleccio');
  cont.innerHTML = '';
  if (!examen.length) {
    cont.innerHTML = '<div class="cap">Tria temes a l\'esquerra: cada clic hi afegeix una pregunta. '
      + 'Les cinc primeres queden com a la PAU: 1, 2, 3, 4a i 4b.</div>';
  }
  const et = etiquetes();
  examen.forEach((_, k) => cont.appendChild(pintaCarta(k, et[k])));

  // Les opcions d'una mateixa pregunta compten una sola vegada: l'alumne en
  // respon una. Dels minuts, es compta la més llarga.
  const qs = triades(), gs = grups();
  const centDe = k => Math.round(puntsSeleccio(qs[k], examen[k].seleccio).reduce((s, a) => s + a, 0) * 100);
  const cent = gs.reduce((s, g) => s + Math.max(...g.map(centDe)), 0);
  const minuts = gs.reduce((s, g) => s + Math.max(...g.map(k => minutsDe(qs[k]))), 0);
  $('#recompte').innerHTML = qs.length
    ? `<span class="seg">${qs.length} ${qs.length === 1 ? 'pregunta' : 'preguntes'}</span>`
      + (gs.length < qs.length ? ` <span class="seg">(se'n responen ${gs.length})</span>` : '') + ' · '
      + `<span class="seg ${cent === 1000 ? 'just' : 'fora'}">${num(cent / 100)} punts</span> · `
      + `<span class="seg ${minuts > durada() ? 'fora' : ''}">~${minuts} de ${durada()} min</span>`
    : 'Cap pregunta triada';

  $('.durada').querySelectorAll('button[data-durada]').forEach(b => {
    b.setAttribute('aria-pressed', String((b.dataset.durada === 'curt') === curt));
  });
  $('#baixa-prova').disabled = !qs.length;
  $('#baixa-prova').textContent = `prova-${numProva()}.tex`;
  $('#baixa-tex').disabled = !qs.length;
  escriuHash();
}

// ── arrencada ────────────────────────────────────────────────────────
const cossosTriats = () => {
  const et = etiquetes();
  return triades().map((q, k) => ambCapcalera(q, `Q${et[k]}`, examen[k].seleccio));
};

/** Les peces d'un examen, en ordre: el segell de versió del format, la
 *  capçalera del centre i les preguntes. Van al prova-N.tex i, dins de la
 *  plantilla, al fitxer «tot en un». */
const pecesExamen = () => [`\\bancrequereix{${BANC.versio}}`, '\\capsaleraexamen', ...cossosTriats()];

const numProva = () => Math.max(1, parseInt($('#numprova').value, 10) || 1);

$('.durada').querySelectorAll('button[data-durada]').forEach(b => {
  b.onclick = () => { curt = b.dataset.durada === 'curt'; pinta(); };
});
$('#baixa-prova').onclick = () => baixa(`prova-${numProva()}.tex`, pecesExamen().join('\n\n') + '\n');
$('#baixa-tex').onclick = () => baixa('examen-sencer.tex', munta(pecesExamen(), false));
$('#numprova').oninput = () => { $('#baixa-prova').textContent = `prova-${numProva()}.tex`; };
$('.botons-entorn').querySelectorAll('button[data-entorn]').forEach(b => {
  b.onclick = () => baixa(`${b.dataset.entorn}.tex`, BANC[b.dataset.entorn]);
});
$('#segell').textContent = `${BANC.preguntes.length} preguntes · ${BANC.generat}`;

llegeixHash();
pinta();
