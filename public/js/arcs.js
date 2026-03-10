/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Missile Arc Animations
   Canvas-rendered parabolic trajectories over Leaflet
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Arcs = {
  arcData: [],
  animationFrame: null,
  canvasLayer: null,

  // Define arc trajectories
  getArcDefinitions() {
    return [
      // Iranian outbound — Red arcs
      { from: [35.69, 51.39], to: [29.35, 47.52], color: '#b81c1c', label: 'Tehran → Kuwait' },
      { from: [35.69, 51.39], to: [25.12, 51.32], color: '#b81c1c', label: 'Tehran → Qatar' },
      { from: [35.69, 51.39], to: [32.79, 34.99], color: '#b81c1c', label: 'Tehran → Haifa' },
      { from: [35.69, 51.39], to: [32.09, 34.78], color: '#b81c1c', label: 'Tehran → Tel Aviv' },
      { from: [33.89, 35.50], to: [32.79, 34.99], color: '#7b3fa0', label: 'Beirut → Haifa' },

      // US/Israel inbound — Blue/white arcs
      { from: [33.50, 33.00], to: [35.69, 51.39], color: '#4a9eff', label: 'Med → Tehran' },
      { from: [25.15, 56.50], to: [27.18, 56.27], color: '#4a9eff', label: 'GoO → Bandar Abbas' },
      { from: [25.15, 56.50], to: [32.65, 51.67], color: '#4a9eff', label: 'GoO → Isfahan' },
      { from: [33.50, 33.00], to: [33.89, 35.50], color: '#d4d4d4', label: 'Med → Beirut' }
    ];
  },

  // Create SVG arc overlay for Leaflet
  init(map) {
    if (!map) return;

    this.arcData = this.getArcDefinitions();

    // Create SVG overlay
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'arc-overlay');
    svg.style.cssText = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 500;';

    const mapContainer = map.getContainer();
    const pane = map.getPane('overlayPane');
    if (pane) pane.appendChild(svg);

    this.svg = svg;
    this.map = map;

    // Redraw on map move/zoom
    map.on('moveend zoomend', () => this.draw());
    this.draw();
  },

  // Calculate quadratic bezier arc points
  draw() {
    if (!this.svg || !this.map) return;

    const paths = this.arcData.map((arc, i) => {
      const fromPoint = this.map.latLngToLayerPoint(L.latLng(arc.from[0], arc.from[1]));
      const toPoint = this.map.latLngToLayerPoint(L.latLng(arc.to[0], arc.to[1]));

      // Control point for parabolic curve
      const midX = (fromPoint.x + toPoint.x) / 2;
      const midY = (fromPoint.y + toPoint.y) / 2;
      const dist = Math.sqrt(Math.pow(toPoint.x - fromPoint.x, 2) + Math.pow(toPoint.y - fromPoint.y, 2));
      const controlY = midY - dist * 0.3;

      const pathD = `M ${fromPoint.x} ${fromPoint.y} Q ${midX} ${controlY} ${toPoint.x} ${toPoint.y}`;
      const dashLen = dist;

      return `<path d="${pathD}" fill="none" stroke="${arc.color}" stroke-width="1.2" stroke-opacity="0.4"
                stroke-dasharray="${dashLen}" stroke-dashoffset="${dashLen}"
                style="animation: arcDash ${3 + i * 0.5}s ease-in-out infinite alternate; animation-delay: ${i * 0.3}s;">
              </path>`;
    }).join('');

    this.svg.innerHTML = `
      <defs>
        <style>
          @keyframes arcDash {
            to { stroke-dashoffset: 0; }
          }
        </style>
      </defs>
      ${paths}
    `;

    // Position SVG to match Leaflet's layer transform
    const topLeft = this.map.containerPointToLayerPoint([0, 0]);
    L.DomUtil.setPosition(this.svg, topLeft);
    const size = this.map.getSize();
    this.svg.setAttribute('width', size.x);
    this.svg.setAttribute('height', size.y);
    this.svg.setAttribute('viewBox', `${topLeft.x} ${topLeft.y} ${size.x} ${size.y}`);
  },

  // Toggle arcs on/off
  toggle(show) {
    if (this.svg) {
      this.svg.style.display = show ? 'block' : 'none';
    }
  }
};
