/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Map Module (Leaflet)
   Every marker earns its light. Every popup tells a story.
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Map = {
  map: null,
  layers: {},

  init() {
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
      'hezbollah': L.layerGroup().addTo(this.map)
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

  // ─── STRIKE MARKERS ──────────────────────────────────────
  createPulseMarker(lat, lng, color, size = 8) {
    return L.circleMarker([lat, lng], {
      radius: size,
      fillColor: color,
      color: color,
      weight: 1,
      opacity: 0.8,
      fillOpacity: 0.6
    });
  },

  createPulseRing(lat, lng, color, radius) {
    return L.circleMarker([lat, lng], {
      radius: radius,
      fillColor: color,
      color: 'transparent',
      fillOpacity: 0.12,
      weight: 0
    });
  },

  // ─── US/ISRAEL STRIKES ON IRAN ────────────────────────────
  addStrikes(strikes) {
    if (!strikes) return;
    const layer = this.layers['us-strikes'];
    layer.clearLayers();

    strikes.forEach(s => {
      const isCivilian = s.subtype === 'civilian_casualty';
      const color = isCivilian ? '#ffffff' : '#d4782a';
      const size = isCivilian ? 10 : 7;

      const marker = this.createPulseMarker(s.lat, s.lng, color, size);
      const pulse = this.createPulseRing(s.lat, s.lng, color, size + 5);

      // Day count
      const dayCount = s.active_days.length;
      const firstDay = s.active_days[0];
      const dayLabel = dayCount === 1 ? 'Day ' + firstDay : 'Days ' + s.active_days[0] + '–' + s.active_days[s.active_days.length - 1];

      const popupContent = `
        <div style="min-width: 220px;">
          <h4 style="color: ${color}; margin-bottom: 8px; font-size: 14px;">${s.city}</h4>
          ${isCivilian ? '<div style="color: #ef4444; font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; font-weight: 600;">CIVILIAN CASUALTY SITE</div>' : ''}
          <div style="font-size: 11px; color: #8a8a8a; margin-bottom: 8px;">
            <strong style="color: #d4782a;">Targets:</strong><br>
            ${s.targets.map(t => '&nbsp;&nbsp;▸ ' + t).join('<br>')}
          </div>
          <div style="font-size: 11px; color: ${isCivilian ? '#ffffff' : '#8a8a8a'}; margin-bottom: 6px;">
            <strong>Casualties:</strong> ${s.casualties_reported}
          </div>
          <div style="font-size: 10px; color: #555; line-height: 1.5;">
            <strong>First strike:</strong> ${WarTheater.Utils.formatDateFull(s.first_strike)}<br>
            <strong>Active:</strong> ${dayLabel} (${dayCount} day${dayCount > 1 ? 's' : ''} of strikes)<br>
            <strong>Source:</strong> ${s.casualties_source}
          </div>
          ${s.notes ? '<div style="font-size: 10px; color: #d4782a; margin-top: 8px; padding-top: 6px; border-top: 1px solid #1a1a1a; font-style: italic;">' + s.notes + '</div>' : ''}
        </div>
      `;
      marker.bindPopup(popupContent, { maxWidth: 300 });

      // Tooltip on hover showing city name
      marker.bindTooltip(s.city + (isCivilian ? ' — CIVILIAN' : ''), {
        permanent: false,
        direction: 'top',
        offset: [0, -8],
        className: 'strike-tooltip'
      });

      layer.addLayer(pulse);
      layer.addLayer(marker);
    });
  },

  // ─── IRANIAN RETALIATION ──────────────────────────────────
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
      const pulse = this.createPulseRing(s.lat, s.lng, color, 12);

      const dayCount = s.active_days.length;
      const dayLabel = dayCount === 1 ? 'Day ' + s.active_days[0] : 'Days ' + s.active_days[0] + '–' + s.active_days[s.active_days.length - 1];

      const typeLabel = isHez ? 'HEZBOLLAH FRONT' : 'IRANIAN RETALIATION';

      const popupContent = `
        <div style="min-width: 220px;">
          <h4 style="color: ${color}; margin-bottom: 4px; font-size: 14px;">${s.city}</h4>
          <div style="color: ${color}; font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; font-weight: 600;">${typeLabel}</div>
          <div style="font-size: 11px; color: #8a8a8a; margin-bottom: 6px;">
            <strong>Weapon:</strong> ${s.weapon}<br>
            <strong>Origin:</strong> ${s.origin}
          </div>
          <div style="font-size: 11px; color: #e0e0e0; margin-bottom: 6px;">
            <strong>Result:</strong> ${s.casualties_reported}
          </div>
          <div style="font-size: 10px; color: #555; line-height: 1.5;">
            <strong>Date:</strong> ${WarTheater.Utils.formatDateFull(s.first_strike)}<br>
            <strong>Active:</strong> ${dayLabel}<br>
            <strong>Source:</strong> ${s.casualties_source}
          </div>
          ${s.notes ? '<div style="font-size: 10px; color: ' + color + '; margin-top: 8px; padding-top: 6px; border-top: 1px solid #1a1a1a; font-style: italic;">' + s.notes + '</div>' : ''}
        </div>
      `;
      marker.bindPopup(popupContent, { maxWidth: 300 });
      marker.bindTooltip(s.city, { permanent: false, direction: 'top', offset: [0, -8] });

      targetLayer.addLayer(pulse);
      targetLayer.addLayer(marker);
    });
  },

  // ─── US NAVAL ASSETS ───────────────────────────────────
  addCarriers(carriers) {
    if (!carriers) return;
    const layer = this.layers['carriers'];
    layer.clearLayers();

    // Icon styles by asset type
    const iconStyles = {
      carrier: { size: 16, color: '#4a9eff', shape: 'rotate(45deg)', glow: 'rgba(74,158,255,0.4)', radius: 150000 },
      amphibious: { size: 13, color: '#3b82f6', shape: 'rotate(45deg)', glow: 'rgba(59,130,246,0.3)', radius: 100000 },
      destroyer: { size: 8, color: '#60a5fa', shape: 'none', glow: 'rgba(96,165,250,0.3)', radius: 0 },
      submarine: { size: 9, color: '#818cf8', shape: 'none', glow: 'rgba(129,140,248,0.3)', radius: 0 }
    };

    const typeLabels = {
      carrier: 'AIRCRAFT CARRIER',
      amphibious: 'AMPHIBIOUS ASSAULT SHIP',
      destroyer: 'GUIDED MISSILE DESTROYER',
      submarine: 'GUIDED MISSILE SUBMARINE'
    };

    carriers.forEach(c => {
      const style = iconStyles[c.type] || iconStyles.destroyer;
      const typeLabel = typeLabels[c.type] || 'US NAVAL ASSET';

      // Icon — diamond for capital ships, circle for escorts/subs
      const isCapitalShip = c.type === 'carrier' || c.type === 'amphibious';
      const iconHtml = isCapitalShip
        ? '<div style="width: ' + style.size + 'px; height: ' + style.size + 'px; background: ' + style.color + '; transform: ' + style.shape + '; border: 1px solid ' + style.color + '; box-shadow: 0 0 10px ' + style.glow + ';"></div>'
        : '<div style="width: ' + style.size + 'px; height: ' + style.size + 'px; background: ' + style.color + '; border-radius: 50%; border: 1px solid ' + style.color + '; box-shadow: 0 0 8px ' + style.glow + ';"></div>';

      const icon = L.divIcon({
        className: c.type === 'carrier' ? 'carrier-icon' : 'naval-icon',
        html: iconHtml,
        iconSize: [style.size, style.size],
        iconAnchor: [style.size / 2, style.size / 2]
      });

      const marker = L.marker([c.lat, c.lng], { icon });

      // Operational radius (only for capital ships)
      if (style.radius > 0) {
        const area = L.circle([c.lat, c.lng], {
          radius: style.radius,
          color: style.color,
          fillColor: style.color,
          fillOpacity: 0.03,
          weight: 0.5,
          opacity: 0.2,
          dashArray: '4 4'
        });
        layer.addLayer(area);
      }

      // Escorts section
      const escortsHtml = c.escorts && c.escorts.length > 0
        ? '<div style="font-size: 10px; color: #555; margin-top: 8px; padding-top: 6px; border-top: 1px solid #1a1a1a;"><strong>Escorts:</strong><br>' + c.escorts.map(e => '&nbsp;&nbsp;▸ ' + e).join('<br>') + '</div>'
        : '';

      const classifiedNote = c.type === 'submarine'
        ? '<div style="font-size: 9px; color: #818cf8; margin-top: 6px; font-style: italic;">Position approximate — exact location classified</div>'
        : '';

      const popupContent = `
        <div style="min-width: 240px;">
          <h4 style="color: ${style.color}; margin-bottom: 4px; font-size: 14px;">${c.name}</h4>
          <div style="color: ${style.color}; font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; font-weight: 600;">${typeLabel}</div>
          <div style="font-size: 11px; color: #8a8a8a; line-height: 1.7;">
            <strong>Hull:</strong> ${c.hull}<br>
            <strong>Formation:</strong> ${c.strike_group}<br>
            <strong>Area:</strong> ${c.area}<br>
            <strong>Status:</strong> <span style="color: #22c55e;">${c.status}</span><br>
            ${c.aircraft !== 'N/A' ? '<strong>Air Wing:</strong> ' + c.aircraft + '<br>' : ''}
            <strong>Deployed:</strong> ${WarTheater.Utils.formatDateFull(c.deployed_since)}
          </div>
          ${escortsHtml}
          ${c.notes ? '<div style="font-size: 10px; color: ' + style.color + '; margin-top: 8px; font-style: italic;">' + c.notes + '</div>' : ''}
          ${classifiedNote}
        </div>
      `;
      marker.bindPopup(popupContent, { maxWidth: 320 });
      marker.bindTooltip(c.name + ' (' + c.hull + ')', { permanent: false, direction: 'top', offset: [0, -10] });

      layer.addLayer(marker);
    });
  },

  // ─── STRAIT OF HORMUZ ────────────────────────────────────
  addHormuz(hormuzData) {
    if (!hormuzData) return;
    const layer = this.layers['hormuz'];
    layer.clearLayers();

    const geo = hormuzData.geometry;
    const impact = hormuzData.impact;
    const strait = hormuzData.strait;

    // Chokepoint polygon with breathing glow
    const polygon = L.polygon(geo.chokepoint, {
      color: '#d4a020',
      fillColor: '#d4a020',
      fillOpacity: 0.15,
      weight: 2,
      opacity: 0.7,
      dashArray: '6 4'
    });

    // Build alternative routes HTML
    const altRoutesHtml = impact.alternative_routes.map(r =>
      '<div style="padding: 2px 0;">' +
      '<span style="color: #d4a020;">' + r.name + '</span>: ' +
      r.capacity_mbd + ' mbd — <span style="color: #555;">' + r.status + '</span>' +
      '</div>'
    ).join('');

    polygon.bindPopup(`
      <div style="min-width: 280px;">
        <h4 style="color: #d4a020; margin-bottom: 4px; font-size: 14px;">STRAIT OF HORMUZ</h4>
        <div style="color: #ef4444; font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; font-weight: 600;">EFFECTIVELY CLOSED TO COMMERCIAL TRAFFIC</div>
        <div style="font-size: 11px; color: #e0e0e0; margin-bottom: 8px; line-height: 1.7;">
          <strong>${strait.percent_global_oil}%</strong> of global oil passes through this waterway.<br>
          <strong>${strait.percent_global_lng}%</strong> of global LNG transits here.<br>
          <strong>Width:</strong> ${strait.width_km}km (shipping lane: ${strait.shipping_lane_width_km}km)
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 8px;">
          <div style="background: rgba(26,26,26,0.8); padding: 8px; text-align: center;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 18px; color: #d4a020;">${impact.tankers_transiting_prewar_daily}</div>
            <div style="font-size: 9px; color: #555; text-transform: uppercase; letter-spacing: 0.05em;">ships/day pre-war</div>
          </div>
          <div style="background: rgba(26,26,26,0.8); padding: 8px; text-align: center;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 18px; color: #ef4444;">${impact.tankers_transiting_current_daily}</div>
            <div style="font-size: 9px; color: #555; text-transform: uppercase; letter-spacing: 0.05em;">ships/day now</div>
          </div>
        </div>
        <div style="font-size: 11px; color: #8a8a8a; line-height: 1.6; margin-bottom: 8px;">
          <strong>Closed since:</strong> ${WarTheater.Utils.formatDateFull(strait.closure_date)}<br>
          <strong>Method:</strong> ${strait.closure_method}<br>
          <strong>Insurance increase:</strong> <span style="color: #ef4444;">+${impact.insurance_cost_increase_pct}%</span><br>
          <strong>Supply shortfall:</strong> <span style="color: #ef4444;">${impact.shortfall_mbd} million bbl/day</span>
        </div>
        <div style="font-size: 10px; color: #555; padding-top: 6px; border-top: 1px solid #1a1a1a;">
          <strong>Alternative pipeline routes:</strong>
          ${altRoutesHtml}
          <div style="color: #d4a020; margin-top: 4px;">Total alternative: ${impact.total_alternative_capacity_mbd} mbd — Shortfall: ${impact.shortfall_mbd} mbd</div>
        </div>
      </div>
    `, { maxWidth: 360 });

    // Shipping lanes
    geo.shipping_lanes.forEach(lane => {
      const polyline = L.polyline(lane.path, {
        color: lane.direction === 'inbound' ? '#d4a020' : '#b8860b',
        weight: 2,
        opacity: 0.3,
        dashArray: '8 4'
      });
      polyline.bindTooltip(lane.direction === 'inbound' ? 'Inbound shipping lane' : 'Outbound shipping lane', { sticky: true });
      layer.addLayer(polyline);
    });

    // Islands with military context
    geo.islands.forEach(isl => {
      const m = L.circleMarker([isl.lat, isl.lng], {
        radius: 4,
        fillColor: '#d4a020',
        color: '#d4a020',
        fillOpacity: 0.6,
        weight: 1,
        opacity: 0.8
      });
      const militaryNote = isl.military ? ' [Military installations]' : '';
      const controlNote = isl.control || '';
      m.bindTooltip(
        '<strong>' + isl.name + '</strong><br>' +
        '<span style="font-size: 10px; color: #8a8a8a;">Control: ' + controlNote + militaryNote + '</span>',
        { permanent: false, direction: 'top' }
      );
      layer.addLayer(m);
    });

    layer.addLayer(polygon);

    // ─── PERMANENT HORMUZ LABEL (Stark × Trump agreement) ───
    const hormuzLabel = L.divIcon({
      className: 'hormuz-permanent-label',
      html: '<div style="' +
        'font-family: Barlow Condensed, sans-serif;' +
        'font-size: 11px;' +
        'font-weight: 600;' +
        'text-transform: uppercase;' +
        'letter-spacing: 0.08em;' +
        'color: #d4a020;' +
        'text-shadow: 0 0 8px rgba(212,160,32,0.4), 0 1px 3px rgba(0,0,0,0.8);' +
        'white-space: nowrap;' +
        'text-align: center;' +
        'line-height: 1.6;' +
        '">' +
        '20% of global oil passes through this waterway.<br>' +
        '<span style="color: #ef4444;">It is currently closed.</span>' +
        '</div>',
      iconSize: [280, 40],
      iconAnchor: [140, 50]
    });
    const labelMarker = L.marker([26.35, 56.55], { icon: hormuzLabel, interactive: false });
    layer.addLayer(labelMarker);
  },

  // ─── TIMELINE SCRUBBER ────────────────────────────────────
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

      days.push({
        date: dateStr,
        day: dayNum,
        label: WarTheater.Utils.formatDate(dateStr),
        events: dayEvents,
        isToday: dateStr === '2026-03-10'
      });
      current.setDate(current.getDate() + 1);
    }

    container.innerHTML = days.map(d => {
      const majorEvent = d.events.find(e => e.category === 'military') || d.events[0];
      const eventCount = d.events.length;
      const eventSummary = d.events.map(e => e.title).join(' | ');

      return `
        <div class="timeline-day ${d.isToday ? 'active' : 'past'}" data-date="${d.date}"
             title="Day ${d.day} — ${d.label}&#10;${eventSummary || 'No major events recorded'}">
          <div style="font-family: 'Barlow Condensed', sans-serif; font-size: 9px; color: ${d.isToday ? 'var(--text-accent)' : 'var(--text-dim)'}; text-transform: uppercase; letter-spacing: 0.05em;">Day ${d.day}</div>
          <div class="dot" style="${eventCount > 2 ? 'width: 12px; height: 12px;' : ''}"></div>
          <div class="date-label">${d.label}</div>
          ${majorEvent ? '<div class="event-label">' + (majorEvent.title.length > 25 ? majorEvent.title.substring(0, 25) + '...' : majorEvent.title) + '</div>' : ''}
          ${eventCount > 1 ? '<div style="font-size: 8px; color: var(--text-dim);">+' + (eventCount - 1) + ' more</div>' : ''}
        </div>
      `;
    }).join('');

    // Click handler for scrubber days
    container.querySelectorAll('.timeline-day').forEach(day => {
      day.style.cursor = 'pointer';
      day.addEventListener('click', () => {
        const date = day.dataset.date;
        // Navigate to The Record panel, filtered to this date
        const navBtn = document.querySelector('[data-panel="record"]');
        if (navBtn) navBtn.click();
        // Scroll to relevant events
        setTimeout(() => {
          const eventEl = document.querySelector('.timeline-event[data-date="' + date + '"]');
          if (eventEl) eventEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 300);
      });
    });
  },

  // ─── POPULATE ALL ─────────────────────────────────────────
  async populate(data) {
    this.addStrikes(data.strikes);
    this.addRetaliation(data.retaliation);
    this.addCarriers(data.carriers);
    this.addHormuz(data.hormuz);
    this.buildTimelineScrubber(data.timeline);
  }
};
