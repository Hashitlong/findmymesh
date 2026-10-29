"""Static site generator for Find My Mesh.
Usage: python3 gen.py [--site https://domain] -> writes ../dist/
Reads: groups.json, usmap.json, content/*.json (optional), removed_groups.csv
"""
import json, os, re, math, html, csv, sys, shutil, random, glob
import markdown as _md
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import brand as _brand

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
DIST = f'{ROOT}/dist'
CONTENT = f'{REPO}/content'
NOINDEX = '--noindex' in sys.argv
import datetime as _dt, zoneinfo as _zi
TODAY = _dt.datetime.now(_zi.ZoneInfo('America/New_York')).strftime('%Y-%m-%d')
SITE_URL = ''
if '--site' in sys.argv:
    SITE_URL = sys.argv[sys.argv.index('--site') + 1].rstrip('/')
NAME = 'Find My Mesh'

GROUPS = json.load(open(f'{ROOT}/groups.json'))
USMAP = json.load(open(f'{ROOT}/usmap.json'))
REMOVED = sum(1 for _ in csv.DictReader(open(f'{REPO}/removed_groups.csv')))
def load(name):
    p = f'{CONTENT}/{name}.json'
    return json.load(open(p)) if os.path.exists(p) else None
GUIDES, HW, VIDEOS = load('guides'), load('hardware'), load('videos')
NODES = json.load(open(f'{ROOT}/nodes.json')) if os.path.exists(f'{ROOT}/nodes.json') else None
def node_stats(code): return (NODES or {}).get('perState', {}).get(code)
TESTED = load('tested')  # {"owner": "...", "items": [{"name","category","amazon_url","used_for","verdict","tested_since"}]}
HAS_TESTED = bool(TESTED and TESTED.get('items'))

def load_posts():
    posts = []
    for f in sorted(glob.glob(f'{CONTENT}/blog/*.md')):
        if os.path.basename(f).lower() == 'readme.md': continue
        txt = open(f).read()
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', txt, re.S)
        if not m: continue
        meta, body = {}, m.group(2)
        cur = None
        for line in m.group(1).splitlines():
            if re.match(r'^\s*-\s+name:', line):
                cur = {'name': line.split('name:', 1)[1].strip()}; meta.setdefault('products', []).append(cur)
            elif cur is not None and re.match(r'^\s{4,}\w+:', line):
                k, v = line.strip().split(':', 1); cur[k.strip()] = v.strip()
            elif re.match(r'^\w+:', line):
                k, v = line.split(':', 1); cur = None
                if k.strip() == 'products': meta['products'] = []
                else: meta[k.strip()] = v.strip()
        if not meta.get('title') or not meta.get('date'): continue
        if meta['date'] > TODAY: continue  # scheduled for later; the nightly rebuild publishes it
        slug_ = os.path.basename(f)[:-3]
        posts.append({'slug': slug_, 'page': f'blog-{slug_}.html', 'body': body, **meta})
    posts.sort(key=lambda p: p['date'], reverse=True)
    return posts
POSTS = load_posts()
HAS_BLOG = bool(POSTS)

STATES = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","DC":"District of Columbia","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
NEIGHBORS = {"AL":"FL GA MS TN","AK":"","AZ":"CA CO NV NM UT","AR":"LA MS MO OK TN TX","CA":"AZ NV OR","CO":"AZ KS NE NM OK UT WY","CT":"MA NY RI","DE":"MD NJ PA","DC":"MD VA","FL":"AL GA","GA":"AL FL NC SC TN","HI":"","ID":"MT NV OR UT WA WY","IL":"IN IA KY MO WI","IN":"IL KY MI OH","IA":"IL MN MO NE SD WI","KS":"CO MO NE OK","KY":"IL IN MO OH TN VA WV","LA":"AR MS TX","ME":"NH","MD":"DE PA VA WV DC","MA":"CT NH NY RI VT","MI":"IN OH WI","MN":"IA ND SD WI","MS":"AL AR LA TN","MO":"AR IL IA KS KY NE OK TN","MT":"ID ND SD WY","NE":"CO IA KS MO SD WY","NV":"AZ CA ID OR UT","NH":"ME MA VT","NJ":"DE NY PA","NM":"AZ CO OK TX UT","NY":"CT MA NJ PA VT","NC":"GA SC TN VA","ND":"MN MT SD","OH":"IN KY MI PA WV","OK":"AR CO KS MO NM TX","OR":"CA ID NV WA","PA":"DE MD NJ NY OH WV","RI":"CT MA","SC":"GA NC","SD":"IA MN MT NE ND WY","TN":"AL AR GA KY MS MO NC VA","TX":"AR LA NM OK","UT":"AZ CO ID NV NM WY","VT":"MA NH NY","VA":"KY MD NC TN WV DC","WA":"ID OR","WV":"KY MD OH PA VA","WI":"IL IA MI MN","WY":"CO ID MT NE SD UT"}
TILES = {"AK":[0,0],"ME":[0,11],"WI":[1,6],"VT":[1,10],"NH":[1,11],"WA":[2,1],"ID":[2,2],"MT":[2,3],"ND":[2,4],"MN":[2,5],"IL":[2,6],"MI":[2,7],"NY":[2,9],"MA":[2,10],"OR":[3,1],"NV":[3,2],"WY":[3,3],"SD":[3,4],"IA":[3,5],"IN":[3,6],"OH":[3,7],"PA":[3,8],"NJ":[3,9],"CT":[3,10],"RI":[3,11],"CA":[4,1],"UT":[4,2],"CO":[4,3],"NE":[4,4],"MO":[4,5],"KY":[4,6],"WV":[4,7],"VA":[4,8],"MD":[4,9],"DE":[4,10],"AZ":[5,2],"NM":[5,3],"KS":[5,4],"AR":[5,5],"TN":[5,6],"NC":[5,7],"SC":[5,8],"DC":[5,9],"OK":[6,4],"LA":[6,5],"MS":[6,6],"AL":[6,7],"GA":[6,8],"HI":[7,0],"TX":[7,4],"FL":[7,9]}

e = lambda s: html.escape(str(s if s is not None else ''), quote=True)
def slug(s): return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')
def state_page(code): return slug(STATES[code]) + '.html'
CHECKED = max(g['last_checked'] for g in GROUPS)
def fmt_date(d):
    y, m, dd = map(int, d.split('-'))
    return f"{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m-1]} {dd}, {y}"
CHECKED_H = fmt_date(CHECKED)
NODE_DATE = fmt_date(NODES['fetched']) if NODES else ''
NODE_CREDIT = f'<p class="mapnote">Node locations from <a href="https://map.meshcore.io/" target="_blank" rel="noopener">map.meshcore.io</a>, the MeshCore community map, as of {NODE_DATE}. Only nodes their owners chose to publish appear.</p>' if NODES else ''
def live_map_link(code):
    # the community map accepts lat/lon/zoom in the URL (per the MeshCore blog's embed instructions)
    c = STATE_CENTER.get(code)
    return f'https://map.meshcore.io/?lat={c[0]}&lon={c[1]}&zoom={c[2]}' if c else 'https://map.meshcore.io/'
STATE_CENTER = {"AL":(32.8,-86.8,7),"AK":(64,-152,4),"AZ":(34.3,-111.7,7),"AR":(34.9,-92.4,7),"CA":(37.2,-119.5,6),"CO":(39,-105.5,7),"CT":(41.6,-72.7,9),"DE":(39,-75.5,9),"DC":(38.9,-77.03,11),"FL":(28.6,-82.4,7),"GA":(32.7,-83.4,7),"HI":(20.8,-156.3,7),"ID":(44.4,-114.6,6),"IL":(40,-89.2,7),"IN":(39.9,-86.3,7),"IA":(42.1,-93.5,7),"KS":(38.5,-98.4,7),"KY":(37.5,-85.3,7),"LA":(31.1,-91.9,7),"ME":(45.4,-69.2,7),"MD":(39,-76.8,8),"MA":(42.3,-71.8,8),"MI":(44.3,-85.4,6),"MN":(46.3,-94.3,6),"MS":(32.7,-89.7,7),"MO":(38.4,-92.5,7),"MT":(47,-109.6,6),"NE":(41.5,-99.8,7),"NV":(39.3,-116.6,6),"NH":(43.7,-71.6,8),"NJ":(40.2,-74.7,8),"NM":(34.4,-106.1,7),"NY":(42.9,-75.5,7),"NC":(35.5,-79.4,7),"ND":(47.5,-100.5,7),"OH":(40.3,-82.8,7),"OK":(35.6,-97.5,7),"OR":(43.9,-120.6,6),"PA":(40.9,-77.8,7),"RI":(41.7,-71.5,10),"SC":(33.9,-80.9,7),"SD":(44.4,-100.2,7),"TN":(35.9,-86.4,7),"TX":(31.5,-99.3,6),"UT":(39.3,-111.7,7),"VT":(44,-72.7,8),"VA":(37.5,-78.8,7),"WA":(47.4,-120.5,7),"WV":(38.6,-80.6,7),"WI":(44.6,-89.9,6),"WY":(43,-107.5,7)}
def num(n):
    try: return f"{int(n):,}"
    except: return e(n)
def safe(u): return u if re.match(r'^https?://', u or '') else ''
def host(u):
    m = re.match(r'^https?://(?:www\.)?([^/?#]+)(/[^?#]*)?', u or '')
    if not m: return ''
    p = (m.group(2) or '').rstrip('/')
    return (m.group(1) + p)[:52]

# group slugs
seen = set()
for g in GROUPS:
    s = slug(re.sub(r'\(.*?\)', '', g['group_name'])) or 'group'
    base, i = s, 2
    while s in seen: s = f'{base}-{i}'; i += 1
    seen.add(s); g['slug'] = s; g['page'] = f'group-{s}.html'

by_state = {}
for g in GROUPS:
    for s in g['state']: by_state.setdefault(s, []).append(g)
def count(s): return len(by_state.get(s, []))
RANK = {'High': 0, 'Medium': 1, 'Low': 2}
def sort_groups(arr): return sorted(arr, key=lambda g: (RANK[g['confidence']], g['group_name'].lower()))

def miles(a, b):
    R = 3958.8
    la1, lo1, la2, lo2 = map(math.radians, [a['lat'], a['lon'], b['lat'], b['lon']])
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))
PINNED = [g for g in GROUPS if g.get('pin') and 'x' in g['pin']]

# ---------- small svg parts ----------
ICON = {
 'web': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>',
 'discord': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 7c3-1.3 7-1.3 10 0l1.5 9.5c-1.6 1.2-3.2 2-4.8 2.4l-.9-1.8M7 7 5.5 16.5c1.6 1.2 3.2 2 4.8 2.4l.9-1.8"/><circle cx="9.5" cy="12.5" r="1"/><circle cx="14.5" cy="12.5" r="1"/></svg>',
 'facebook': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M15.5 8h-2a2 2 0 0 0-2 2v11M9 13h6"/></svg>',
 'map': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="2.2"/><path d="M7.8 7.8a6 6 0 0 0 0 8.4M16.2 7.8a6 6 0 0 1 0 8.4M4.9 4.9a10 10 0 0 0 0 14.2M19.1 4.9a10 10 0 0 1 0 14.2"/></svg>',
 'chat': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/></svg>',
 'out': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>',
}
SIG_LABEL = {'High': 'Verified', 'Medium': 'Partly verified', 'Low': 'Site down'}
SIG_TITLE = {'High': "We opened the group's own website and it covers MeshCore", 'Medium': 'No website; confirmed through Facebook or Discord plus a regional directory', 'Low': 'Website was down on the check date'}
def sig(c):
    on = {'High': 3, 'Medium': 2, 'Low': 1}[c]
    bars = ''.join(f'<rect class="{"on" if i < on else ""}" x="{i*6}" y="{12-(i+1)*4}" width="4" height="{(i+1)*4}" rx="1"/>' for i in range(3))
    return f'<span class="sig {c}" title="{e(SIG_TITLE[c])}"><svg width="16" height="12" viewBox="0 0 16 12" aria-hidden="true">{bars}</svg>{SIG_LABEL[c]}</span>'

def contours(seed=7, w=1200, h=420, peaks=3, rings=8):
    rnd = random.Random(seed)
    paths = []
    for p in range(peaks):
        cx, cy = rnd.uniform(0.15, 0.95)*w, rnd.uniform(0.1, 0.9)*h
        ph = [rnd.uniform(0, 6.28) for _ in range(3)]
        for r in range(1, rings+1):
            R = r * rnd.uniform(26, 34)
            pts = []
            for k in range(73):
                a = k/72*2*math.pi
                rr = R*(1 + .16*math.sin(3*a+ph[0]) + .09*math.sin(5*a+ph[1]) + .05*math.sin(2*a+ph[2]+r*.3))
                pts.append(f'{cx+rr*math.cos(a):.0f},{cy+rr*.62*math.sin(a):.0f}')
            paths.append('M' + 'L'.join(pts) + 'Z')
    return f'<svg class="contours" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><path d="{" ".join(paths)}" fill="none" stroke="currentColor" stroke-width="1.1"/></svg>'

def readout(s):
    s = e(s)
    s = re.sub(r'(\d{3}\.\d+ ?MHz)', r'<b>\1</b>', s, count=1)
    return f'<span class="readout" aria-label="Radio settings">{s}</span>'

def chip(url, icon, label, n=''):
    if not safe(url): return ''
    return f'<a class="chip" href="{e(url)}" rel="noopener" target="_blank">{ICON[icon]}{label}{f" <span class=n>{n}</span>" if n else ""}</a>'
def other_label(u):
    return 'Telegram' if 't.me' in u else 'Reddit' if 'reddit' in u else 'IRC' if 'libera' in u else 'GitHub' if 'github' in u else 'Matrix' if 'matrix' in u else 'Chat'

