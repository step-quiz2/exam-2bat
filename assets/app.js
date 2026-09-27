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
   ═══════════════════════════════════════════════════════════════════════ */

// Sense prototip: així #__proto__ o #constructor no hi troben res. Amb {},
// hi trobarien les propietats d'Object i la pàgina petaria (regla 5).
const PER_TEMA = Object.create(null);
BANC.temes.forEach(t => { PER_TEMA[t.slug] = []; });
BANC.preguntes.forEach(p => { (PER_TEMA[p.tema] ||= []).push(p); });
Object.values(PER_TEMA).forEach(l => l.sort((a, b) => a.codi.localeCompare(b.codi)));

let examen = [];          // preguntes en ordre: { slug, i }; i és l'índex dins PER_TEMA[slug]
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

/** Idèntic a materialitza() de build.py: la versió d'una pregunta per a una
 *  modalitat, neta. A 50 min, fora els blocs nomesllarg i \\apartat[x]{y} →
 *  \\apartat{x}; a 1 h 30, fora només les línies del bloc i → \\apartat{y}. */
function materialitza(tex, esCurt) {
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
 *  (si n'hi ha) i cos, ja net per a la modalitat de l'examen. La procedència
 *  surt del catàleg, mai del .tex. */
const ambCapcalera = (q, etiqueta) =>
  `\\encapcalament{${etiqueta}}\n`
  + (q.procedencia ? `\\procedencia{${q.procedencia}}\n` : '')
  + materialitza(q.tex, curt).trim();

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
// La coma separa preguntes; la barra uneix les opcions d'una mateixa
// pregunta (4a|4b). Les adreces antigues, sense barres ni prefix, continuen
// valent: són exàmens d'1 h 30.
function llegeixHash() {
  let cru = location.hash.replace(/^#/, '');
  // Un % solt o una adreça retallada fan petar decodeURIComponent. Els slugs
  // i els codis són ASCII: si no es pot descodificar, es llegeix tal com és.
  try { cru = decodeURIComponent(cru); } catch { /* es queda sense descodificar */ }
  if (cru.startsWith('50min/')) { curt = true; cru = cru.slice('50min/'.length); }
  cru.split(',').forEach(grup => {
    let primera = true;
    grup.split('|').forEach(tros => {
      const [slug, codi] = tros.split(':');
      const llista = PER_TEMA[slug];
      if (!llista) return;
      let i = llista.findIndex(q => q.codi === codi);
      if (i >= 0 && usades(slug).has(i)) return;      // regla 6
      if (i < 0) i = primeraLliure(slug);              // codi desaparegut → la primera lliure
      if (i < 0) return;                               // tema buit o sense variants lliures
      estructura[examen.length] = !primera;            // la plaça que ocuparà
      examen.push({ slug, i });
      primera = false;
    });
  });
}

function escriuHash() {
  const s = examen.map((p, k) =>
    (k ? (esOpcio(k) ? '|' : ',') : '') + `${p.slug}:${preguntaDe(p).codi}`).join('');
  const h = (curt ? '50min/' : '') + s;
  history.replaceState(null, '', h ? '#' + h : location.pathname + location.search);
}

// ── accions ──────────────────────────────────────────────────────────
/** Un clic a un tema hi afegeix una pregunta: la primera variant lliure. */
function afegeix(slug) {
  const i = primeraLliure(slug);
  if (i < 0) return;
  examen.push({ slug, i });
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

/** Passa a la variant següent (o anterior) del mateix tema que no sigui ja
 *  a l'examen (regla 6). */
function rota(k, pas) {
  const p = examen[k], n = PER_TEMA[p.slug].length, altres = usades(p.slug, k);
  for (let s = 1; s < n; s++) {
    const i = ((p.i + pas * s) % n + n) % n;
    if (altres.has(i)) continue;
    const obert = visor[preguntaDe(p).id];
    delete visor[preguntaDe(p).id];
    p.i = i;
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
function pintaTemes() {
  const ul = $('#temes');
  ul.innerHTML = '';
  Object.entries(BANC.unitats).forEach(([u, info]) => {
    const temes = BANC.temes.filter(t => t.unitat === u);
    if (!temes.length) return;
    const cap = document.createElement('li');
    cap.className = 'grup' + (u === 'pau' ? ' grup-pau' : '');
    cap.innerHTML = `<span>${esc(info.nom)}</span> ${esc(info.subtitol)}`;
    ul.appendChild(cap);
    temes.forEach(t => pintaTema(ul, t));
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
  const div = document.createElement('div');
  div.className = 'carta' + (esPau ? ' pau' : '') + (esOpcio(k) ? ' opcio' : '');
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
    <div class="meta">
      <span>${apartatsDe(q).map(num).join(' + ')} = ${num(apartatsDe(q).reduce((s, a) => s + a, 0))} punts</span>
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
                          munta([ambCapcalera(q, `Q${etiqueta}`)], false)),
    prev:     () => rota(k, -1),
    next:     () => rota(k, +1),
    amunt:    () => mou(k, -1),
    avall:    () => mou(k, +1),
    treu:     () => treu(k),
    opcio:    () => commutaOpcio(k),
  };
  div.querySelectorAll('button[data-fer]').forEach(b => { b.onclick = fer[b.dataset.fer]; });
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
  const centDe = q => Math.round(apartatsDe(q).reduce((s, a) => s + a, 0) * 100);
  const cent = gs.reduce((s, g) => s + Math.max(...g.map(k => centDe(qs[k]))), 0);
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
  $('#baixa-sol').disabled = !qs.length;
  escriuHash();
}

// ── arrencada ────────────────────────────────────────────────────────
const cossosTriats = () => {
  const et = etiquetes();
  return triades().map((q, k) => ambCapcalera(q, `Q${et[k]}`));
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
$('#baixa-sol').onclick = () => baixa('examen-sencer-solucions.tex', munta(pecesExamen(), true));
$('#numprova').oninput = () => { $('#baixa-prova').textContent = `prova-${numProva()}.tex`; };
$('.botons-entorn').querySelectorAll('button[data-entorn]').forEach(b => {
  b.onclick = () => baixa(`${b.dataset.entorn}.tex`, BANC[b.dataset.entorn]);
});
$('#segell').textContent = `${BANC.preguntes.length} preguntes · ${BANC.generat}`;

llegeixHash();
pinta();
