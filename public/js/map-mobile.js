/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Collapsible map overlays on small screens
   On phones the legend and layer controls start collapsed to a
   single tappable header so they don't cover the map or popups.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  function makeCollapsible(el, label) {
    if (!el || el.querySelector('.map-toggle')) return;
    var heading = el.querySelector('h4');
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'map-toggle';
    btn.setAttribute('aria-expanded', 'false');
    btn.textContent = label + ' ▸';
    if (heading) heading.style.display = 'none';
    el.insertBefore(btn, el.firstChild);
    el.classList.add('map-collapsible', 'collapsed');
    btn.addEventListener('click', function () {
      var open = el.classList.toggle('collapsed') === false;
      btn.setAttribute('aria-expanded', String(open));
      btn.textContent = label + (open ? ' ▾' : ' ▸');
    });
  }

  function init() {
    if (!window.matchMedia('(max-width: 768px)').matches) return;
    makeCollapsible(document.getElementById('map-legend'), 'Legend');
    makeCollapsible(document.getElementById('layer-controls'), 'Layers');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