def group_chips(g):
    fb_n = g['facebook_size'].replace(' members', '').replace(' followers', ' followers') if g['facebook_size'] else ''
    return ''.join([chip(g['website_url'], 'web', 'Website'), chip(g['discord_url'], 'discord', 'Discord', num(g['discord_members']) if g['discord_members'] else ''),
                    chip(g['facebook_url'], 'facebook', 'Facebook', fb_n), chip(g['other_chat_url'], 'chat', other_label(g['other_chat_url'])) if g['other_chat_url'] else '',
                    chip(g['live_map_url'], 'map', KIND_LABEL[map_kind(g['live_map_url'])] if safe(g['live_map_url']) else 'Map')])

def group_row(g, show_state=False, dist=None):
    st = ', '.join(f'<a href="{state_page(s)}">{s}</a>' for s in g['state'] if s in STATES)
    where = e(g['area_covered']) + (f' · {st}' if show_state else '')
    extra = f'<span class="mono small">{dist:,.0f} mi</span>' if dist is not None else ''
    return f'''<div class="grow" data-st="{' '.join(g['state'])}" data-c="{g['confidence']}" data-d="{1 if g['discord_url'] else 0}" data-f="{1 if g['facebook_url'] else 0}" data-m="{1 if g['live_map_url'] else 0}" data-r="{1 if g['radio_settings_confirmed'] else 0}" data-t="{e((g['group_name']+' '+g['area_covered']).lower())}">
  <div class="who"><h3><a href="{g['page']}">{e(g['group_name'])}</a></h3><p class="where">{where}</p></div>
  <div class="side">{sig(g['confidence'])}{extra}{'<span class="tag">Mostly Meshtastic</span>' if g.get('mostly_meshtastic') else '<span class="tag">Also Meshtastic</span>' if g['runs_meshtastic_too']=='yes' else ''}</div>
  <div class="acts">{group_chips(g)}</div>
</div>'''

# ---------- maps ----------
def us_map(pins=True, hops=True, link_states=True, cls='usmap'):
    parts = []
    for code, d in USMAP['states'].items():
        has = ' has' if count(code) else ''
        p = f'<path class="st{has}" d="{d}"/>'
        if link_states:
            p = f'<a href="{state_page(code)}" aria-label="{e(STATES[code])}, {count(code)} groups"><title>{e(STATES[code])}: {count(code)} group{"s" if count(code)!=1 else ""}</title>{p}</a>'
        parts.append(p)
    hop_svg, pin_svg = '', ''
    node_svg = ''
    if NODES:
        dots_old, dots_new = [], []
        for x, y, t, days, st in NODES['nodes']:
            if t not in (2, 3): continue
            (dots_new if (days is not None and days <= 30) else dots_old).append(f'M{x},{y}h.01')
        node_svg = f'<path class="nodes old" d="{" ".join(dots_old)}"/><path class="nodes new" d="{" ".join(dots_new)}"/>'
    if hops:
        drawn = set()
        for g in PINNED:
            near = sorted(((miles(g['pin'], o['pin']), o) for o in PINNED if o is not g and (o['pin']['x'], o['pin']['y']) != (g['pin']['x'], g['pin']['y'])), key=lambda t: t[0])[:2]
            for d, o in near:
                if d > 260: continue
                k = tuple(sorted([g['slug'], o['slug']]))
                if k in drawn: continue
                drawn.add(k)
                hop_svg += f'<path class="hop" d="M{g["pin"]["x"]},{g["pin"]["y"]}L{o["pin"]["x"]},{o["pin"]["y"]}"/>'
    if pins:
        for i, g in enumerate(PINNED):
            x, y = g['pin']['x'], g['pin']['y']
            ring = f'<circle class="ring" cx="{x}" cy="{y}" r="6" style="animation-delay:{(i*0.37)%3.2:.2f}s"/>' if i % 3 == 0 else ''
            pin_svg += f'<a href="{g["page"]}" aria-label="{e(g["group_name"])}, {e(g["pin"]["city"])}">{ring}<circle class="pin" cx="{x}" cy="{y}" r="4.6"><title>{e(g["group_name"])} — {e(g["pin"]["city"])}, {g["pin"]["state"]}</title></circle></a>'
    return f'<svg class="{cls}" viewBox="0 0 975 610" aria-label="Map of U.S. MeshCore groups. State and group links are also listed below.">{"".join(parts)}<path class="borders" d="{USMAP["borders"]}"/>{node_svg}<g>{hop_svg}</g><g>{pin_svg}</g></svg>'

def state_map(code):
    if code not in USMAP['states']: return ''
    x0, y0 = USMAP['bounds'][code][0]; x1, y1 = USMAP['bounds'][code][1]
    pad = max(18, (x1-x0)*.12, (y1-y0)*.12)
    x0, y0, x1, y1 = x0-pad, y0-pad, x1+pad, y1+pad
    show = [code] + [n for n in NEIGHBORS.get(code, '').split() if n]
    parts = []
    for c in show:
        if c not in USMAP['states']: continue
        cls = 'st has' if c == code else 'st'
        parts.append(f'<a href="{state_page(c)}"><title>{e(STATES[c])}</title><path class="{cls}" d="{USMAP["states"][c]}"/></a>')
    pins = ''
    if NODES:
        r = max(1.0, (x1-x0)/400)
        dots_old, dots_new = [], []
        for x, y, t, days, st in NODES['nodes']:
            if t not in (2, 3) or not (x0 <= x <= x1 and y0 <= y <= y1): continue
            (dots_new if (days is not None and days <= 30) else dots_old).append(f'M{x},{y}h.01')
        pins += f'<path class="nodes old" style="stroke-width:{r*2:.1f}" d="{" ".join(dots_old)}"/><path class="nodes new" style="stroke-width:{r*2:.1f}" d="{" ".join(dots_new)}"/>'
    for g in PINNED:
        x, y = g['pin']['x'], g['pin']['y']
        if x0 <= x <= x1 and y0 <= y <= y1:
            pins += f'<a href="{g["page"]}"><circle class="pin" cx="{x}" cy="{y}" r="{max(3.2,(x1-x0)/90):.1f}"><title>{e(g["group_name"])} — {e(g["pin"]["city"])}</title></circle></a>'
    return f'<svg class="usmap" viewBox="{x0:.0f} {y0:.0f} {x1-x0:.0f} {y1-y0:.0f}" role="img" aria-label="Map of {e(STATES[code])} with group locations">{"".join(parts)}{pins}</svg>'

def tiles():
    out = []
    for s, (r, c) in TILES.items():
        n = count(s); cl = 'c0' if n == 0 else 'c1' if n == 1 else 'c2' if n <= 3 else 'c3'
        out.append(f'<a class="tile {cl}" style="grid-row:{r+1};grid-column:{c+1}" href="{state_page(s)}" aria-label="{e(STATES[s])}: {n} group{"s" if n!=1 else ""}">{s}<small>{n or "–"}</small></a>')
    return f'''<div class="tiles-wrap"><div class="tiles">{"".join(out)}</div>
<div class="key" aria-label="Key"><span><i style="background:var(--sunk)"></i>No group found yet</span><span><i style="background:color-mix(in srgb,var(--signal) 22%,var(--sunk))"></i>1 group</span><span><i style="background:color-mix(in srgb,var(--signal) 52%,var(--sunk))"></i>2–3 groups</span><span><i style="background:var(--signal)"></i>4 or more</span>
<p class="small sub" style="margin-top:6px">Counts include regional groups that cover a state. No group near you? <a href="add.html">Tell us about one</a> or <a href="start.html">start one</a>.</p></div></div>'''

# ---------- page shell ----------
NAV = [('near-me.html', 'Find a group', 'find'), ('start.html', 'Get started', 'start'), ('gear.html', 'Gear', 'gear'),
       ('live-maps.html', 'Live maps', 'maps'), ('chats.html', 'Chats', 'chats'), ('learn.html', 'Learn', 'learn')] + ([('blog.html', 'Blog', 'blog')] if HAS_BLOG else [])
FONTS = 'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..100,700..900&family=Atkinson+Hyperlegible:wght@400;700&family=IBM+Plex+Mono:wght@400;500&display=swap'

