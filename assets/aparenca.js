/* ═══════════════════════════════════════════════════════════════════════
   Banc de preguntes — aparença: clar, fosc o el del sistema.
   Es carrega al <head>, abans de pintar res: així la pàgina no fa un
   parpelleig del tema equivocat en obrir-se.

   «Sistema» (per defecte) no posa cap atribut: el full d'estil segueix
   prefers-color-scheme, i canvia sol si el sistema operatiu canvia.
   «Clar» i «Fosc» posen data-theme a <html> i manen sobre el sistema.

   És una preferència de qui fa els exàmens, no part de l'examen: no va a
   l'adreça, sinó a la memòria del navegador, si la hi deixa. Si no, sempre
   «Sistema».
   ═══════════════════════════════════════════════════════════════════════ */
(() => {
  const CLAU = 'banc-aparenca';
  const MODES = ['clar', 'fosc', 'sistema'];
  const ATRIBUT = { clar: 'light', fosc: 'dark' };

  let mode = 'sistema';
  try { const m = localStorage.getItem(CLAU); if (MODES.includes(m)) mode = m; }
  catch { /* sense memòria del navegador: sistema */ }

  const aplica = () => {
    const arrel = document.documentElement;
    if (ATRIBUT[mode]) arrel.setAttribute('data-theme', ATRIBUT[mode]);
    else arrel.removeAttribute('data-theme');
    document.querySelectorAll('[data-aparenca]').forEach(b =>
      b.setAttribute('aria-pressed', String(b.dataset.aparenca === mode)));
  };
  aplica();

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-aparenca]').forEach(b => b.addEventListener('click', () => {
      mode = b.dataset.aparenca;
      try { localStorage.setItem(CLAU, mode); } catch { /* res */ }
      aplica();
    }));
    aplica();
  });
})();
