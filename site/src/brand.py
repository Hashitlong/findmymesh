"""Logo and favicon generation for Find My Mesh.
The mark: a node on a topographic map. Three contour rings (slightly irregular, like a hill)
around a bright node dot, with a short signal tick. Reads at 16px as a target/ping, at full size as a map.
"""
import math, random, os, subprocess

def ring(cx, cy, R, seed, pts=64, wobble=(.07, .035)):
    rnd = random.Random(seed); ph = [rnd.uniform(0, 6.28) for _ in range(2)]
    out = []
    for k in range(pts):
        a = k / pts * 2 * math.pi
        rr = R * (1 + wobble[0] * math.sin(3 * a + ph[0]) + wobble[1] * math.sin(5 * a + ph[1]))
        out.append(f'{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}')
    return 'M' + 'L'.join(out) + 'Z'

def mark_svg(size=64, ink='#1b2420', signal='#b4541a', bg=None, pad=0):
    c = size / 2
    s = size / 64  # scale factor from a 64 design grid
    rings = ''.join(f'<path d="{ring(c, c, r * s, seed)}" fill="none" stroke="{ink}" stroke-width="{w * s:.2f}" stroke-linejoin="round"/>'
                    for r, seed, w in [(27, 3, 2.6), (19.5, 7, 2.6), (12.5, 11, 2.6)])
    dot = f'<circle cx="{c}" cy="{c}" r="{5.2 * s:.2f}" fill="{signal}"/>'
    bgrect = f'<rect width="{size}" height="{size}" rx="{size * .22:.1f}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">{bgrect}{rings}{dot}</svg>'

def wordmark_svg(ink='#1b2420', signal='#b4541a'):
    # mark + text; the text uses the site's display font with a safe fallback
    m = mark_svg(44, ink, signal)
    inner = m.split('>', 1)[1].rsplit('</svg>', 1)[0]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 52" width="300" height="52" role="img" aria-label="Find My Mesh">'
            f'<g transform="translate(0,4)">{inner}</g>'
            f'<text x="56" y="37" font-family="Archivo, Arial Narrow, Arial, sans-serif" font-weight="900" font-size="30" font-stretch="75%" letter-spacing=".3" fill="{ink}">FIND MY <tspan fill="{signal}">MESH</tspan></text></svg>')

def write_all(dist):
    os.makedirs(f'{dist}/assets', exist_ok=True)
    open(f'{dist}/assets/mark.svg', 'w').write(mark_svg(64))
    open(f'{dist}/assets/mark-dark.svg', 'w').write(mark_svg(64, ink='#e6eae4', signal='#f08a4b'))
    open(f'{dist}/assets/logo.svg', 'w').write(wordmark_svg())
    open(f'{dist}/assets/logo-dark.svg', 'w').write(wordmark_svg(ink='#e6eae4', signal='#f08a4b'))
    # favicon: SVG that follows the OS theme, plus PNG/ICO fallbacks on a paper tile
    fav = mark_svg(64).replace('<svg ', '<svg ', 1).replace('</svg>', '<style>@media (prefers-color-scheme:dark){path{stroke:#e6eae4}circle{fill:#f08a4b}}</style></svg>')
    open(f'{dist}/favicon.svg', 'w').write(fav)
    tile = {s: mark_svg(s, bg='#eef1ec', pad=0) for s in (32, 180, 192, 512)}
    for s, svg in tile.items(): open(f'{dist}/assets/icon-{s}.svg', 'w').write(svg)
    open(f'{dist}/site.webmanifest', 'w').write('{"name":"Find My Mesh","short_name":"FindMyMesh","icons":[{"src":"/assets/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/assets/icon-512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#b4541a","background_color":"#eef1ec","display":"browser"}')

if __name__ == '__main__':
    import sys
    write_all(sys.argv[1])
    print('brand assets written')