BRAND_MARK = _brand.mark_svg(32, ink='currentColor', signal='var(--signal)').replace('<svg ', '<svg aria-hidden="true" class="brandmark" ', 1)
def header(cur):
    CUR = ' aria-current="page"'
    nav = ''.join(f'<a href="{h}"{CUR if k==cur else ""}>{t}</a>' for h, t, k in NAV)
    mnav = ''.join(f'<a href="{h}">{t}</a>' for h, t, k in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="masthead"><div class="wrap">
  <a class="brand" href="index.html">{BRAND_MARK}Find My <b>Mesh</b></a>
  <nav class="nav" aria-label="Main">{nav}</nav>
  <a class="btn cta" href="add.html">Add your group</a>
  <details class="menu"><summary aria-label="Menu"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>Menu</summary>
    <nav class="menu-panel" aria-label="Main">{mnav}<a href="directory.html">All groups</a><a class="btn" href="add.html">Add your group</a></nav></details>
</div></header>'''

def footer():
    return f'''<footer class="foot"><div class="wrap">
<div class="cols4">
 <div><p class="foothead">Find</p><ul><li><a href="near-me.html">Groups near you</a></li><li><a href="states.html">All states</a></li><li><a href="directory.html">All groups</a></li><li><a href="live-maps.html">Live maps</a></li><li><a href="chats.html">Discord &amp; Facebook</a></li></ul></div>
 <div><p class="foothead">Get started</p><ul><li><a href="start.html">What is MeshCore</a></li><li><a href="meshcore-vs-meshtastic.html">MeshCore vs Meshtastic</a></li><li><a href="start.html#setup">Setup guide</a></li><li><a href="repeaters.html">Build a repeater</a></li><li><a href="glossary.html">Glossary</a></li></ul></div>
 <div><p class="foothead">Gear &amp; tools</p><ul><li><a href="gear.html">Devices &amp; where to buy</a></li>{'<li><a href="gear-i-use.html">Gear I use</a></li>' if HAS_TESTED else ''}{'<li><a href="blog.html">Reviews &amp; comparisons</a></li>' if HAS_BLOG else ''}<li><a href="software.html">Software</a></li><li><a href="videos.html">Videos</a></li><li><a href="learn.html">Docs &amp; wikis</a></li></ul></div>
 <div><p class="foothead">This site</p><ul><li><a href="about.html">How we check listings</a></li><li><a href="add.html">Add a listing</a></li><li><a href="add.html#fix">Report a broken link</a></li></ul></div>
</div>
<div class="fine"><span>Independent community directory, not endorsed by any MeshCore or Meshtastic project. MeshCore and Meshtastic are trademarks of their respective owners and are used here only to identify the projects. As an Amazon Associate I earn from qualifying purchases; links marked "Paid link" on the gear and review pages are affiliate links. Product prices and availability shown are accurate as of the date/time indicated and are subject to change; any price and availability information displayed on Amazon at the time of purchase will apply. <a href="about.html#disclosures">Disclosures &amp; privacy</a>.</span><span class="mono">Links checked {CHECKED_H}</span></div>
</div></footer>'''

PAGES = {}
def page(fname, title, desc, cur, body, scripts=''):
    full_title = title if title == NAME else f'{title} · {NAME}'
    canon = f'<link rel="canonical" href="{SITE_URL}/{"" if fname=="index.html" else fname.replace(".html","")}">' if SITE_URL else ''
    robots = '<meta name="robots" content="noindex, nofollow">\n' if NOINDEX else ''
    head = f'''{robots}<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">{canon}
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/site.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon.ico" sizes="32x32"><link rel="apple-touch-icon" href="assets/icon-180.png"><link rel="manifest" href="site.webmanifest"><meta name="theme-color" content="#b4541a">
<meta property="og:image" content="{SITE_URL + "/" if SITE_URL else ""}assets/og.png">'''
    content = f'{header(cur)}\n<main id="main">{body}</main>\n{footer()}\n{scripts}'
    PAGES[fname] = (head, content)

def band(inner, seed=3):
    return f'<section class="band">{contours(seed)}<div class="wrap">{inner}</div></section>'
def pagehead(h1, lede='', crumbs=None, extra=''):
    cr = ''
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Breadcrumb">' + ' <span aria-hidden="true">/</span> '.join(f'<a href="{h}">{e(t)}</a>' if h else f'<span>{e(t)}</span>' for h, t in crumbs) + '</nav>'
    return f'<div class="pagehead">{cr}<h1>{h1}</h1>{f"<p class=lede>{lede}</p>" if lede else ""}{extra}</div>'
def lk(name, hst, url, about, badge=''):
    return f'<a class="lk" href="{e(url)}" target="_blank" rel="noopener">{f"<span class=badge>{e(badge)}</span>" if badge else ""}<strong>{e(name)}</strong><span>{e(about)}</span><span class="host">{e(hst)}</span></a>'
def sources(lst):
    if not lst: return ''
    return '<div class="sources"><span class="label">Sources</span><ul>' + ''.join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s.get("title") or host(s["url"]))}</a></li>' for s in lst if safe(s.get('url'))) + '</ul></div>'

# ---------- data used on several pages ----------
OFFICIAL = [
  ('MeshCore', 'meshcore.io', 'https://meshcore.io/', "The project's home: app downloads and getting started.", ''),
  ('Web flasher', 'flasher.meshcore.io', 'https://flasher.meshcore.io/', 'Install companion, repeater or room server firmware from your browser.', ''),
  ('MeshCore.io Discord', 'discord.gg/meshcore', 'https://discord.gg/meshcore', 'The official Discord server. 14,943 members.', 'Discord'),
  ('MeshCore Official', 'facebook.com/groups/meshcore', 'https://www.facebook.com/groups/meshcore', 'Public Facebook group. 33.6K members.', 'Facebook'),
  ('r/meshcore', 'reddit.com/r/meshcore', 'https://www.reddit.com/r/meshcore/', 'The main MeshCore subreddit.', 'Reddit'),
  ('Documentation', 'docs.meshcore.io', 'https://docs.meshcore.io/', 'FAQ, CLI commands, packet format.', ''),
]
TOOLS = [
  ("Official", "From the MeshCore project.", [
    ("MeshCore app","meshcore.io","https://meshcore.io/","Phone, desktop and web app for companion radios."),
    ("Web flasher","flasher.meshcore.io","https://flasher.meshcore.io/","Install firmware from a Chrome-based browser."),
    ("Repeater USB config","config.meshcore.io","https://config.meshcore.io/","Configure a repeater over USB."),
    ("Official node map","map.meshcore.io","https://map.meshcore.io/","Worldwide map of nodes people have uploaded."),
    ("Documentation","docs.meshcore.io","https://docs.meshcore.io/","FAQ, CLI commands, packet format, companion protocol."),
    ("Firmware source","github.com/meshcore-dev","https://github.com/meshcore-dev/MeshCore","The MeshCore firmware repository.")]),
  ("Community firmware", "Alternative builds. Not supported by the official project.", [
    ("mishmesh","github.com/burakcan","https://github.com/burakcan/MeshCore-mishmesh","Standalone companion firmware for MeshCore radios."),
    ("ZephCore","github.com/liquidraver","https://github.com/liquidraver/ZephCore","MeshCore port to the Zephyr RTOS."),
    ("CAIRN","github.com/cvhviz","https://github.com/cvhviz/CAIRN","Touch-screen companion firmware for several boards.")]),
  ("Maps and analyzers", "What regional groups run to show live traffic.", [
    ("meshcore-mqtt-live-map","github.com/yellowcooln","https://github.com/yellowcooln/meshcore-mqtt-live-map","Live traffic map with animated routes. Powers many regional maps."),
    ("CoreScope","github.com/Kpa-clawbot","https://github.com/Kpa-clawbot/CoreScope","Self-hosted packet analyzer with live map, replay and analytics."),
    ("meshcoretomqtt","github.com/Cisien","https://github.com/cisien/meshcoretomqtt","Sends a node's packet data to MQTT. This is the observer piece."),
    ("MeshCore Viewshed (QGIS)","github.com/alanmazzotta","https://github.com/alanmazzotta/MeshCore_QGIS","Terrain-based coverage analysis for planning repeaters.")]),
  ("Desktop, phone and web tools", "Dashboards, scanners and signal testers.", [
    ("MeshMonitor","github.com/Yeraze","https://github.com/Yeraze/meshmonitor","Web dashboard for monitoring mesh nodes. Supports MeshCore."),
    ("Remote Terminal for MeshCore","github.com/jkingsman","https://github.com/jkingsman/Remote-Terminal-for-MeshCore","Remote client with packet capture, bots and MQTT."),
    ("MeshConsole","pypi.org","https://pypi.org/project/meshconsole/","Command line and web dashboard for Meshtastic and MeshCore."),
    ("MeshCore Insights","github.com/BomBefok","https://github.com/BomBefok/MeshcoreInsights","Desktop dashboard: live map, messaging, node analysis."),
    ("MeshCoreScanner","App Store","https://apps.apple.com/us/app/meshcorescanner/id6761951768","iPhone app that maps repeater coverage as you drive."),
    ("MeshCore Signal Tester","F-Droid","https://f-droid.org/packages/cz.kyblsoft.meshcore.signaltester/","Android signal monitor with SNR and RSSI charts.")]),
  ("Home Assistant, bots and bridges", "Connect the mesh to other systems.", [
    ("meshcore-ha","github.com/meshcore-dev","https://github.com/meshcore-dev/meshcore-ha","Home Assistant integration for monitoring and control."),
    ("MESH-API","github.com/mr-tbot","https://github.com/mr-tbot/mesh-api","Routes mesh messages to AI and outside APIs. Experimental.")]),
  ("Developer libraries", "Build your own tools.", [
    ("meshcore-cli","github.com/meshcore-dev","https://github.com/meshcore-dev/meshcore-cli","Command-line interface to a MeshCore node."),
    ("meshcore_py","github.com/meshcore-dev","https://github.com/meshcore-dev/meshcore_py","Python bindings."),
    ("meshcore.js","github.com/meshcore-dev","https://github.com/meshcore-dev/meshcore.js","JavaScript library for companion devices.")]),
]
NATIONAL_MAPS = [
  ("Official MeshCore node map","map.meshcore.io","https://map.meshcore.io/","Nodes people have uploaded, worldwide. Zoom to your area."),
  ("meshcoretel.io","meshcoretel.io","https://meshcoretel.io/","Public telemetry with live packet animations, by region and country."),
  ("MeshMapper","meshmapper.net","https://meshmapper.net/","Coverage maps for many U.S. regions."),
]
LEARN_DOCS = [
  ("MeshCore documentation","docs.meshcore.io","https://docs.meshcore.io/","Official FAQ, CLI reference and protocol docs."),
  ("EastMesh wiki","wiki.eastmesh.au","https://wiki.eastmesh.au/","Deep dives on routing, packets and encryption."),
  ("LILYGO wiki: MeshCore","wiki.lilygo.cc","https://wiki.lilygo.cc/open-source/meshcore/","Setup notes for LILYGO boards."),
  ("Mesh 101","mesh101.com","https://mesh101.com/","Beginner guides."),
  ("LetsMesh Forum","forum.letsmesh.net","https://forum.letsmesh.net/","Hardware, firmware and troubleshooting threads."),
]
LEARN_LISTS = [
  ("awesome-meshcore","github.com/samuk","https://github.com/samuk/awesome-meshcore","Community-curated list of MeshCore resources."),
  ("meshcore-index","github.com/meshcore-cz","https://github.com/meshcore-cz/meshcore-index","Open catalog of the MeshCore ecosystem, including networks."),
  ("meshcore.ninja","meshcore.ninja","https://meshcore.ninja/","Browsable catalog built from meshcore-index."),
  ("Cascadia Mesh: other meshes","cascadiamesh.org","https://cascadiamesh.org/other-meshes/","List of U.S. meshes kept by Cascadia Mesh."),
]
LEARN_READ = [
  ("MeshCore blog","blog.meshcore.io","https://blog.meshcore.io/","Official project blog."),
  ("LoRa Mesh blog","mesh.oppedahl.com","https://mesh.oppedahl.com/","Personal blog: Summit County, Colorado repeater builds, battery tests and coverage maps."),
  ("MeshCore: A Comprehensive Guide to Off-Grid Mesh Communication","Book · David A. Rodgers Jr.","https://www.booksamillion.com/p/MeshCore/Jr-David-A-Rodgers/9798245445557","Independently published guide."),
]

# Discord totals: count each server once (some groups share one) and leave out mostly-Meshtastic groups
_servers = {}
for g in GROUPS:
    if g['discord_server_name'] and not g.get('mostly_meshtastic'):
        _servers[(g['discord_server_name'], str(g['discord_members']))] = int(g['discord_members'] or 0)
discord_total = sum(_servers.values())
discord_servers = len(_servers)
states_covered = len([s for s in by_state if s in STATES and s != 'DC'])
MAP_URLS = {}
for g in GROUPS:
    if safe(g['live_map_url']): MAP_URLS.setdefault(g['live_map_url'].rstrip('/'), []).append(g)
# Checked by opening each map in a browser on 2026-10-29. 'live' = animated packets/routes, 'node' = node locations, 'coverage' = coverage/drive-test.
MAP_KINDS = {
 'live.bostonme.sh': ('live', 'Asks you to tick "verify you are human" first.'), 'map.mwmesh.com': ('live', 'Asks you to tick "verify you are human" first.'),
 'map.newenglandme.sh': ('live', 'Asks you to tick "verify you are human" first.'), 'livemap.meshtexas.org': ('live', ''), 'meshcore-map.ctmesh.org': ('live', ''),
 'map.pvmesh.org': ('live', ''), 'chicagolandmesh.org/corescope/map': ('live', 'CoreScope: press Live on the map.'), 'map.lvmesh.com': ('live', 'CoreScope: press Live on the map.'),
 'map.nvme.sh/map3': ('live', 'CoreScope: press Live on the map.'), 'map.okimesh.org': ('live', 'CoreScope: press Live on the map.'),
 'www.eastidahomesh.com/live-map.html': ('live', 'CoreScope: press Live on the map.'), 'www.gulfcoastmesh.org/meshmap': ('live', 'Live analyzer embedded on the page.'),
 'nhmesh.live': ('live', 'Live dashboard with messages and map.'), 'map.nocomesh.org/map': ('live', 'Packet viewer (Meshview) with a traffic heat map.'),
 'rdumesh.org/map': ('node', ''), 'nashme.sh/map': ('node', ''), 'map.wcmesh.com': ('node', ''), 'idahomesh.org/map': ('node', ''), 'nodakmesh.org/meshcore/map': ('node', ''),
 'api.phillymesh.net/map': ('node', ''), 'mesh.og.coop/map': ('node', ''), 'map.nwomesh.org': ('node', 'Meshtastic map.'), 'map.bucksmesh.net': ('node', 'Meshtastic monitor.'),
 'wnymeshcore.org/map': ('coverage', ''), 'dcmesh.org/coverage-map': ('coverage', ''), 'ntxmesh.com/coverage-map': ('coverage', ''), 'cnymesh.org/map.html': ('coverage', ''),
 'idahomesh.com/maps': ('coverage', ''), 'cascadiamesh.org/map': ('unknown', 'Blocked our check; open it to see.'), 'map.atlmesh.org': ('unknown', 'Was down on the check date.'),
}
KIND_LABEL = {'live': 'Live traffic', 'node': 'Node map', 'coverage': 'Coverage', 'unknown': 'Map'}
def _mh(u):
    m = re.match(r'^https?://([^/?#]+)(/[^?#]*)?', u or '')
    return (m.group(1) + (m.group(2) or '').rstrip('/')) if m else ''
def map_kind(u):
    h = _mh(u)
    if 'meshmapper.net' in h: return 'coverage'
    return MAP_KINDS.get(h, ('unknown', ''))[0]
def map_note(u): return '' if 'meshmapper.net' in _mh(u) else MAP_KINDS.get(_mh(u), ('', ''))[1]
LIVE_MAP_COUNT = len([u for u in MAP_URLS if map_kind(u) == 'live'])
NAME_NOTE = ('<div class="callout"><strong>A note on the MeshCore name</strong><p>Two camps use the MeshCore name. The core developers run meshcore.io, the docs, the blog and the GitHub repository, '
             'and say "the only \'official\' MeshCore is the github repo." A former team member runs meshcore.co.uk and MeshOS, and has filed trademark applications that the core team is opposing. '
             'This site links to both where useful, but only calls something official if meshcore.io links it. <a href="https://blog.meshcore.io/2026/04/23/the-split" target="_blank" rel="noopener">The core team\'s account</a>.</p></div>')

# ================= PAGES =================
def build_home():
    hero = f'''<div class="hero">
  <div class="flow">
    <p class="label">MeshCore · United States</p>
    <h1>Find the mesh near you.</h1>
    <p class="lede">Every U.S. MeshCore group we could verify, with links to its website, chats and maps where they exist, and radio settings when the group publishes them. Every link checked on {CHECKED_H}.</p>
    <form class="find" action="near-me.html" id="homefind">
      <label for="zip">Your ZIP code</label>
      <div class="row"><input id="zip" name="zip" inputmode="numeric" pattern="[0-9]{{5}}" maxlength="5" placeholder="28117" autocomplete="postal-code"><button class="btn" type="submit">Find groups</button></div>
    </form>
    <div class="readouts"><div><b>{len(GROUPS)}</b><span>groups</span></div><div><b>{states_covered}</b><span>states + DC</span></div><div><b>{num(NODES['us']) if NODES else '–'}</b><span>U.S. nodes on the map</span></div><div><b>{num(discord_total)}</b><span>members in regional Discords</span></div></div>
  </div>
  <figure style="margin:0" class="flow">{us_map(hops=False)}<figcaption class="mapnote">Small dots are the {num(sum(1 for n in NODES['nodes'] if n[2] in (2,3))) if NODES else ''} U.S. repeaters and room servers on the community map; bright ones were heard in the last 30 days. Large dots are local groups, placed on the main city each lists. Tap a state for its groups.</figcaption>{NODE_CREDIT}</figure>
</div>'''
    path = f'''<section class="wrap section"><div class="section-head"><h2>New to MeshCore?</h2><p class="sub">Four steps from curious to on the air.</p></div>
<div class="path">
 <a href="start.html"><span class="n">01</span><h3>Learn what it is</h3><p>Text messaging over radio, with no cell service or internet. How it works and what you need.</p></a>
 <a href="meshcore-vs-meshtastic.html"><span class="n">02</span><h3>Pick MeshCore or Meshtastic</h3><p>The two big LoRa mesh projects, side by side, so you choose once.</p></a>
 <a href="gear.html"><span class="n">03</span><h3>Get a radio</h3><p>Supported devices, U.S. sellers, and what to check before you buy.</p></a>
 <a href="start.html#setup"><span class="n">04</span><h3>Set up and say hello</h3><p>Flash, pair your phone, set your area's radio settings, join the local channel.</p></a>
</div></section>'''
    states = f'''<section class="wrap section"><div class="section-head"><h2>Pick your state</h2><p class="sub">Verified groups per state. <a href="states.html">List view</a></p></div>{tiles()}</section>'''
    official = f'''<section class="wrap section"><div class="section-head"><h2>Core team channels</h2><p class="sub">Linked from meshcore.io, the MeshCore developers' site.</p></div><div class="links">{"".join(lk(n,h,u,a,b) for n,h,u,a,b in OFFICIAL)}</div></section>'''
    more = f'''<section class="wrap section"><div class="section-head"><h2>Everything else, in one place</h2></div><div class="links">
 {lk_int("directory.html","All groups",f"All {len(GROUPS)} groups. Filter by state, Discord, Facebook or live map.")}
 {lk_int("live-maps.html","Live maps",f"{LIVE_MAP_COUNT} live traffic maps, plus node and coverage maps, labeled so you know which is which.")}
 {lk_int("chats.html","Discord & Facebook",f"{discord_servers} regional Discords and every verified Facebook group.")}
 {lk_int("repeaters.html","Build a repeater","Flashing, setup commands, placement and solar.")}
 {lk_int("software.html","Software","Apps, the flasher, community firmware, analyzers and libraries.")}
 {lk_int("videos.html","Videos","Setup walkthroughs, repeater builds and comparisons.")}
</div></section>'''
    script = '''<script>
document.getElementById('homefind').addEventListener('submit',function(ev){ev.preventDefault();var z=document.getElementById('zip').value.trim();location.href='near-me.html'+(/^\\d{5}$/.test(z)?'#z-'+z:'');});
</script>'''
    page('index.html', NAME, f'Find MeshCore mesh radio groups near you: {len(GROUPS)} verified U.S. groups with websites, Discords, Facebook groups, live maps and radio settings.', 'home',
         band(hero, 11) + path + states + official + more, script)

def lk_int(href, title, about):
    return f'<a class="lk" href="{href}"><strong>{e(title)}</strong><span>{e(about)}</span></a>'

def build_states():
    for code, name in STATES.items():
        lst = sort_groups(by_state.get(code, []))
        local = [g for g in lst if len(g['state']) == 1]
        regional = [g for g in lst if len(g['state']) > 1]
        settings = sorted({re.split(r'[;(]', g['radio_settings_confirmed'])[0].strip() for g in lst if g['radio_settings_confirmed']})
        maps = [g for g in lst if safe(g['live_map_url'])]
        nb = [n for n in NEIGHBORS.get(code, '').split() if n]
        nearest = ''
        if not lst and code not in ('AK', 'HI'):
            b = USMAP['bounds'].get(code)
            if b:
                cx, cy = (b[0][0]+b[1][0])/2, (b[0][1]+b[1][1])/2
                near = sorted(PINNED, key=lambda g: (g['pin']['x']-cx)**2 + (g['pin']['y']-cy)**2)[:4]
                nearest = f'<h2 style="margin-top:8px">Closest groups we know of</h2><div class="rows">{"".join(group_row(g, True) for g in near)}</div>'
        empty = f'''<div class="empty"><h2>No MeshCore group found in {e(name)} yet</h2><p>We looked for {'an' if name[0] in 'AEIOU' else 'a'} {e(name)} group with its own website, Discord or Facebook group and didn't find one we could verify. That doesn't mean nobody is on the air.</p>
<div class="acts" style="display:flex;flex-wrap:wrap;gap:8px"><a class="chip" href="add.html">Tell us about a group</a><a class="chip" href="https://map.meshcore.io/" target="_blank" rel="noopener">{ICON["map"]}Check the node map</a><a class="chip" href="https://www.facebook.com/groups/meshcore" target="_blank" rel="noopener">{ICON["facebook"]}Ask in MeshCore Official</a></div></div>{nearest}''' if not lst else ''
        ns = node_stats(code)
        node_readout = f'<div><b>{num(ns["repeaters"])}</b><span>repeaters on the map</span></div><div><b>{num(ns["active30"])}</b><span>nodes heard in 30 days</span></div>' if ns else '<div><b>0</b><span>nodes on the map</span></div>'
        maps_live = [g for g in maps if map_kind(g['live_map_url']) == 'live']
        head = pagehead(f'MeshCore in {e(name)}', '', [('index.html', 'Home'), ('states.html', 'States'), (None, name)],
            f'<div class="readouts"><div><b>{len(local)}</b><span>local group{"s" if len(local)!=1 else ""}</span></div><div><b>{len(regional)}</b><span>regional</span></div>{node_readout}<div><b>{len(maps_live)}</b><span>live traffic map{"s" if len(maps_live)!=1 else ""}</span></div></div>')
        live_btn = f'<p style="margin-top:10px"><a class="btn line" href="{e(live_map_link(code))}" target="_blank" rel="noopener">Open the live community map for {e(name)}</a></p>'
        body = band(f'<div style="display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:24px;align-items:center" class="statehead">{head}<figure style="margin:0;padding-block:20px">{state_map(code)}<figcaption class="mapnote">Dots are repeaters and room servers on the community map; bright ones were heard in the last 30 days. Large dots are local groups.</figcaption>{NODE_CREDIT}{live_btn}</figure></div>', hash(code) % 50) + f'''
<div class="wrap section"><div class="cols"><div class="main">
 {empty}
 {f'<div class="section-head"><h2>Local groups</h2></div><div class="rows">{"".join(group_row(g) for g in local)}</div>' if local else ''}
 {f'<div class="section-head"><h2>Regional groups covering {e(name)}</h2></div><div class="rows">{"".join(group_row(g, True) for g in regional)}</div>' if regional else ''}
</div><aside>
 <section class="panel"><h3>Radio settings used here</h3>{"".join(f"<div>{readout(s)}</div>" for s in settings) + "<p class='small sub'>From the groups' own pages. Ask your local group before changing settings; some areas differ.</p>" if settings else "<p class='small sub'>No group here publishes settings we could confirm. Most U.S. groups we checked use the USA/Canada preset. Ask your local group before you set a radio.</p>"}</section>
 {f'<section class="panel"><h3>On the community map</h3><dl class="facts"><dt>Repeaters</dt><dd>{num(ns["repeaters"])}</dd><dt>Room servers</dt><dd>{num(ns["rooms"])}</dd><dt>Companions</dt><dd>{num(ns["companions"])}</dd><dt>Heard in 30 days</dt><dd>{num(ns["active30"])} of {num(ns["total"])}</dd><dt>Most common frequency</dt><dd class="mono">{e(str(ns["freq"][0][0]))} MHz ({num(ns["freq"][0][1])} nodes)</dd></dl><p class="small sub">From map.meshcore.io on {NODE_DATE}. Owners choose whether to publish a node, so real numbers are higher.</p></section>' if ns and ns["freq"] else ''}
 <section class="panel"><h3>Maps</h3>{"".join(f'<a class="chip" href="{e(g["live_map_url"])}" target="_blank" rel="noopener">{ICON["map"]}{e(g["group_name"])} <span class="n">{KIND_LABEL[map_kind(g["live_map_url"])]}</span></a>' for g in maps) or "<p class='small sub'>None listed. An area shows up on live maps when someone runs an observer. <a href='live-maps.html#observer'>How that works</a>.</p>"}</section>
 {f'<section class="panel"><h3>Neighboring states</h3><div style="display:flex;flex-wrap:wrap;gap:8px">{"".join(f"<a class=chip href={state_page(n)}>{e(STATES[n])} <span class=n>{count(n)}</span></a>" for n in nb)}</div></section>' if nb else ''}
 <a class="btn line" href="add.html">Add or fix a listing</a>
</aside></div></div>'''
        desc = f'{len(lst)} MeshCore mesh radio group{"s" if len(lst)!=1 else ""} in {name}' + (f': {", ".join(g["group_name"] for g in local[:4])}' if local else '') + '. Websites, Discords, Facebook groups, live maps and radio settings.'
        page(state_page(code), f'MeshCore groups in {name}', desc, 'find', body)
    # state list page
    rows = ''.join(f'<tr><td><a href="{state_page(c)}">{e(n)}</a></td><td class="num">{count(c)}</td><td class="sub small">{e(", ".join(g["group_name"] for g in sort_groups(by_state.get(c, []))[:4]))}{"…" if count(c)>4 else ""}</td></tr>' for c, n in sorted(STATES.items(), key=lambda t: t[1]))
    page('states.html', 'MeshCore by state', 'Every U.S. state and DC with the number of verified MeshCore groups in each.', 'find',
         band(pagehead('MeshCore by state', 'Every state and DC, with the groups we verified in each.', [('index.html','Home'),(None,'States')]), 21) +
         f'<div class="wrap section">{tiles()}<div class="tbox"><table><thead><tr><th>State</th><th class="num">Groups</th><th>Groups</th></tr></thead><tbody>{rows}</tbody></table></div></div>')

def build_groups():
    for g in GROUPS:
        if g.get('pin') and 'x' in g['pin']:
            near = sorted(((miles(g['pin'], o['pin']), o) for o in PINNED if o is not g), key=lambda t: t[0])[:5]
            near_html = ''.join(group_row(o, True, d) for d, o in near if d < 400)
        else:
            near_html = ''.join(group_row(o, True) for o in sort_groups([o for o in by_state.get(g['state'][0], []) if o is not g])[:5])
        st_links = ', '.join(f'<a href="{state_page(s)}">{e(STATES[s])}</a>' for s in g['state'] if s in STATES)
        link_rows = []
        def lr(label, url, icon, extra=''):
            if safe(url): link_rows.append(f'<a class="lk" href="{e(url)}" target="_blank" rel="noopener"><span class="badge">{label}</span><strong>{e(host(url))} {ICON["out"]}</strong>{f"<span>{extra}</span>" if extra else ""}</a>')
        lr('Website', g['website_url'], 'web')
        lr('Discord', g['discord_url'], 'discord', (f"{e(g['discord_server_name'])} · {num(g['discord_members'])} members on {CHECKED_H}") if g['discord_server_name'] else 'Members-only link. Join through the website.' if 'channels' in g['discord_url'] else '')
        lr('Facebook', g['facebook_url'], 'facebook', f"{e(g['facebook_name'])} · {e(g['facebook_size'])}" if g['facebook_name'] else '')
        lr(other_label(g['other_chat_url']), g['other_chat_url'], 'chat')
        lr(KIND_LABEL[map_kind(g['live_map_url'])] if safe(g['live_map_url']) else 'Map', g['live_map_url'], 'map', map_note(g['live_map_url']) if safe(g['live_map_url']) else '')
        main_state = g['state'][0]
        crumbs = [('index.html', 'Home'), (state_page(main_state), STATES.get(main_state, main_state)), (None, g['group_name'])]
        head = pagehead(e(g['group_name']), e(g['area_covered']) + f' · {st_links}', crumbs, f'<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center">{sig(g["confidence"])}{"<span class=tag>Also Meshtastic</span>" if g["runs_meshtastic_too"]=="yes" else ""}<span class="small sub">Checked {fmt_date(g["last_checked"])}</span></div>')
        mp = state_map(main_state) if main_state in USMAP['states'] else ''
        body = band(head, len(g['slug'])) + f'''<div class="wrap section"><div class="cols"><div class="main">
 <div class="section-head"><h2>Where to find them</h2></div>
 <div class="links">{"".join(link_rows) or "<p>No working links on the check date.</p>"}</div>
 {f'<div class="callout"><strong>Note</strong><p>{e(g["notes"])}</p></div>' if g['notes'] else ''}
 {f'<div class="section-head"><h2>Radio settings</h2></div><div>{readout(g["radio_settings_confirmed"])}</div><p class="small sub">As published on the group\'s own pages.</p>' if g['radio_settings_confirmed'] else ''}
 {f'<div class="section-head"><h2>Nearby groups</h2></div><div class="rows">{near_html}</div>' if near_html else ''}
</div><aside>
 {f'<figure style="margin:0" class="panel"><h3>Location</h3>{mp}<figcaption class="small sub">{"Pin marks " + e(g["pin"]["city"]) + ", the main city the group lists. Not an exact location." if g.get("pin") else "Statewide or regional group, so no single pin."}</figcaption></figure>' if mp else ''}
 <section class="panel"><h3>How we verified this</h3><dl class="facts"><dt>Status</dt><dd>{SIG_LABEL[g["confidence"]]}</dd><dt>Evidence</dt><dd>{e(g["meshcore_confirmed_by"])}</dd><dt>Checked</dt><dd>{fmt_date(g["last_checked"])}</dd></dl></section>
 <section class="panel"><h3>Run this group?</h3><p class="small">Claim the listing to update links, settings and your description.</p><a class="btn line" href="add.html#claim">Claim or fix this listing</a></section>
</aside></div></div>'''
        desc = f'{g["group_name"]}: MeshCore mesh radio group for {g["area_covered"]}. Website, Discord, Facebook, live map and radio settings, checked {CHECKED_H}.'
        page(g['page'], f'{g["group_name"]} ({", ".join(g["state"])})', desc, 'find', body)

def build_directory():
    opts = ''.join(f'<option value="{c}">{e(n)} ({count(c)})</option>' for c, n in sorted(STATES.items(), key=lambda t: t[1]))
    rows = ''.join(group_row(g, True) for g in sorted(GROUPS, key=lambda g: (g['state'][0], g['group_name'].lower())))
    body = band(pagehead('All groups', f'All {len(GROUPS)} verified U.S. MeshCore groups. Filter to find a Discord to join, a Facebook group or a live map.', [('index.html','Home'),(None,'All groups')]), 5) + f'''
<div class="wrap section">
<form class="filters" id="df" onsubmit="return false">
 <div class="field" style="flex:2 1 240px"><label for="dq">Search</label><input id="dq" type="search" placeholder="Name, city or area"></div>
 <div class="field" style="flex:1 1 200px"><label for="ds">State</label><select id="ds"><option value="">All states</option>{opts}</select></div>
 <div class="field" style="flex:1 1 170px"><label for="dc">Verification</label><select id="dc"><option value="">Any</option><option value="High">Verified</option><option value="Medium">Partly verified</option><option value="Low">Site down</option></select></div>
 <label class="check"><input type="checkbox" id="fd">Has Discord</label><label class="check"><input type="checkbox" id="ff">Has Facebook</label><label class="check"><input type="checkbox" id="fm">Has live map</label><label class="check"><input type="checkbox" id="fr">Publishes radio settings</label>
</form>
<p class="small sub" id="dn" aria-live="polite">{len(GROUPS)} of {len(GROUPS)} groups</p>
<div class="rows" id="dl">{rows}</div>
<p class="empty" id="d0" hidden>No groups match these filters. Clear a filter or two.</p>
</div>'''
    script = '''<script>
(function(){var $=function(i){return document.getElementById(i)},rows=[].slice.call(document.querySelectorAll('#dl .grow'));
function run(){var t=$('dq').value.trim().toLowerCase(),s=$('ds').value,c=$('dc').value,n=0;
rows.forEach(function(r){var d=r.dataset,ok=(!t||d.t.indexOf(t)>-1)&&(!s||(' '+d.st+' ').indexOf(' '+s+' ')>-1)&&(!c||d.c===c)&&(!$('fd').checked||d.d==='1')&&(!$('ff').checked||d.f==='1')&&(!$('fm').checked||d.m==='1')&&(!$('fr').checked||d.r==='1');r.hidden=!ok;if(ok)n++;});
$('dn').textContent=n+' of '+rows.length+' groups';$('d0').hidden=n>0;}
['dq','ds','dc','fd','ff','fm','fr'].forEach(function(i){$(i).addEventListener(i==='dq'?'input':'change',run);});
var h=location.hash.match(/^#q-(.+)$/);if(h){$('dq').value=decodeURIComponent(h[1]).replace(/-/g,' ');}
var st=location.hash.match(/^#st-([a-z]{2})$/i);if(st){$('ds').value=st[1].toUpperCase();}
run();})();
</script>'''
    page('directory.html', 'All MeshCore groups', f'Searchable list of all {len(GROUPS)} verified U.S. MeshCore groups with links to their websites, Discords, Facebook groups and live maps.', 'find', body, script)

def build_near():
    data = [{'n': g['group_name'], 'p': g['page'], 'a': g['area_covered'], 'c': g['confidence'], 'la': g['pin']['lat'], 'lo': g['pin']['lon'], 'st': g['state']} for g in PINNED]
    statewide = {}
    for g in GROUPS:
        if not g.get('pin'):
            for s in g['state']: statewide.setdefault(s, []).append({'n': g['group_name'], 'p': g['page']})
    body = band(f'''<div class="hero" style="grid-template-columns:minmax(0,5fr) minmax(0,7fr)">
<div class="flow">{pagehead("Find a group near you", "Enter a ZIP code to see the closest MeshCore groups, sorted by distance.", [("index.html","Home"),(None,"Find a group")])}
<form class="find" id="nf"><label for="nz">ZIP code</label><div class="row"><input id="nz" inputmode="numeric" maxlength="5" pattern="[0-9]{{5}}" placeholder="28117" autocomplete="postal-code"><button class="btn" type="submit">Search</button></div><p class="small sub" id="nmsg" aria-live="polite"></p></form>
<p class="small sub">Or <a href="states.html">browse by state</a>. Distances are straight-line miles to the main city each group lists. Radio range depends on terrain and repeaters, so a group 60 miles away can still be your best bet.</p></div>
<figure style="margin:0">{us_map(hops=False)}</figure></div>''', 17) + '''
<div class="wrap section"><div id="nres"></div></div>'''
    script = f'''<script>window.NEAR={json.dumps(data, separators=(",",":"))};window.STATEWIDE={json.dumps(statewide, separators=(",",":"))};window.STATENAMES={json.dumps(STATES)};</script>
<script src="assets/zips.js" defer></script>
<script>
(function(){{
var $=function(i){{return document.getElementById(i)}};
function esc(s){{return String(s).replace(/[&<>"']/g,function(c){{return {{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c]}})}}
function mi(a,b,c,d){{var R=3958.8,r=Math.PI/180,x=Math.sin((c-a)*r/2),y=Math.sin((d-b)*r/2);return 2*R*Math.asin(Math.sqrt(x*x+Math.cos(a*r)*Math.cos(c*r)*y*y));}}
var idx=null;function lookup(z){{if(!window.ZIPS)return null;if(!idx){{idx={{}};window.ZIPS.split(';').forEach(function(t){{var p=t.split(',');idx[p[0]]=[+p[1],+p[2]];}});}}return idx[z]||null;}}
var lbl={{High:'Verified',Medium:'Partly verified',Low:'Site down'}};
function run(z){{
 var ll=lookup(z);if(!ll){{$('nmsg').textContent=window.ZIPS?'We don\\'t have a location for ZIP '+z+'. Check the number, or browse by state.':'Loading ZIP data, try again in a second.';return;}}
 $('nmsg').textContent='';var res=window.NEAR.map(function(g){{return [mi(ll[0],ll[1],g.la,g.lo),g];}}).sort(function(a,b){{return a[0]-b[0]}});
 var near=res.filter(function(r){{return r[0]<=150}});if(near.length<5)near=res.slice(0,5);else near=near.slice(0,12);
 var closeSt={{}};res.slice(0,3).forEach(function(r){{r[1].st.forEach(function(s){{closeSt[s]=1}})}});
 var sw=[];Object.keys(closeSt).forEach(function(s){{(window.STATEWIDE[s]||[]).forEach(function(g){{if(!sw.some(function(x){{return x.p===g.p}}))sw.push(g)}})}});
 var h='<div class="section-head"><h2>Closest to '+esc(z)+'</h2><p class="sub">'+near.length+' groups</p></div><div class="rows">'+near.map(function(r){{var g=r[1];return '<div class="grow"><div class="who"><h3><a href="'+g.p+'">'+esc(g.n)+'</a></h3><p class="where">'+esc(g.a)+' · '+g.st.join(', ')+'</p></div><div class="side"><span class="mono" style="font-size:20px">'+Math.round(r[0]).toLocaleString('en-US')+' mi</span><span class="sig '+g.c+'">'+lbl[g.c]+'</span></div></div>'}}).join('')+'</div>';
 if(sw.length)h+='<div class="section-head" style="margin-top:28px"><h2>Statewide and regional groups</h2><p class="sub">These cover whole states, so they have no single location.</p></div><div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:14px">'+sw.map(function(g){{return '<a class="chip" href="'+g.p+'">'+esc(g.n)+'</a>'}}).join('')+'</div>';
 $('nres').innerHTML=h;
}}
function go(z){{if(!/^\\d{{5}}$/.test(z)){{$('nmsg').textContent='Enter a 5-digit ZIP code.';return;}}if(window.ZIPS)run(z);else{{$('nmsg').textContent='Loading ZIP data…';var t=setInterval(function(){{if(window.ZIPS){{clearInterval(t);run(z);}}}},150);}}}}
$('nf').addEventListener('submit',function(ev){{ev.preventDefault();var z=$('nz').value.trim();try{{history.replaceState(null,'','#z-'+z)}}catch(e){{}}go(z);}});
var m=location.hash.match(/^#z-(\\d{{5}})$/);if(m){{$('nz').value=m[1];go(m[1]);}}
}})();
</script>'''
    page('near-me.html', 'Find a MeshCore group near you', 'Enter your ZIP code to find the closest MeshCore mesh radio groups in the U.S., sorted by distance.', 'find', body, script)

def build_maps():
    order = {'live': 0, 'node': 1, 'coverage': 2, 'unknown': 3}
    wm = sorted(MAP_URLS.items(), key=lambda kv: (order[map_kind(kv[0])], kv[1][0]['state'][0], kv[1][0]['group_name'].lower()))
    def st_links(gs): return " ".join(f"<a href={state_page(s)}>{s}</a>" for s in sorted({s for g in gs for s in g["state"]}) if s in STATES)
    def map_row(u, gs):
        names = ", ".join(f'<a href="{g["page"]}">{e(g["group_name"])}</a>' for g in gs)
        return f'<tr><td class="mono">{st_links(gs)}</td><td>{names}</td><td><span class="tag">{KIND_LABEL[map_kind(u)]}</span>{(" <span class=small>" + e(map_note(u)) + "</span>") if map_note(u) else ""}</td><td><a href="{e(gs[0]["live_map_url"])}" target="_blank" rel="noopener" class="mono small">{e(host(gs[0]["live_map_url"]))}</a></td></tr>'
    rows = ''.join(map_row(u, gs) for u, gs in wm)
    body = band(pagehead('Live maps', "Three kinds of map, and they're not the same. Live traffic maps animate messages moving across the mesh, as heard by that group's observer radios. Node maps show where repeaters are. Coverage maps show where signals have been measured. We opened every one and labeled it.", [('index.html','Home'),(None,'Live maps')]), 9) + f'''
<div class="wrap section"><div class="section-head"><h2>National and worldwide</h2></div><div class="links">{"".join(lk(*m) for m in NATIONAL_MAPS)}</div></div>
<div class="wrap section"><div class="section-head"><h2>Regional maps</h2><p class="sub">{LIVE_MAP_COUNT} live traffic, {len([u for u in MAP_URLS if map_kind(u)=='node'])} node maps, {len([u for u in MAP_URLS if map_kind(u)=='coverage'])} coverage. Each opened in a browser on Oct 29, 2026. They run on volunteers' servers and can go down.</p></div>
<div class="callout"><strong>Want the moving dots?</strong><p>The maps labeled <span class="tag">Live traffic</span> are the ones that animate messages. Some ask you to tick a "verify you are human" box first, and CoreScope maps have a Live button to press.</p></div>
<div class="tbox"><table><thead><tr><th>State</th><th>Group</th><th>What it shows</th><th>Map</th></tr></thead><tbody>{rows}</tbody></table></div></div>
<div class="wrap section" id="observer"><div class="section-head"><h2>Put your area on the map</h2></div>
<div class="cols"><div class="main prose"><p>An <strong>observer</strong> is a MeshCore radio connected to a computer that uploads every packet it hears. Regional maps draw their lines from those uploads, so an area with no observer stays dark even if it has repeaters.</p>
<ol class="steps"><li><h3>Ask your local group</h3><p>Find out which MQTT server their map uses. <a href="near-me.html">Find your group</a>.</p></li><li><h3>Set up the uploader</h3><p>Connect a radio to an always-on computer and run <a href="https://github.com/cisien/meshcoretomqtt" target="_blank" rel="noopener">meshcoretomqtt</a>, the common observer script.</p></li><li><h3>No map yet? Run one</h3><p>Use <a href="https://github.com/yellowcooln/meshcore-mqtt-live-map" target="_blank" rel="noopener">meshcore-mqtt-live-map</a> or <a href="https://github.com/Kpa-clawbot/CoreScope" target="_blank" rel="noopener">CoreScope</a>. Then <a href="add.html">tell us</a> so we can list it.</p></li></ol></div></div></div>'''
    page('live-maps.html', 'MeshCore live maps', f'{len(wm)} regional MeshCore traffic and coverage maps plus national node maps, and how to put your area on the map.', 'maps', body)

def build_chats():
    ds = sorted([g for g in GROUPS if g['discord_server_name']], key=lambda g: -int(g['discord_members'] or 0))
    fb = sorted([g for g in GROUPS if g['facebook_url'] and g['facebook_name']], key=lambda g: (g['state'][0], g['group_name']))
    oth = [g for g in GROUPS if safe(g['other_chat_url'])]
    nat = [('MeshCore Official','Facebook','https://www.facebook.com/groups/meshcore','Public group. 33.6K members.'),('MeshCore.io','Discord','https://discord.gg/meshcore','The official Discord server. 14,943 members.'),('r/meshcore','Reddit','https://www.reddit.com/r/meshcore/','The main MeshCore subreddit.'),('LetsMesh Forum','Forum','https://forum.letsmesh.net/','Hardware, firmware and troubleshooting, with regional categories.'),('@meshcore@mastodon.social','Mastodon','https://mastodon.social/@meshcore','Official project account.')]
    body = band(pagehead('Discord, Facebook and more', 'Where MeshCore people talk. The official channels first, then every regional Discord and Facebook group we verified.', [('index.html','Home'),(None,'Chats')]), 13) + f'''
<div class="wrap section"><div class="section-head"><h2>National</h2></div><div class="links">{"".join(lk(n, host(u), u, a, p) for n,p,u,a in nat)}</div></div>
<div class="wrap section"><div class="section-head"><h2>Regional Discord servers</h2><p class="sub">{discord_servers} servers · {num(discord_total)} members · counts from Discord on {CHECKED_H}. Many also serve Meshtastic users.</p></div>
<div class="tbox"><table><thead><tr><th>Server</th><th>Group</th><th>State</th><th class="num">Members</th></tr></thead><tbody>{"".join(f'<tr><td><a href="{e(g["discord_url"])}" target="_blank" rel="noopener">{e(g["discord_server_name"])}</a></td><td><a href="{g["page"]}">{e(g["group_name"])}</a></td><td class="mono">{" ".join(g["state"])}</td><td class="num">{num(g["discord_members"])}</td></tr>' for g in ds)}</tbody></table></div>
<p class="small sub">A few groups share a server with a neighbor, so some servers appear twice in the table; the total counts each server once and leaves out Mountain Mesh, which is mostly Meshtastic.</p></div>
<div class="wrap section"><div class="section-head"><h2>Facebook groups and pages</h2><p class="sub">Each opened in a browser on {CHECKED_H}.</p></div>
<div class="tbox"><table><thead><tr><th>Name on Facebook</th><th>Group</th><th>State</th><th class="num">Size</th></tr></thead><tbody>{"".join(f'<tr><td><a href="{e(g["facebook_url"])}" target="_blank" rel="noopener">{e(g["facebook_name"])}</a></td><td><a href="{g["page"]}">{e(g["group_name"])}</a></td><td class="mono">{" ".join(g["state"])}</td><td class="num">{e(g["facebook_size"])}</td></tr>' for g in fb)}</tbody></table></div></div>
{f'<div class="wrap section"><div class="section-head"><h2>Telegram, Reddit and IRC</h2></div><div style="display:flex;flex-wrap:wrap;gap:8px">{"".join(chip(g["other_chat_url"], "chat", e(g["group_name"]), other_label(g["other_chat_url"])) for g in oth)}</div></div>' if oth else ''}'''
    page('chats.html', 'MeshCore Discord and Facebook groups', f'{discord_servers} regional MeshCore Discord servers and every verified Facebook group in the U.S., plus the official channels.', 'chats', body)

def build_software():
    body = band(pagehead('Software', 'Official apps and tools first, then community projects. Community projects are run by volunteers and are not supported by the MeshCore project.', [('index.html','Home'),('learn.html','Learn'),(None,'Software')]), 23)
    for t, b, items in TOOLS:
        body += f'<div class="wrap section"><div class="section-head"><h2>{e(t)}</h2><p class="sub">{e(b)}</p></div><div class="links">{"".join(lk(*i) for i in items)}</div></div>'
    body += f'<div class="wrap"><p class="small sub" style="margin-top:20px">Each project checked on {CHECKED_H}: the page exists and the project is not archived.</p></div>'
    page('software.html', 'MeshCore software and tools', 'Official MeshCore apps, the web flasher, community firmware, live map software, analyzers, Home Assistant integration and developer libraries.', 'learn', body)

def build_learn():
    body = band(pagehead('Learn MeshCore', 'Guides on this site, then the best docs, wikis and catalogs elsewhere.', [('index.html','Home'),(None,'Learn')]), 27) + f'''
<div class="wrap section"><div class="section-head"><h2>Guides on this site</h2></div><div class="links">
{lk_int("start.html","What is MeshCore, and how to start","What it does, what you need, and a step-by-step setup.")}
{lk_int("meshcore-vs-meshtastic.html","MeshCore vs Meshtastic","The two LoRa mesh projects side by side.")}
{lk_int("repeaters.html","Build a repeater","Flashing, setup commands, placement and solar.")}
{lk_int("glossary.html","Glossary","Companion, repeater, room server, SF, BW, CR and more, in plain English.")}
{lk_int("software.html","Software","Apps, firmware, maps, analyzers and libraries.")}
{lk_int("videos.html","Videos","Walkthroughs and builds worth watching.")}
</div></div>
<div class="wrap section">{NAME_NOTE}</div>
{('<div class="wrap section"><div class="section-head"><h2>Start with a video</h2><p class="sub"><a href="videos.html">All ' + str(len([x for x in (VIDEOS or {}).get('videos', []) if safe(x.get('url'))])) + ' videos</a></p></div><div class="vgrid">' + ''.join(video_card(x) for x in [x for x in (VIDEOS or {}).get('videos', []) if x.get('category') in ('intro','setup') and safe(x.get('url'))][:3]) + '</div></div>') if VIDEOS else ''}
<div class="wrap section"><div class="section-head"><h2>Docs and wikis</h2></div><div class="links">{"".join(lk(*i) for i in LEARN_DOCS)}</div></div>
<div class="wrap section"><div class="section-head"><h2>Community catalogs</h2><p class="sub">Other lists of MeshCore resources. We used these as starting points, then verified each group ourselves.</p></div><div class="links">{"".join(lk(*i) for i in LEARN_LISTS)}</div></div>
<div class="wrap section"><div class="section-head"><h2>Blogs and books</h2></div><div class="links">{"".join(lk(*i) for i in LEARN_READ)}</div></div>'''
    lscript = '''<script>
document.addEventListener('click',function(ev){var a=ev.target.closest('.vthumb');if(!a)return;var f=a.closest('.vframe');if(!f||!f.dataset.yt)return;ev.preventDefault();
var i=document.createElement('iframe');i.src='https://www.youtube-nocookie.com/embed/'+f.dataset.yt+'?autoplay=1&rel=0';i.title=a.getAttribute('aria-label').replace(/^Play: /,'');i.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';i.allowFullscreen=true;i.referrerPolicy='strict-origin-when-cross-origin';f.replaceChildren(i);});
</script>'''
    page('learn.html', 'Learn MeshCore', 'Beginner guides, MeshCore vs Meshtastic, repeater builds, a glossary, plus the best MeshCore docs, wikis and community catalogs.', 'learn', body, lscript)

PENDING = '<div class="empty"><p>This guide is being written and checked against the official docs. Check back soon.</p></div>'

def build_start():
    G = GUIDES or {}
    w, s = G.get('what_is'), G.get('getting_started')
    what = f'<div class="prose">{"".join(f"<p>{e(p)}</p>" for p in w["paragraphs"])}</div>{sources(w.get("sources"))}' if w else PENDING
    setup = ''
    if s:
        setup = (f'<p class="prose">{e(s.get("intro",""))}</p>' if s.get('intro') else '') + '<ol class="steps">' + ''.join(f'<li><h3>{e(st["title"])}</h3><p>{e(st["text"])}</p></li>' for st in s['steps']) + '</ol>' + (f'<div class="callout"><strong>About radio settings</strong><p>{e(s["settings_note"])}</p><p><a href="near-me.html">Find your local group</a> and use what they publish.</p></div>' if s.get('settings_note') else '') + sources(s.get('sources'))
    else: setup = PENDING
    body = band(pagehead('What is MeshCore?', 'Text messaging over radio, with no cell towers or internet. Here is what it is, what you need, and how to send your first message.', [('index.html','Home'),(None,'Get started')]), 31) + f'''
<div class="wrap section"><div class="cols"><div class="main">{what}</div>
<aside><section class="panel"><h3>Already decided?</h3><a class="chip" href="gear.html">Pick a device</a><a class="chip" href="near-me.html">Find your local group</a><a class="chip" href="meshcore-vs-meshtastic.html">Compare with Meshtastic</a></section></aside></div></div>
<div class="wrap section" id="setup"><div class="section-head"><h2>Set up your first radio</h2><p class="sub">Checked against the official docs on {fmt_date((GUIDES or {}).get("checked", CHECKED))}.</p></div>{setup}</div>'''
    page('start.html', 'What is MeshCore? How to get started', 'What MeshCore is, what you need, and a step-by-step guide to flashing a radio, pairing your phone and sending your first message in the U.S.', 'start', body)

def build_vs():
    v = (GUIDES or {}).get('vs_meshtastic')
    if v:
        tbl = '<div class="tbox"><table><thead><tr><th>Topic</th><th>MeshCore</th><th>Meshtastic</th></tr></thead><tbody>' + ''.join(f'<tr><th scope="row" style="text-transform:none;letter-spacing:0;font-family:var(--body);font-size:16px;color:var(--ink)">{e(r["topic"])}</th><td>{e(r["meshcore"])}</td><td>{e(r["meshtastic"])}</td></tr>' for r in v['rows']) + '</tbody></table></div>'
        inner = (f'<p class="prose">{e(v.get("intro",""))}</p>' if v.get('intro') else '') + tbl + f'<div class="prose">{"".join(f"<p>{e(p)}</p>" for p in v.get("paragraphs", []))}</div>' + sources(v.get('sources')) + '<p class="prose small sub">Related: our sister site Prepped Gear compares the two from an emergency-communications angle in <a href="https://preppedgear.com/meshcore-vs-meshtastic/">MeshCore vs Meshtastic: routing, apps, hardware</a>.</p>'
    else: inner = PENDING
    body = band(pagehead('MeshCore vs Meshtastic', 'The two big LoRa mesh projects, compared on what each one documents. Many U.S. groups run both.', [('index.html','Home'),('start.html','Get started'),(None,'MeshCore vs Meshtastic')]), 37) + f'<div class="wrap section">{inner}</div>'
    page('meshcore-vs-meshtastic.html', 'MeshCore vs Meshtastic', 'MeshCore and Meshtastic compared side by side: routing, repeaters, hop limits, apps, hardware and which to choose.', 'start', body)

def terrain_svg():
    return '''<svg viewBox="0 0 640 200" role="img" aria-label="Diagram: a repeater on a hilltop relays between two radios that can't see each other" style="width:100%;height:auto;max-width:680px">
<path d="M0 170 C80 160 120 150 170 155 S260 120 320 60 S400 120 460 150 S580 160 640 168 V200 H0Z" fill="var(--sunk)"/>
<path d="M0 170 C80 160 120 150 170 155 S260 120 320 60 S400 120 460 150 S580 160 640 168" fill="none" stroke="var(--ink)" stroke-width="2"/>
<line x1="320" y1="60" x2="320" y2="22" stroke="var(--ink)" stroke-width="3"/><circle cx="320" cy="20" r="5" fill="var(--signal)"/>
<rect x="40" y="148" width="12" height="18" rx="2" fill="var(--ink)"/><rect x="590" y="146" width="12" height="18" rx="2" fill="var(--ink)"/>
<path d="M52 150 L318 24 M592 148 L322 24" stroke="var(--signal)" stroke-width="2" stroke-dasharray="6 6" fill="none"/>
<path d="M52 156 L590 154" stroke="var(--bad)" stroke-width="1.5" stroke-dasharray="2 6" fill="none" opacity=".8"/>
<text x="330" y="18" font-family="var(--mono)" font-size="13" fill="var(--ink)">repeater</text>
<text x="20" y="190" font-family="var(--mono)" font-size="13" fill="var(--ink)">your radio</text>
<text x="548" y="190" font-family="var(--mono)" font-size="13" fill="var(--ink)">their radio</text>
<text x="250" y="148" font-family="var(--mono)" font-size="12" fill="var(--bad)">blocked by the hill</text>
</svg>'''

def build_repeaters():
    r = (GUIDES or {}).get('repeater_guide')
    if r:
        inner = (f'<p class="prose">{e(r.get("intro",""))}</p>' if r.get('intro') else '')
        for sec in r['sections']:
            inner += f'<div class="section-head" style="margin-top:12px"><h2>{e(sec["heading"])}</h2></div><div class="prose">{"".join(f"<p>{e(p)}</p>" for p in sec.get("paragraphs", []))}</div>'
            if sec.get('commands'):
                inner += '<dl class="gloss">' + ''.join(f'<div><dt><code>{e(c["cmd"])}</code></dt><dd>{e(c["what"])}</dd></div>' for c in sec['commands']) + '</dl>'
        inner += sources(r.get('sources'))
    else: inner = PENDING
    body = band(pagehead('Build a MeshCore repeater', 'Repeaters carry messages between radios that can\'t reach each other. A good one, up high, can connect a whole county.', [('index.html','Home'),('learn.html','Learn'),(None,'Repeaters')]), 41) + f'''
<div class="wrap section"><figure style="margin:0" class="flow">{terrain_svg()}<figcaption class="small sub">Height beats power. A repeater with a clear view of both radios relays what the hill blocks.</figcaption></figure></div>
<div class="wrap section flow">{inner}</div>
<div class="wrap section"><div class="callout"><strong>Before you mount anything</strong><p>Ask your <a href="near-me.html">local group</a> where repeaters are needed and which settings they use. A repeater on the wrong settings can't talk to anyone.</p></div></div>'''
    page('repeaters.html', 'How to build a MeshCore repeater', 'How to set up a MeshCore repeater: flashing, configuration commands, radio settings, placement and solar builds.', 'learn', body)

def build_glossary():
    gl = (GUIDES or {}).get('glossary')
    inner = ('<dl class="gloss">' + ''.join(f'<div id="{slug(t["term"])}"><dt>{e(t["term"])}</dt><dd>{e(t["definition"])}</dd></div>' for t in sorted(gl['terms'], key=lambda t: t['term'].lower())) + '</dl>' + sources(gl.get('sources'))) if gl else PENDING
    body = band(pagehead('MeshCore glossary', 'The words you will run into, in plain English.', [('index.html','Home'),('learn.html','Learn'),(None,'Glossary')]), 43) + f'<div class="wrap section">{inner}</div>'
    page('glossary.html', 'MeshCore glossary', 'Plain-English definitions of MeshCore terms: companion, repeater, room server, observer, advert, SF, BW, CR, path hash and more.', 'learn', body)

def build_gear():
    hw = HW or {}
    devs = hw.get('devices') or []
    SKU = {'Seeed Wio Tracker L1 Pro': 'https://www.seeedstudio.com/Wio-Tracker-L1-Pro-for-Meshcore-p-6717.html',
           'Seeed SenseCAP Solar Node P1-Pro': 'https://www.seeedstudio.com/SenseCAP-Solar-Node-P1-Pro-for-Meshcore-p-6741.html'}
    ROLE = {'companion': '<a href="glossary.html#companion">Companion</a>', 'repeater': '<a href="glossary.html#repeater">Repeater</a>', 'room_server': '<a href="glossary.html#room-server">Room server</a>', 'sensor': 'Sensor'}
    def ff(d): return re.sub(r';?\s*see notes\)?', ')', d.get('form_factor', '')).replace('()', '').replace(' )', ')')
    sellers = [s for s in (hw.get('sellers') or []) if s.get('mentions_meshcore')]
    fw = hw.get('firmware') or {}
    def yn(v):
        v = str(v or '').lower()
        return 'Yes' if v == 'yes' else 'No' if v == 'no' else 'Optional' if v.startswith('optional') else '<span class="sub">Not stated</span>'
    dev_tbl = ('<div class="tbox"><table><thead><tr><th>Device</th><th>Maker</th><th>Firmware</th><th>Type</th><th>GPS</th><th>Screen</th><th>915 MHz</th></tr></thead><tbody>' + ''.join(
        f'<tr><td><a href="{e(SKU.get(d["name"], d["maker_url"]))}" target="_blank" rel="noopener"><strong>{e(d["name"])}</strong></a></td><td>{e(d["maker"])}</td><td class="small">{", ".join(ROLE.get(r, e(r)) for r in d.get("roles", []))}</td><td class="small sub">{e(ff(d))}</td><td>{yn(d.get("gps"))}</td><td>{yn(d.get("screen"))}</td><td>{yn(d.get("us_915"))}</td></tr>' for d in devs if safe(d.get('maker_url'))) + '</tbody></table></div>') if devs else PENDING
    def clean(t):
        t = re.sub(r'\s*\(\$[^)]*\)', '', t); t = re.sub(r'\s*\$\d[\d,.]*(\s*[-–]\s*\$?\d[\d,.]*)?', '', t)
        t = re.sub(r'\s+([,.;])', r'\1', t).strip(); return t if t.endswith('.') else t + '.'
    sell = ''.join(lk(s['name'], host(s['url']), s['url'], clean(s['sells']) + (' Ships from the U.S.' if str(s.get('ships_from_us')).lower() == 'yes' else ''), 'Ships from U.S.' if str(s.get('ships_from_us')).lower() == 'yes' else 'Seller') for s in sellers if safe(s.get('url')))
    body = band(pagehead('Devices and where to buy', 'Pick a supported radio, buy the version that covers the U.S. 902–928 MHz band, and check with your local group before you mount anything.', [('index.html','Home'),(None,'Gear')]), 47) + f'''
<div class="wrap section"><div class="cols"><div class="main">
 {'<div class="callout"><strong>Want a recommendation?</strong><p><a href="gear-i-use.html">See the gear we use and tested</a>, with notes on how each one did.</p></div>' if HAS_TESTED else ''}
 <div class="section-head"><h2>Supported devices</h2><p class="sub">{"Firmware " + e(fw.get("version")) + " · " + e(fw.get("date","")) if fw.get("version") else ""}</p></div>
 {dev_tbl}
 <p class="small sub">Every device is in the official web flasher with the firmware types shown. Specs come from each maker's product page; "Not stated" means the maker's page didn't say.</p>
 <div class="callout"><strong>"For Meshtastic" on the box is fine</strong><p>Many radios ship with Meshtastic installed and are sold as Meshtastic devices. You can reflash them with MeshCore using the <a href="https://flasher.meshcore.io/" target="_blank" rel="noopener">web flasher</a>. Where meshcore.io links a MeshCore version of a product, we link that one.</p>
 <p>The LILYGO T-Deck usually runs a standalone MeshCore firmware with a screen and keyboard. The FAQ says it is free to use, with an optional paid unlock for some features, and is not open source.</p></div>
</div><aside><section class="panel"><h3>Before you buy</h3><ol class="steps">
 <li><h3>Get the U.S. band</h3><p>Buy a version that covers 902–928 MHz. Makers label it 915 MHz, US915, 900 MHz or 863–928 MHz. Avoid 433 MHz and 868-only versions; there is no U.S. MeshCore preset for them.</p></li>
 <li><h3>Check the flasher</h3><p>Make sure the exact model is on the <a href="https://flasher.meshcore.io/" target="_blank" rel="noopener">official flasher</a>.</p></li>
 <li><h3>Antenna first</h3><p>Don't power on or transmit with the antenna port open. <a href="https://forum.rakwireless.com/t/rak7268-warning-understand-do-not-power-the-device-if-the-lora-antenna-port-has-been-left-open-to-avoid-potential-damage-to-the-rak7268-rak7268c-wisgate-edge-lite-2/7121" target="_blank" rel="noopener">RAKwireless warns</a> this can damage the radio.</p></li>
 <li><h3>Ask locally</h3><p>Your <a href="near-me.html">local group</a> knows what works on their mesh.</p></li></ol></section></aside></div></div>
<div class="wrap section"><div class="section-head"><h2>Where to buy</h2><p class="sub">The makers below are the ones meshcore.io itself points buyers to.</p></div><div class="links">
 {lk("store.meshcore.co.uk","store.meshcore.co.uk","https://store.meshcore.co.uk/","Run by meshcore.co.uk, not the meshcore.io core team. Sells MeshOS licenses and a MeshOS device. Prices in pounds; U.S. shipping not stated.","MeshOS")}
 {lk("Heltec Automation","heltec.org","https://heltec.org/","LoRa boards and node kits. Listed as a place to buy on meshcore.io.","Maker")}
 {lk("LILYGO","lilygo.cc","https://lilygo.cc/","LoRa boards and handhelds like the T-Deck. Listed on meshcore.io.","Maker")}
 {lk("Seeed Studio","seeedstudio.com","https://www.seeedstudio.com/","Trackers and solar nodes. Listed on meshcore.io.","Maker")}
 {lk("RAKwireless","rakwireless.com","https://www.rakwireless.com/","WisBlock boards and WisMesh devices. Listed on meshcore.io.","Maker")}
 {lk("Elecrow","elecrow.com","https://www.elecrow.com/","ThinkNode devices. Listed on meshcore.io.","Maker")}
</div></div>
<div class="wrap section"><div class="section-head"><h2>U.S. sellers</h2><p class="sub">Each site opened on {CHECKED_H} and confirmed to mention MeshCore. We don't vouch for any seller. Make sure any radio you buy is set within U.S. power limits.</p></div><div class="links">{sell}</div>{'' if sell else '<p class="small sub">No U.S. sellers verified yet. <a href="add.html">Add your shop</a>.</p>'}</div>'''
    page('gear.html', 'MeshCore devices and where to buy', 'Which radios run MeshCore, what to check before you buy in the U.S., and where to buy: board makers and U.S. sellers.', 'gear', body)

def video_card(x):
    vid = x.get('video_id') or re.search(r'v=([\w-]+)', x['url']).group(1)
    date = fmt_date(x['published']) if re.match(r'\d{4}-\d\d-\d\d$', x.get('published') or '') else ''
    ch = f'<a href="{e(x["channel_url"])}" target="_blank" rel="noopener">{e(x["channel"])}</a>' if safe(x.get('channel_url')) else e(x['channel'])
    return f'''<article class="vcard"><div class="vframe" data-yt="{e(vid)}"><a class="vthumb" href="{e(x["url"])}" target="_blank" rel="noopener" aria-label="Play: {e(x["title"])}"><img src="https://i.ytimg.com/vi/{e(vid)}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><span class="vplay" aria-hidden="true"><svg width="28" height="28" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></span></a></div>
<div class="vmeta"><strong>{e(x["title"])}</strong><span class="small sub">{ch}{" · " + date if date else ""} · <a href="{e(x["url"])}" target="_blank" rel="noopener">Watch on YouTube</a></span></div></article>'''

def build_videos():
    v = VIDEOS or {}
    cats = [('intro','Start here'),('vs','MeshCore vs Meshtastic'),('setup','First setup'),('repeater','Repeaters'),('solar','Solar and outdoor builds'),('device','Specific devices'),('regions','Regions and settings'),('advanced','Maps, observers and advanced')]
    inner = ''
    for k, t in cats:
        vids = [x for x in v.get('videos', []) if x.get('category') == k and safe(x.get('url'))]
        if not vids: continue
        inner += f'<div class="wrap section"><div class="section-head"><h2>{t}</h2></div><div class="vgrid">' + ''.join(video_card(x) for x in vids) + '</div></div>'
    inner = ('<div class="wrap section"><p class="small sub">We confirmed each video exists and is public; we can\'t vouch for everything said in it. Andy Kirby runs meshcore.co.uk and MeshOS, which are separate from the meshcore.io core team; see <a href="learn.html">the note on the MeshCore name</a>.</p></div>' + inner) if inner else inner
    if v.get('channels'):
        inner += '<div class="wrap section"><div class="section-head"><h2>Channels that cover MeshCore</h2></div><div class="links">' + ''.join(lk(c['name'], host(c['url']), c['url'], c.get('why', ''), 'YouTube') for c in v['channels'] if safe(c.get('url'))) + '</div></div>'
    if not inner: inner = f'<div class="wrap section">{PENDING}</div>'
    body = band(pagehead('MeshCore videos', 'Walkthroughs and builds worth watching, from the creators who make them. Click to play here, or open on YouTube to support the channel.', [('index.html','Home'),('learn.html','Learn'),(None,'Videos')]), 53) + inner
    vscript = '''<script>
document.addEventListener('click',function(ev){var a=ev.target.closest('.vthumb');if(!a)return;var f=a.closest('.vframe');if(!f||!f.dataset.yt)return;ev.preventDefault();
var i=document.createElement('iframe');i.src='https://www.youtube-nocookie.com/embed/'+f.dataset.yt+'?autoplay=1&rel=0';i.title=a.getAttribute('aria-label').replace(/^Play: /,'');i.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';i.allowFullscreen=true;i.referrerPolicy='strict-origin-when-cross-origin';f.replaceChildren(i);});
</script>'''
    page('videos.html', 'MeshCore videos', 'The best MeshCore videos: getting started, MeshCore vs Meshtastic, repeater and solar builds, and specific devices.', 'learn', body, vscript)

def build_about():
    c = lambda k: len([g for g in GROUPS if g['confidence'] == k])
    body = band(pagehead('How we check listings', 'A directory is only useful if the links work. Here is what we check and what each label means.', [('index.html','Home'),(None,'How we check')]), 59) + f'''
<div class="wrap section"><div class="cols"><div class="main">
<div class="section-head"><h2>Verification labels</h2></div>
<dl class="gloss"><div><dt>{sig("High")}</dt><dd>The group's own website mentions MeshCore. Any Discord invite we list works; a few groups use a neighbor's or a radio club's server, and their page says so. <span class="mono">{c("High")} groups.</span></dd></div>
<div><dt>{sig("Medium")}</dt><dd>The group has no website we could use. We confirmed it through its Facebook group, opened in a browser, or a working Discord invite whose server name matches, and most are also listed in a regional directory. <span class="mono">{c("Medium")} groups.</span></dd></div>
<div><dt>{sig("Low")}</dt><dd>The group's website was down on the check date. It's listed so you can find it, but treat it with care. <span class="mono">{c("Low")} groups.</span></dd></div></dl>
<div class="section-head"><h2>What we check on every listing</h2></div>
<ol class="steps"><li><h3>Every link checked</h3><p>Websites and maps are loaded and read. Pages that block automated checks were opened in a browser.</p></li><li><h3>Discord checked with Discord</h3><p>Each invite is looked up with Discord itself: whether it still works, the server's name and its member count.</p></li><li><h3>Facebook opened in a browser</h3><p>We confirm the group's name, size, and that it isn't paused or gone.</p></li><li><h3>Settings only from the source</h3><p>Radio settings are shown only when the group publishes them on its own pages.</p></li></ol>
<div class="section-head"><h2>What we leave out</h2></div><p class="prose">Groups that only run Meshtastic (groups that are mostly Meshtastic but publish MeshCore guidance are listed and marked), personal sites, groups we can't reach through any working link, and dead invites. On the last check we removed {REMOVED} groups for these reasons. We never list private member information or repeater locations people haven't made public.</p>
<div class="section-head" id="disclosures"><h2>Disclosures and privacy</h2></div><p class="prose"><strong>Affiliate links.</strong> Find My Mesh is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate I earn from qualifying purchases. Affiliate links appear only on the gear and review pages, are marked "Paid link", and never influence which groups are listed or how they are ranked. Product photos, titles and prices on those pages come from Amazon's Creators API; prices are shown with the time they were fetched and may have changed by the time you buy.</p><p class="prose"><strong>Privacy.</strong> This site has no accounts, no tracking pixels and no advertising network. The listing form sends what you type to the site owner and nothing else. Amazon may set cookies when you click an affiliate link, under Amazon's own privacy policy. Node counts on the state pages come from a daily snapshot of the public MeshCore community map (map.meshcore.io) and include no personal information.</p>
</div><aside><section class="panel"><h3>Last full check</h3><p class="mono" style="font-size:24px">{CHECKED_H}</p><p class="small sub">Discord invites expire and small groups go quiet, so links are rechecked regularly.</p></section>
<section class="panel"><h3>Independent</h3><p class="small">This directory is not run by or affiliated with the MeshCore project. For official information go to <a href="https://meshcore.io/" target="_blank" rel="noopener">meshcore.io</a>.</p></section>
<section class="panel"><h3>Who runs this</h3><p class="small">Find My Mesh is run by <strong>Roger Johnson</strong> in Mooresville, North Carolina. Roger spent about 17 years in NASCAR as a car chief and crew chief, holds a private pilot certificate, and now owns <a href="https://mooresvillemarketing.com/">Mooresville Marketing</a>, a web and digital marketing agency in Mooresville. He got into MeshCore the way most people do: one radio, then a repeater on the roof, then wondering why the good information was scattered across so many regional sites. This directory is the fix.</p><p class="small">He's putting up repeaters around the Lake Norman area and testing a lot of gear along the way; the <a href="gear.html">gear pages</a> and {'<a href="blog.html">reviews</a>' if HAS_BLOG else 'reviews'} come from that.</p><p class="small">Corrections, additions and takedown requests: use the <a href="add.html">listing form</a>.</p></section></aside></div></div>
<div class="wrap section">{NAME_NOTE}</div>'''
    page('about.html', 'How we verify MeshCore listings', 'How Find My Mesh verifies every MeshCore group listing: links opened, Discord invites checked, Facebook groups confirmed, settings from the source.', 'about', body)

def build_add():
    opts = ''.join(f'<option value="{c}">{e(n)}</option>' for c, n in sorted(STATES.items(), key=lambda t: t[1]))
    body = band(pagehead('Add or fix a listing', 'Groups, Discords, Facebook groups, live maps, shops, tools and videos. We check every submission before it goes live.', [('index.html','Home'),(None,'Add a listing')]), 61) + f'''
<div class="wrap section"><div class="cols"><div class="main">
<form class="form" id="af" name="listing" method="POST" data-netlify="true" netlify-honeypot="company">
 <input type="hidden" name="form-name" value="listing"><p hidden><label>Leave this empty <input name="company"></label></p>
 <div class="field"><label for="a-type">What is this?</label><select id="a-type" name="type"><option>Local or regional group</option><option>Facebook group</option><option>Discord, Telegram or other chat</option><option>Live map</option><option>Shop or builder</option><option>Software or tool</option><option>Video or channel</option><option id="fix">Fix to an existing listing</option><option id="claim">Claim a listing I run</option></select></div>
 <div class="field"><label for="a-name">Name</label><input id="a-name" name="name" required></div>
 <div class="field"><label for="a-url">Main link</label><input id="a-url" name="url" type="url" placeholder="https://" required></div>
 <div class="field"><label for="a-state">State</label><select id="a-state" name="state"><option value="">National / online</option>{opts}</select></div>
 <div class="field"><label for="a-area">City or area covered</label><input id="a-area" name="area" placeholder="e.g. Charlotte metro, Lake Norman"></div>
 <div class="field"><label for="a-more">Other links and details</label><textarea id="a-more" name="details" rows="5" placeholder="Discord invite, Facebook group, live map, radio settings, what's wrong with the current listing"></textarea></div>
 <div class="field"><label for="a-email">Your email (not shown publicly)</label><input id="a-email" name="email" type="email"></div>
 <label class="check"><input type="checkbox" name="owner" id="a-own">I run or represent this</label>
 <p class="small sub">We use your email only to ask about this listing. We don't publish it or share it. Submissions are stored by our form provider.</p>
 <p class="callout" id="a-err" role="alert" hidden></p>
 <button class="btn" type="submit" style="align-self:flex-start">Submit for review</button>
 <div class="callout" id="a-ok" role="status" hidden><strong>Thanks. We got it.</strong><p>We'll open every link and add it within a few days.</p></div>
</form></div>
<aside><section class="panel"><h3>What happens next</h3><ol class="steps"><li><h3>We check it</h3><p>Every link opened, and confirmed it's about MeshCore.</p></li><li><h3>It goes live</h3><p>With a "checked" date.</p></li><li><h3>We keep it current</h3><p>Listings are rechecked and dead links removed.</p></li></ol></section></aside></div></div>'''
    script = '''<script>
(function(){var f=document.getElementById('af');if(location.hash==='#fix')document.getElementById('a-type').value='Fix to an existing listing';if(location.hash==='#claim')document.getElementById('a-type').value='Claim a listing I run';
f.addEventListener('submit',function(ev){ev.preventDefault();var err=document.getElementById('a-err'),n=f.name.value.trim(),u=f.url.value.trim();
if(!n||!/^https?:\\/\\//.test(u)){err.textContent='Add a name and a main link that starts with https://';err.hidden=false;return;}err.hidden=true;
var body=new URLSearchParams(new FormData(f)).toString();
fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body}).then(function(r){if(!r.ok)throw 0;document.getElementById('a-ok').hidden=false;f.reset();}).catch(function(){err.textContent="Your listing didn't send. Check your connection and try again.";err.hidden=false;});});})();
</script>'''
    page('add.html', 'Add or fix a MeshCore listing', 'Add a MeshCore group, Discord, Facebook group, live map, shop or tool to the U.S. directory, or report a broken link.', '', body, script)

def build_tested():
    if not HAS_TESTED: return
    owner = e(TESTED.get('owner', 'the site owner'))
    cats = []
    for it in TESTED['items']:
        if it.get('category') not in cats: cats.append(it.get('category'))
    disclosure = '<p class="callout"><strong>As an Amazon Associate I earn from qualifying purchases.</strong> Links marked "Paid link" pay this site a small commission at no extra cost to you. Only gear ' + owner + ' has used personally is listed, and commissions never affect the group directory.</p>'
    inner = ''
    for c in cats:
        items = [i for i in TESTED['items'] if i.get('category') == c]
        inner += f'<div class="wrap section"><div class="section-head"><h2>{e(c)}</h2></div><div class="rows">'
        for i in items:
            btn = f'<a class="btn" href="{e(i["amazon_url"])}" target="_blank" rel="sponsored noopener">View on Amazon</a> <span class="tag">Paid link</span>' if safe(i.get('amazon_url')) and 'tag=' in i['amazon_url'] else ''
            m = re.search(r'/dp/([A-Z0-9]{10})', i.get('amazon_url', '')); asin = m.group(1) if m else ''
            photo = f'<a class="pphoto" href="{e(i["amazon_url"])}" target="_blank" rel="sponsored noopener" aria-hidden="true" tabindex="-1"><img data-asin="{asin}" alt="{e(i["name"])}" src="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%27200%27 height=%27200%27%3E%3C/svg%3E" width="200" height="200" loading="lazy"></a>' if btn and asin else ''
            price = f'<span class="pprice small" data-asin="{asin}" hidden></span>' if photo else ''
            inner += f'''<div class="grow product">{photo}<div class="who"><h3>{e(i["name"])}</h3><p class="where">Used for: {e(i.get("used_for",""))}</p><p>{e(i.get("verdict",""))}</p>{price}</div>
<div class="side">{f'<span class="small sub">Using since {e(i["tested_since"])}</span>' if i.get("tested_since") else ""}</div><div class="acts" style="align-items:center">{btn}</div></div>'''
        inner += '</div></div>'
    body = band(pagehead('Gear I use', f'Radios, boards, repeaters and antennas {owner} has bought and run, with notes on how each one did.', [('index.html','Home'),('gear.html','Gear'),(None,'Gear I use')], disclosure), 67) + inner + f'<div class="wrap section">{disclosure}</div>'
    page('gear-i-use.html', 'MeshCore gear I use', 'MeshCore radios, boards, repeaters and antennas tested hands-on, with notes on how each performed.', 'gear', body, '<script src="assets/amz-images.js" defer></script>')

AMZ_DISCLOSURE = '<p class="callout"><strong>As an Amazon Associate I earn from qualifying purchases.</strong> Buttons marked "Paid link" pay this site a small commission at no extra cost to you. Only gear I have bought and used is recommended, and commissions never affect the group directory.</p>'
def product_box(pr):
    ok = safe(pr.get('amazon', '')) and 'tag=' in pr.get('amazon', '')
    m = re.search(r'/dp/([A-Z0-9]{10})', pr.get('amazon', ''))
    asin = pr.get('asin') or (m.group(1) if m else '')
    btn = f'<a class="btn" href="{e(pr["amazon"])}" target="_blank" rel="sponsored noopener">View on Amazon</a> <span class="tag">Paid link</span>' if ok else ''
    since = f'<span class="small sub">Owned since {e(pr["owned_since"])}</span>' if pr.get('owned_since') else ''
    photo = f'<a class="pphoto" href="{e(pr["amazon"])}" target="_blank" rel="sponsored noopener" aria-hidden="true" tabindex="-1"><img data-asin="{e(asin)}" alt="{e(pr["name"])}" src="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%27200%27 height=%27200%27%3E%3C/svg%3E" width="200" height="200" loading="lazy"></a>' if ok and asin else ''
    price = f'<span class="pprice small" data-asin="{e(asin)}" hidden></span>' if ok and asin else ''
    return f'<div class="grow product">{photo}<div class="who"><h3>{e(pr["name"])}</h3><p>{e(pr.get("verdict", ""))}</p>{price}</div><div class="side">{since}</div><div class="acts" style="align-items:center">{btn}</div></div>'

def build_blog():
    if not HAS_BLOG: return
    cats = []
    for p in POSTS:
        if p.get('category') and p['category'] not in cats: cats.append(p['category'])
    for p in POSTS:
        body_html = _md.markdown(p['body'], extensions=['tables', 'fenced_code', 'smarty'])
        body_html = re.sub(r'<img alt="([^"]*)" src="(?!https?://)([^"]+)"', lambda m: f'<img alt="{m.group(1)}" src="images/{m.group(2)}" loading="lazy"', body_html)
        ALT = re.compile(r'alt="([^"]*)"')
        body_html = re.sub(r'<p>(<img[^>]+>)</p>', lambda m: f'<figure style="margin:0">{m.group(1)}<figcaption class="small sub">{(ALT.search(m.group(1)) or [None, ""])[1] if False else (ALT.search(m.group(1)).group(1) if ALT.search(m.group(1)) else "")}</figcaption></figure>', body_html)
        prods = p.get('products') or []
        hero = f'<figure style="margin:0"><img src="images/{e(p["hero"])}" alt="{e(p["title"])}" style="width:100%;border-radius:var(--r)"></figure>' if p.get('hero') and os.path.exists(f'{CONTENT}/images/{p["hero"]}') else ''
        related = [q for q in POSTS if q is not p][:3]
        body = band(pagehead(e(p['title']), e(p.get('summary', '')), [('index.html', 'Home'), ('blog.html', 'Blog'), (None, p['title'])], f'<p class="small sub">{e(p.get("category",""))} · {fmt_date(p["date"])}</p>'), sum(map(ord, p['slug'])) % 60) + f'''
<div class="wrap section"><div class="cols"><div class="main">
 {AMZ_DISCLOSURE if prods else ''}
 {hero}
 <div class="prose post">{body_html}</div>
 {f'<div class="section-head"><h2>The gear in this post</h2></div><div class="rows">{"".join(product_box(pr) for pr in prods)}</div>{AMZ_DISCLOSURE}' if prods else ''}
</div><aside>
 <section class="panel"><h3>About these reviews</h3><p class="small">Everything reviewed here was bought and run by the author, usually for months, on a real mesh. Opinions are the author's own. <a href="about.html">How this site works</a>.</p></section>
 {f'<section class="panel"><h3>More posts</h3>{"".join(f"<a class=chip href={q[chr(112)+chr(97)+chr(103)+chr(101)]}>{e(q[chr(116)+chr(105)+chr(116)+chr(108)+chr(101)])}</a>" for q in related)}</section>' if related else ''}
</aside></div></div>'''
        page(p['page'], p['title'], p.get('summary', p['title'])[:155], 'blog', body, '<script src="assets/amz-images.js" defer></script>' if prods else '')
    # index
    def card(p):
        return f'<a class="lk" href="{p["page"]}"><span class="badge">{e(p.get("category",""))} · {fmt_date(p["date"])}</span><strong>{e(p["title"])}</strong><span>{e(p.get("summary",""))}</span></a>'
    inner = ''
    for c in cats:
        inner += f'<div class="wrap section"><div class="section-head"><h2>{e(c)}</h2></div><div class="links">{"".join(card(p) for p in POSTS if p.get("category") == c)}</div></div>'
    body = band(pagehead('Blog', 'Hands-on reviews and comparisons of radios, boards, repeaters and antennas, from someone who has owned a lot of them.', [('index.html', 'Home'), (None, 'Blog')]), 71) + inner
    page('blog.html', 'Blog', 'Hands-on MeshCore gear reviews and comparisons: radios, boards, repeaters and antennas, tested on a real mesh.', 'blog', body)

def build_404():
    page('404.html', 'Page not found', 'Page not found.', '', band(pagehead('Page not found', 'The page moved or never existed. Try finding a group near you.', None, '<p><a class="btn" href="near-me.html">Find a group</a></p>'), 2))

# ---------- write ----------
def write_all():
    if os.path.exists(DIST): shutil.rmtree(DIST)
    os.makedirs(f'{DIST}/assets')
    shutil.copy(f'{ROOT}/src/site.css', f'{DIST}/assets/site.css')
    shutil.copy(f'{ROOT}/src/amz-images.js', f'{DIST}/assets/amz-images.js')
    _brand.write_all(DIST)
    for f in ('favicon.ico', 'assets/icon-32.png', 'assets/icon-180.png', 'assets/icon-192.png', 'assets/icon-512.png', 'assets/og.png'):
        if os.path.exists(f'{ROOT}/brand/{f}'): shutil.copy(f'{ROOT}/brand/{f}', f'{DIST}/{f}')
    shutil.copy(f'{REPO}/geo/zips.js', f'{DIST}/assets/zips.js')
    if os.path.isdir(f'{CONTENT}/images'): shutil.copytree(f'{CONTENT}/images', f'{DIST}/images')
    reset = '<style>[hidden]{display:none!important}</style>'
    for fname, (head, content) in PAGES.items():
        doc = f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n{reset}\n</head>\n<body>\n{content}\n</body>\n</html>\n'
        if SITE_URL:  # clean URLs to match canonicals; Netlify serves /name for name.html
            doc = re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"', lambda m: f'href="/{"" if m.group(1)=="index" else m.group(1)}{m.group(2) or ""}"', doc)
        open(f'{DIST}/{fname}', 'w').write(doc)
    # artifact entry: index content without the document skeleton
    head, content = PAGES['index.html']
    open(f'{ROOT}/artifact-index.html', 'w').write(f'{head}\n{content}\n')
    if SITE_URL:
        urls = ''.join(f'<url><loc>{SITE_URL}/{"" if f=="index.html" else f.replace(".html","")}</loc><lastmod>{CHECKED}</lastmod></url>' for f in PAGES if f != '404.html')
        open(f'{DIST}/sitemap.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
        open(f'{DIST}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
    if NOINDEX:
        open(f'{DIST}/robots.txt', 'w').write('User-agent: *\nDisallow: /\n')
        open(f'{DIST}/_headers', 'w').write('/*\n  X-Robots-Tag: noindex, nofollow\n')
    print('pages', len(PAGES), '| guides', bool(GUIDES), 'hardware', bool(HW), 'videos', bool(VIDEOS))

for b in [build_home, build_states, build_groups, build_directory, build_near, build_maps, build_chats, build_software, build_learn, build_start, build_vs, build_repeaters, build_glossary, build_gear, build_videos, build_about, build_add, build_tested, build_blog, build_404]:
    b()
write_all()
