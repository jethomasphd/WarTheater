/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Map Module (Leaflet)
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Map = {
  map: null,
  layers: {},

  init() {
    // Initialize Leaflet map
    this.map = L.map('theater-map', {
      center: [29.5, 52.0],
      zoom: 5,
      minZoom: 4,
      maxZoom: 10,
      zoomControl: true,
      attributionControl: false
    });

    // Dark base tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(this.map);

    // Track cursor coordinates
    this.map.on('mousemove', (e) => {
      const coords = document.getElementById('map-coords');
      if (coords) {
        coords.textContent = e.latlng.lat.toFixed(4) + '°N, ' + e.latlng.lng.toFixed(4) + '°E';
      }
    });

    // Initialize layer groups
    this.layers = {
      'us-strikes': L.layerGroup().addTo(this.map),
      'iran-retaliation': L.layerGroup().addTo(this.map),
      'carriers': L.layerGroup().addTo(this.map),
      'hormuz': L.layerGroup().addTo(this.map),
      'hezbollah': L.layerGroup().addTo(this.map),
      'missile-ranges': L.layerGroup(),
      'arcs': L.layerGroup()
    };

    // Bind layer toggles
    document.querySelectorAll('[data-layer]').forEach(checkbox => {
      checkbox.addEventListener('change', (e) => {
        const layerName = e.target.dataset.layer;
        const layer = this.layers[layerName];
        if (!layer) return;
        if (e.target.checked) {
          this.map.addLayer(layer);
        } else {
          this.map.removeLayer(layer);
        }
      });
    });
  },

  // Create pulsing strike marker
  createPulseMarker(lat, lng, color, size = 8) {
    return L.circleMarker([lat, lng], {
      radius: size,
      fillColor: color,
      color: color,
      weight: 1,
      opacity: 0.8,
      fillOpacity: 0.6,
      className: 'pulse-marker'
    });
  },

  // Add US/Israel strikes on Iran
  addStrikes(strikes) {
    if (!strikes) return;
    const layer = this.layers['us-strikes'];
    layer.clearLayers();

    strikes.forEach(s => {
      const isCivilian = s.subtype === 'civilian_casualty';
      const color = isCivilian ? '#ffffff' : '#d4782a';
      const size = isCivilian ? 10 : 7;

      const marker = this.createPulseMarker(s.lat, s.lng, color, size);

      // Outer pulse ring
      const pulse = L.circleMarker([s.lat, s.lng], {
        radius: size + 4,
        fillColor: color,
        color: 'transparent',
        fillOpacity: 0.15,
        weight: 0
      });

      const popupContent = `
        <h4 style="color: ${color};">${s.city}</h4>
        <div class="popup-targets">
          <strong>Targets:</strong> ${s.targets.join(', ')}
        </div>
        <div class="popup-casualties" style="color: ${isCivilian ? '#ffffff' : '#8a8a8a'};">
          <strong>Casualties:</strong> ${s.casualties_reported}
        </div>
        <div style="font-size: 10px; color: #555; margin-top: 6px;">
          First strike: ${s.first_strike} | Active: ${s.active_days.length} days
          ${s.notes ? '<br>' + s.notes : ''}
        </div>
      `;
      marker.bindPopup(popupContent);

      layer.addLayer(pulse);
      layer.addLayer(marker);
    });
  },

  // Add Iranian retaliation strikes
  addRetaliation(retaliation) {
    if (!retaliation) return;
    const layer = this.layers['iran-retaliation'];
    const hezLayer = this.layers['hezbollah'];
    layer.clearLayers();
    hezLayer.clearLayers();

    retaliation.forEach(s => {
      const isHez = s.type === 'hezbollah_front';
      const color = isHez ? '#7b3fa0' : '#b81c1c';
      const targetLayer = isHez ? hezLayer : layer;

      const marker = this.createPulseMarker(s.lat, s.lng, color, 7);

      const pulse = L.circleMarker([s.lat, s.lng], {
        radius: 12,
        fillColor: color,
        color: 'transparent',
        fillOpacity: 0.1,
        weight: 0
      });

      const popupContent = `
        <h4 style="color: ${color};">${s.city}</h4>
        <div style="font-size: 11px; color: #8a8a8a;">
          <strong>Weapon:</strong> ${s.weapon}<br>
          <strong>Origin:</strong> ${s.origin}
        </div>
        <div class="popup-casualties">
          <strong>Result:</strong> ${s.casualties_reported}
        </div>
        <div style="font-size: 10px; color: #555; margin-top: 6px;">
          ${s.notes || ''}
        </div>
      `;
      marker.bindPopup(popupContent);

      targetLayer.addLayer(pulse);
      targetLayer.addLayer(marker);
    });
  },

  // Add carrier strike groups
  addCarriers(carriers) {
    if (!carriers) return;
    const layer = this.layers['carriers'];
    layer.clearLayers();

    carriers.forEach(c => {
      // Carrier icon - blue diamond
      const icon = L.divIcon({
        className: 'carrier-icon',
        html: `<div style="
          width: 14px; height: 14px;
          background: #4a9eff;
          transform: rotate(45deg);
          border: 1px solid #6db4ff;
          box-shadow: 0 0 10px rgba(74,158,255,0.4);
        "></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7]
      });

      const marker = L.marker([c.lat, c.lng], { icon });

      // Carrier patrol area
      const area = L.circle([c.lat, c.lng], {
        radius: 150000, // 150km operational radius
        color: '#4a9eff',
        fillColor: '#4a9eff',
        fillOpacity: 0.03,
        weight: 0.5,
        opacity: 0.3,
        dashArray: '4 4'
      });

      const popupContent = `
        <h4 style="color: #4a9eff;">${c.name}</h4>
        <div style="font-size: 11px; color: #8a8a8a;">
          <strong>${c.hull}</strong> — ${c.strike_group}<br>
          <strong>Area:</strong> ${c.area}<br>
          <strong>Status:</strong> ${c.status}<br>
          <strong>Aircraft:</strong> ${c.aircraft}
        </div>
        <div style="font-size: 10px; color: #555; margin-top: 6px;">
          Escorts: ${c.escorts.join(', ')}
        </div>
      `;
      marker.bindPopup(popupContent);

      layer.addLayer(area);
      layer.addLayer(marker);
    });
  },

  // Add Strait of Hormuz
  addHormuz(hormuzData) {
    if (!hormuzData) return;
    const layer = this.layers['hormuz'];
    layer.clearLayers();

    const geo = hormuzData.geometry;

    // Chokepoint polygon
    const polygon = L.polygon(geo.chokepoint, {
      color: '#d4a020',
      fillColor: '#d4a020',
      fillOpacity: 0.12,
      weight: 1.5,
      opacity: 0.6,
      dashArray: '4 4'
    });

    const impact = hormuzData.impact;
    const strait = hormuzData.strait;
    polygon.bindPopup(`
      <h4 style="color: #d4a020;">STRAIT OF HORMUZ — CLOSED</h4>
      <div style="font-size: 11px; color: #8a8a8a;">
        <strong>${strait.percent_global_oil}%</strong> of global oil transits this waterway<br>
        <strong>Pre-war:</strong> ${impact.tankers_transiting_prewar_daily} tankers/day<br>
        <strong>Current:</strong> ${impact.tankers_transiting_current_daily} tankers/day<br>
        <strong>Closed since:</strong> ${strait.closure_date}<br>
        <strong>Insurance increase:</strong> +${impact.insurance_cost_increase_pct}%<br>
        <strong>Supply shortfall:</strong> ${impact.shortfall_mbd} million bbl/day
      </div>
    `);

    // Shipping lanes
    geo.shipping_lanes.forEach(lane => {
      const polyline = L.polyline(lane.path, {
        color: lane.direction === 'inbound' ? '#d4a020' : '#b8860b',
        weight: 2,
        opacity: 0.3,
        dashArray: '8 4'
      });
      layer.addLayer(polyline);
    });

    // Islands
    geo.islands.forEach(isl => {
      const m = L.circleMarker([isl.lat, isl.lng], {
        radius: 4,
        fillColor: '#d4a020',
        color: '#d4a020',
        fillOpacity: 0.6,
        weight: 1,
        opacity: 0.8
      });
      m.bindTooltip(isl.name, {
        permanent: false,
        className: 'hormuz-tooltip',
        direction: 'top'
      });
      layer.addLayer(m);
    });

    layer.addLayer(polygon);
  },

  // Add missile range rings
  addMissileRanges(data) {
    if (!data) return;
    const layer = this.layers['missile-ranges'];
    layer.clearLayers();

    const origin = data.origin;

    data.systems.forEach(sys => {
      const circle = L.circle([origin.lat, origin.lng], {
        radius: sys.range_km * 1000,
        color: sys.color,
        fillColor: sys.color,
        fillOpacity: 0.02,
        weight: 1,
        opacity: 0.25,
        dashArray: '6 4'
      });

      circle.bindTooltip(`${sys.name} — ${sys.range_km}km`, {
        permanent: false,
        direction: 'top'
      });

      layer.addLayer(circle);
    });

    // Origin marker
    const originMarker = L.circleMarker([origin.lat, origin.lng], {
      radius: 3,
      fillColor: '#ff3333',
      color: '#ff3333',
      fillOpacity: 1,
      weight: 0
    });
    originMarker.bindTooltip('Tehran — Missile Origin', { direction: 'top' });
    layer.addLayer(originMarker);
  },

  // Build timeline scrubber
  buildTimelineScrubber(events) {
    const container = document.getElementById('timeline-days');
    if (!container || !events) return;

    const warStart = new Date('2026-02-28');
    const today = new Date('2026-03-10');
    const days = [];
    const current = new Date(warStart);

    while (current <= today) {
      const dateStr = current.toISOString().split('T')[0];
      const dayNum = WarTheater.Utils.getWarDay(dateStr);
      const dayEvents = events.filter(e => e.date === dateStr);
      const majorEvent = dayEvents.find(e => e.category === 'military') || dayEvents[0];

      days.push({
        date: dateStr,
        day: dayNum,
        label: WarTheater.Utils.formatDate(dateStr),
        event: majorEvent ? majorEvent.title : null,
        isToday: dateStr === '2026-03-10'
      });
      current.setDate(current.getDate() + 1);
    }

    container.innerHTML = days.map(d => `
      <div class="timeline-day ${d.isToday ? 'active' : 'past'}" data-date="${d.date}">
        <div class="dot"></div>
        <div class="date-label">${d.label}</div>
        ${d.event ? `<div class="event-label">${d.event.substring(0, 30)}${d.event.length > 30 ? '…' : ''}</div>` : ''}
      </div>
    `).join('');
  },

  // Populate all map data
  async populate(data) {
    this.addStrikes(data.strikes);
    this.addRetaliation(data.retaliation);
    this.addCarriers(data.carriers);
    this.addHormuz(data.hormuz);
    this.addMissileRanges(data.missiles);
    this.buildTimelineScrubber(data.timeline);
  }
};
