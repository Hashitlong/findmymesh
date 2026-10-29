// Pulls the MeshCore map node file, keeps U.S. nodes, assigns states, writes site/nodes.json
// Run from anywhere: node fetch_nodes.mjs [path/to/nodes.bin]  (uses cached file if given)
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { unpack } = require('msgpackr');
const topo = require('topojson-client');
const { geoContains, geoAlbersUsa } = require('d3-geo');
const here = path.dirname(fileURLToPath(import.meta.url));
const SITE = path.join(here, '..');
const URL = 'https://map.meshcore.io/api/v1/nodes?binary=1&short=1';
const UA = 'FindMyMesh/0.1 (+https://findmymesh.com; rogerprw@gmail.com) daily-build';

let buf;
if (process.argv[2] && fs.existsSync(process.argv[2])) buf = fs.readFileSync(process.argv[2]);
else {
  const r = await fetch(URL, { headers: { 'User-Agent': UA } });
  if (!r.ok) throw new Error('nodes fetch failed ' + r.status);
  buf = Buffer.from(await r.arrayBuffer());
}
const all = unpack(buf);
const us = JSON.parse(fs.readFileSync(path.join(SITE, '..', 'geo', 'states-10m.json')));
const states = topo.feature(us, us.objects.states).features;
const FIPS = {"01":"AL","02":"AK","04":"AZ","05":"AR","06":"CA","08":"CO","09":"CT","10":"DE","11":"DC","12":"FL","13":"GA","15":"HI","16":"ID","17":"IL","18":"IN","19":"IA","20":"KS","21":"KY","22":"LA","23":"ME","24":"MD","25":"MA","26":"MI","27":"MN","28":"MS","29":"MO","30":"MT","31":"NE","32":"NV","33":"NH","34":"NJ","35":"NM","36":"NY","37":"NC","38":"ND","39":"OH","40":"OK","41":"OR","42":"PA","44":"RI","45":"SC","46":"SD","47":"TN","48":"TX","49":"UT","50":"VT","51":"VA","53":"WA","54":"WV","55":"WI","56":"WY"};
// bounding boxes to speed up point-in-state tests
const boxes = states.map(f => { let minX=180,minY=90,maxX=-180,maxY=-90; const walk=c=>{ if(typeof c[0]==='number'){ if(c[0]<minX)minX=c[0]; if(c[0]>maxX)maxX=c[0]; if(c[1]<minY)minY=c[1]; if(c[1]>maxY)maxY=c[1]; } else c.forEach(walk); }; walk(f.geometry.coordinates); return [minX,minY,maxX,maxY]; });
const proj = geoAlbersUsa().scale(1300).translate([487.5, 305]);
const now = Date.now();
const out = [], perState = {};
let candidates = 0;
for (const n of all) {
  if (typeof n.lat !== 'number' || typeof n.lon !== 'number') continue;
  if (!((n.lat > 24 && n.lat < 50 && n.lon > -125 && n.lon < -66) || (n.lat > 51 && n.lon < -129) || (n.lat < 23 && n.lon < -154))) continue;
  candidates++;
  let st = null;
  for (let i = 0; i < states.length; i++) {
    const b = boxes[i];
    if (n.lon < b[0] || n.lon > b[2] || n.lat < b[1] || n.lat > b[3]) continue;
    if (geoContains(states[i], [n.lon, n.lat])) { st = FIPS[states[i].id]; break; }
  }
  if (!st) continue;
  const p = proj([n.lon, n.lat]); if (!p) continue;
  const days = n.la ? Math.max(0, Math.round((now - new Date(n.la)) / 864e5)) : null;
  out.push([+p[0].toFixed(1), +p[1].toFixed(1), n.t, days, st]);
  const s = perState[st] ||= { total: 0, repeaters: 0, companions: 0, rooms: 0, active30: 0, freq: {} };
  s.total++; if (n.t === 2) s.repeaters++; else if (n.t === 1) s.companions++; else if (n.t === 3) s.rooms++;
  if (days !== null && days <= 30) s.active30++;
  if (n.p && n.p.freq) s.freq[n.p.freq] = (s.freq[n.p.freq] || 0) + 1;
}
for (const s of Object.values(perState)) s.freq = Object.entries(s.freq).sort((a, b) => b[1] - a[1]).slice(0, 3);
const result = { fetched: new Date().toISOString().slice(0, 10), worldwide: all.length, us: out.length, perState, nodes: out };
fs.writeFileSync(path.join(SITE, 'nodes.json'), JSON.stringify(result));
console.log('worldwide', all.length, 'us candidates', candidates, 'assigned to states', out.length, 'KB', Math.round(JSON.stringify(result).length / 1024));
console.log('NC', perState.NC, 'TX total', perState.TX && perState.TX.total);
