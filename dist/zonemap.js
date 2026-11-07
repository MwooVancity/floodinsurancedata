/* Flood zone at a point, from FEMA's live map service (CLAUDE.md address-tool rule, owner 2026-11-06).
   The site never computes, draws or stores a zone: it relays FEMA's own answer for a point the reader placed and
   confirmed. Loaded only after the reader taps; the page works without it (the no-JS link goes to FEMA's map).
   describe() is pure and mirrored by an independent Python oracle (tools/test_zonemap.py). */
(function () {
  "use strict";
  var NFHL = "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer";
  var GEO = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress";
  var MSC = "https://msc.fema.gov/portal/home";
  var NEAR_M = 15, WAIT_MS = 8000;
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  var ZPAGES = { AE: "ae", X: "x", VE: "ve", A: "a", AO: "ao", AH: "ah", D: "d" };

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function day(ms) {
    if (typeof ms !== "number" || !isFinite(ms)) return null;
    var d = new Date(ms); if (isNaN(d.getTime())) return null;   // fuzz 11-06: 1e300 printed "undefined NaN, NaN"
    return MONTHS[d.getUTCMonth()] + " " + d.getUTCDate() + ", " + d.getUTCFullYear();
  }
  function zoneName(a) {
    var z = String(a.FLD_ZONE || "").trim(), s = String(a.ZONE_SUBTY || "").trim();
    if (!z) return null;
    return "Zone " + z + (s ? " (" + s.toLowerCase() + ")" : "");
  }

  /* point, box, panel: FEMA query JSON, or null when that request failed or timed out. Returns lines of text. */
  function describe(point, box, panel) {
    if (!point || !box || point.error || box.error) return { kind: "down", lines: ["FEMA's map service did not answer. Check this spot on FEMA's map."] };
    var here = (point.features || []).map(function (f) { return f.attributes || {}; }).filter(function (a) { return zoneName(a); });
    if (!here.length) return { kind: "none", lines: ["FEMA's digital flood map shows no flood zone at this pin. That is not a finding of no flood risk: FEMA's digital map does not cover every place. Check this spot on FEMA's map."] };
    var seen = {}, near = [];
    here.concat((box.features || []).map(function (f) { return f.attributes || {}; })).forEach(function (a) {
      var n = zoneName(a); if (n && !seen[n]) { seen[n] = 1; near.push(n); }
    });
    var lines = [];
    var main = zoneName(here[0]);
    if (near.length > 1) lines.push("A zone line is within " + NEAR_M + " meters (about 50 feet) of this pin. FEMA's map shows: " + near.join("; ") + ".");
    else lines.push("FEMA's map shows " + main + " at this pin.");
    var sfha = String(here[0].SFHA_TF || "").toUpperCase();
    if (sfha === "T") lines.push("FEMA marks this spot as a Special Flood Hazard Area (high-risk).");
    else if (sfha === "F" && near.length === 1 && String(here[0].FLD_ZONE).trim() === "X") lines.push("FEMA does not mark this spot as a Special Flood Hazard Area.");
    var p = panel && !panel.error && (panel.features || [])[0] ? panel.features[0].attributes || {} : null;
    if (p && p.FIRM_PAN) lines.push("FEMA map panel " + String(p.FIRM_PAN).trim() + (day(p.EFF_DATE) ? ", in effect since " + day(p.EFF_DATE) : "") + ".");
    return { kind: near.length > 1 ? "near" : "one", zone: String(here[0].FLD_ZONE).trim(), lines: lines };
  }
  window.__zmDescribe = describe;   // tests call the same function the page uses

  function get(url, params) {
    var q = Object.keys(params).map(function (k) { return k + "=" + encodeURIComponent(params[k]); }).join("&");
    var ctl = window.AbortController ? new AbortController() : null;
    var t = setTimeout(function () { if (ctl) ctl.abort(); }, WAIT_MS);
    return fetch(url + "?" + q, ctl ? { signal: ctl.signal } : {}).then(function (r) { clearTimeout(t); return r.ok ? r.json() : null; })
      .catch(function () { clearTimeout(t); return null; });
  }
  function geocode(addr) {   // the Census geocoder sends no CORS header; its JSONP form answers (verified 11-06)
    return new Promise(function (ok) {
      var cb = "__zmg" + Date.now(), s = document.createElement("script"), done = false;
      var end = function (v) { if (done) return; done = true; delete window[cb]; s.remove(); ok(v); };
      window[cb] = function (d) {
        var m = d && d.result && d.result.addressMatches && d.result.addressMatches[0];
        end(m ? { lat: m.coordinates.y, lon: m.coordinates.x, matched: m.matchedAddress } : null);
      };
      s.src = GEO + "?address=" + encodeURIComponent(addr) + "&benchmark=Public_AR_Current&format=jsonp&callback=" + cb;
      s.onerror = function () { end(null); };
      setTimeout(function () { end(null); }, WAIT_MS);
      document.head.appendChild(s);
    });
  }

  function start(box) {
    var out = box.querySelector(".zm-out"), mapEl = box.querySelector(".zm-map"), map, pin, fema;
    var say = function (html) { out.innerHTML = html; };
    function showMap(lat, lon, note) {
      mapEl.style.display = "block";
      if (!map) {
        map = L.map(mapEl, { scrollWheelZoom: false });
        L.tileLayer("https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}",
          { maxZoom: 19, maxNativeZoom: 16, attribution: "Basemap: USGS The National Map" }).addTo(map);
        fema = L.GridLayer.extend({ createTile: function (c) {   // FEMA's own flood-zone layer, drawn by FEMA's server
          var img = document.createElement("img"), s = this.getTileSize(), nw = this._map.unproject([c.x * s.x, c.y * s.y], c.z),
              se = this._map.unproject([(c.x + 1) * s.x, (c.y + 1) * s.y], c.z), a = L.CRS.EPSG3857.project(nw), b = L.CRS.EPSG3857.project(se);
          img.alt = ""; img.src = NFHL + "/export?bbox=" + [a.x, b.y, b.x, a.y].join(",") + "&bboxSR=3857&imageSR=3857&size=" + s.x + "," + s.y +
            "&layers=show:28&transparent=true&format=png32&f=image";
          return img; } });
        new fema({ opacity: 0.6, attribution: "Flood zones: FEMA National Flood Hazard Layer" }).addTo(map);
        pin = L.marker([lat, lon], { draggable: true }).addTo(map);
        pin.on("dragend", function () { ask(); });
      }
      map.setView([lat, lon], 18); pin.setLatLng([lat, lon]);
      ask(note);
    }
    function ask(note) {
      say((note ? "<p>" + note + "</p>" : "") + "<p><b>Is the pin on your building?</b> Drag it onto the building if not.</p>" +
          '<button type="button" class="btn zm-ok">Yes, the pin is on my building</button>');
      out.querySelector(".zm-ok").onclick = confirm;
    }
    function confirm() {
      var ll = pin.getLatLng(), m = L.CRS.EPSG3857.project(ll), g = ll.lng + "," + ll.lat;
      say("<p>Asking FEMA's map…</p>");
      var base = { geometryType: "esriGeometryPoint", inSR: 4326, returnGeometry: "false", f: "json" };
      Promise.all([
        get(NFHL + "/28/query", Object.assign({ geometry: g, outFields: "FLD_ZONE,ZONE_SUBTY,SFHA_TF" }, base)),
        // Web Mercator units are stretched by 1/cos(latitude): scale so the box really reaches NEAR_M meters on the ground
        get(NFHL + "/28/query", { geometry: (function (k) { return [m.x - k, m.y - k, m.x + k, m.y + k]; })(NEAR_M / Math.cos(ll.lat * Math.PI / 180)).join(","), geometryType: "esriGeometryEnvelope",
                                  inSR: 3857, outFields: "FLD_ZONE,ZONE_SUBTY", returnGeometry: "false", f: "json" }),
        get(NFHL + "/3/query", Object.assign({ geometry: g, outFields: "FIRM_PAN,EFF_DATE" }, base))
      ]).then(function (r) {
        var d = describe(r[0], r[1], r[2]);
        var zl = d.zone && ZPAGES[d.zone] ? ' <a href="/flood-zones/' + ZPAGES[d.zone] + '/">What zone ' + esc(d.zone) + " means and costs</a>." : "";
        say("<p>" + d.lines.map(esc).join("</p><p>") + "</p>" + (zl ? "<p>" + zl + "</p>" : "") + box.querySelector(".zm-label").innerHTML +
            '<p><a href="' + MSC + '" rel="noopener" target="_blank">Check it on FEMA\'s map →</a></p>');
      });
    }
    box.querySelector(".zm-go").onclick = function () {
      var a = box.querySelector(".zm-addr").value.trim();
      if (a.length < 5) { say("<p>Type a street address, city and state.</p>"); return; }
      say("<p>Finding the address…</p>");
      geocode(a).then(function (r) {
        if (!r) { say("<p>The Census Bureau's address finder did not match that address. Check the spelling, or use your location and drag the pin.</p>"); return; }
        showMap(r.lat, r.lon, "Matched address: " + esc(r.matched) + ". The pin is an estimate along the street, not your exact building.");
      });
    };
    box.querySelector(".zm-loc").onclick = function () {
      if (!navigator.geolocation) { say("<p>This browser cannot share a location. Type the address instead.</p>"); return; }
      say("<p>Finding your location…</p>");
      navigator.geolocation.getCurrentPosition(function (p) { showMap(p.coords.latitude, p.coords.longitude, "This is where your device is, which may not be the building you mean."); },
        function () { say("<p>Location was not shared. Type the address instead.</p>"); }, { timeout: WAIT_MS });
    };
  }
  window.__zmStart = start;
})();
