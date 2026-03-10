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
      minZoom: 2,
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
      'global-bases': L.layerGroup().addTo(this.map)
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
    var layer = this.layers['carriers'];
    layer.clearLayers();

    var typeLabels = {
      carrier: 'AIRCRAFT CARRIER',
      amphibious: 'AMPHIBIOUS ASSAULT SHIP',
      destroyer: 'GUIDED MISSILE DESTROYER',
      submarine: 'GUIDED MISSILE SUBMARINE'
    };
    var typeColors = {
      carrier: '#4a9eff',
      amphibious: '#3b82f6',
      destroyer: '#60a5fa',
      submarine: '#818cf8'
    };

    carriers.forEach(function(c) {
      var color = typeColors[c.type] || '#60a5fa';
      var typeLabel = typeLabels[c.type] || 'US NAVAL ASSET';
      var isCapital = (c.type === 'carrier' || c.type === 'amphibious');
      var dotPx = isCapital ? 20 : 12;
      var shortName = c.name.replace('USS ', '');

      // Build icon HTML with permanent label below
      var shapeStyle = isCapital
        ? 'width:' + dotPx + 'px;height:' + dotPx + 'px;background:' + color + ';transform:rotate(45deg);border:2px solid #fff;box-shadow:0 0 16px ' + color + ',0 0 32px ' + color + ';'
        : 'width:' + dotPx + 'px;height:' + dotPx + 'px;background:' + color + ';border-radius:50%;border:2px solid #fff;box-shadow:0 0 12px ' + color + ',0 0 24px ' + color + ';';

      var labelHtml = '<div style="position:absolute;top:' + (dotPx + 4) + 'px;left:50%;transform:translateX(-50%);white-space:nowrap;' +
        'font-family:Barlow Condensed,sans-serif;font-size:' + (isCapital ? '11' : '10') + 'px;font-weight:600;color:' + color + ';' +
        'text-transform:uppercase;letter-spacing:0.06em;text-shadow:0 0 6px #000,0 0 12px #000;text-align:center;line-height:1.2;">' +
        shortName + (isCapital ? '<br><span style="font-size:9px;color:#8a8a8a;font-weight:400;">' + c.hull + '</span>' : '') + '</div>';

      var html = '<div style="position:relative;width:' + dotPx + 'px;height:' + dotPx + 'px;">' +
        '<div style="position:absolute;top:0;left:0;' + shapeStyle + '"></div>' +
        '</div>' + labelHtml;

      var icon = L.divIcon({
        className: isCapital ? 'carrier-icon' : 'naval-icon',
        html: html,
        iconSize: [dotPx, dotPx + 28],
        iconAnchor: [dotPx / 2, dotPx / 2]
      });

      var marker = L.marker([c.lat, c.lng], { icon: icon, zIndexOffset: isCapital ? 1000 : 500 });

      // Operational radius ring for capital ships
      if (isCapital) {
        var radius = c.type === 'carrier' ? 150000 : 100000;
        var area = L.circle([c.lat, c.lng], {
          radius: radius,
          color: color,
          fillColor: color,
          fillOpacity: 0.04,
          weight: 1,
          opacity: 0.25,
          dashArray: '6 4'
        });
        layer.addLayer(area);
      }

      // Rich popup
      var escortsHtml = (c.escorts && c.escorts.length > 0)
        ? '<div style="font-size:10px;color:#555;margin-top:8px;padding-top:6px;border-top:1px solid #1a1a1a;"><strong>Escorts:</strong><br>' + c.escorts.map(function(e) { return '&nbsp;&nbsp;▸ ' + e; }).join('<br>') + '</div>'
        : '';
      var classifiedNote = (c.type === 'submarine')
        ? '<div style="font-size:9px;color:#818cf8;margin-top:6px;font-style:italic;">Position approximate — exact location classified</div>'
        : '';

      var popupContent =
        '<div style="min-width:240px;">' +
        '<h4 style="color:' + color + ';margin-bottom:4px;font-size:14px;">' + c.name + '</h4>' +
        '<div style="color:' + color + ';font-size:10px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;font-weight:600;">' + typeLabel + '</div>' +
        '<div style="font-size:11px;color:#8a8a8a;line-height:1.7;">' +
        '<strong>Hull:</strong> ' + c.hull + '<br>' +
        '<strong>Formation:</strong> ' + c.strike_group + '<br>' +
        '<strong>Area:</strong> ' + c.area + '<br>' +
        '<strong>Status:</strong> <span style="color:#22c55e;">' + c.status + '</span><br>' +
        (c.aircraft !== 'N/A' ? '<strong>Air Wing:</strong> ' + c.aircraft + '<br>' : '') +
        '<strong>Deployed:</strong> ' + WarTheater.Utils.formatDateFull(c.deployed_since) +
        '</div>' +
        escortsHtml +
        (c.notes ? '<div style="font-size:10px;color:' + color + ';margin-top:8px;font-style:italic;">' + c.notes + '</div>' : '') +
        classifiedNote +
        '</div>';

      marker.bindPopup(popupContent, { maxWidth: 320 });
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

  // ─── NEWS TICKER (replaces timeline scrubber) ────────────
  buildNewsTicker(events) {
    var ticker = document.getElementById('news-ticker');
    if (!ticker || !events) return;

    var catColors = {
      military: '#d4782a', financial: '#ef4444', humanitarian: '#f59e0b',
      diplomatic: '#4a9eff', domestic: '#7b3fa0'
    };

    // Get the single most recent event
    var latest = events.slice().sort(function(a, b) {
      return (b.date + 'T' + (b.time || '00:00')).localeCompare(a.date + 'T' + (a.time || '00:00'));
    })[0];

    if (!latest) return;

    var day = WarTheater.Utils.getWarDay(latest.date);
    var color = catColors[latest.category] || '#8a8a8a';
    var dp = latest.data_point ? ' — ' + latest.data_point : '';

    // Replace entire ticker with static latest + CTA
    ticker.innerHTML =
      '<div class="ticker-label">LATEST</div>' +
      '<div class="ticker-track" style="display:flex;align-items:center;padding:0 12px;overflow:hidden;">' +
        '<span style="font-family:JetBrains Mono,monospace;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' +
          '<span style="color:' + color + ';font-weight:600;">DAY ' + day + '</span> ' +
          '<span style="color:#555;">|</span> ' +
          '<span style="color:#e0e0e0;">' + latest.title + '</span>' +
          '<span style="color:#8a8a8a;">' + dp + '</span>' +
        '</span>' +
      '</div>' +
      '<div class="ticker-cta" id="ticker-cta">THE RECORD &#x25B8;</div>';

    document.getElementById('ticker-cta').addEventListener('click', function() {
      var btn = document.querySelector('[data-panel="record"]');
      if (btn) btn.click();
    });
  },

  // ─── GLOBAL BASES & LANDMARKS ──────────────────────────
  addGlobalBases() {
    var layer = this.layers['global-bases'];
    layer.clearLayers();

    var bases = [
      { name: 'Norfolk Naval Station', lat: 36.95, lng: -76.30, type: 'naval', note: 'Largest naval base in the world. Home port for carrier strike groups.' },
      { name: 'Pearl Harbor', lat: 21.35, lng: -157.95, type: 'naval', note: 'US Pacific Fleet HQ. Key logistics hub for Indo-Pacific.' },
      { name: 'Ramstein AB', lat: 49.44, lng: 7.60, type: 'air', note: 'USAFE HQ. Critical airlift node for Middle East operations.' },
      { name: 'Diego Garcia', lat: -7.32, lng: 72.41, type: 'air', note: 'B-2/B-52 staging. Tomahawk launch platform, Indian Ocean.' },
      { name: 'Al Udeid AB', lat: 25.12, lng: 51.31, type: 'air', note: 'CENTCOM forward HQ. Combined Air Ops Center for all sorties.' },
      { name: 'Yokosuka', lat: 35.29, lng: 139.67, type: 'naval', note: '7th Fleet HQ. Forward-deployed carrier home port.' },
      { name: 'Incirlik AB', lat: 37.00, lng: 35.43, type: 'air', note: 'NATO base, Turkey. Northern approach operations.' },
      { name: 'Camp Lemonnier', lat: 11.55, lng: 43.15, type: 'base', note: 'Djibouti. Only permanent US base in Africa.' },
      { name: 'Bahrain (5th Fleet)', lat: 26.23, lng: 50.48, type: 'naval', note: '5th Fleet HQ. Direct control of Gulf naval assets.' },
      { name: 'RAF Fairford', lat: 51.68, lng: -1.79, type: 'air', note: 'UK. B-52 forward deployment for CENTCOM operations.' },
      { name: 'Pentagon', lat: 38.87, lng: -77.06, type: 'landmark', note: 'DoD HQ. Where Operation Epic Fury is commanded.' },
      { name: 'New York', lat: 40.71, lng: -74.01, type: 'landmark', note: 'NYSE/NYMEX. Processing war-driven market volatility.' },
      { name: 'Houston', lat: 29.76, lng: -95.37, type: 'landmark', note: 'US energy capital. Refinery hub feeling Hormuz closure.' }
    ];

    var colors = { naval: '#4a9eff', air: '#d4782a', base: '#22c55e', landmark: '#8a8a8a' };
    var labels = { naval: 'US NAVAL INSTALLATION', air: 'US AIR FORCE BASE', base: 'US MILITARY BASE', landmark: 'KEY LOCATION' };

    bases.forEach(function(b) {
      var c = colors[b.type] || '#8a8a8a';
      var m = L.circleMarker([b.lat, b.lng], {
        radius: 5, fillColor: c, color: c, weight: 1, opacity: 0.7, fillOpacity: 0.5
      });
      m.bindTooltip(b.name, { permanent: false, direction: 'top', offset: [0, -6] });
      m.bindPopup(
        '<div style="min-width:200px;">' +
        '<h4 style="color:' + c + ';margin-bottom:4px;font-size:13px;">' + b.name + '</h4>' +
        '<div style="color:' + c + ';font-size:9px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;font-weight:600;">' + (labels[b.type] || '') + '</div>' +
        '<div style="font-size:11px;color:#8a8a8a;line-height:1.6;">' + b.note + '</div>' +
        '</div>', { maxWidth: 260 }
      );
      layer.addLayer(m);
    });
  },

  // ─── POPULATE ALL ─────────────────────────────────────────
  async populate(data) {
    this.addStrikes(data.strikes);
    this.addRetaliation(data.retaliation);
    this.addCarriers(data.carriers);
    this.addHormuz(data.hormuz);
    this.addGlobalBases();
    this.buildNewsTicker(data.timeline);
  }
};
