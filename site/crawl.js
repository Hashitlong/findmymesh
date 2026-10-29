const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http');
const DIST = 'dist';
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0].split('#')[0]); if (p === '/') p = '/index.html'; if (!/\.[a-z0-9]+$/i.test(p)) p += '.html';
  const f = path.join(DIST, p);
  if (!fs.existsSync(f)) { res.writeHead(404); return res.end('nf'); }
  const ext = path.extname(f); res.writeHead(200, { 'Content-Type': ext === '.css' ? 'text/css' : ext === '.js' ? 'text/javascript' : 'text/html' });
  fs.createReadStream(f).pipe(res);
}).listen(8765);
(async () => {
  const shots = process.argv.slice(2);
  const browser = await chromium.launch();
  const files = fs.readdirSync(DIST).filter(f => f.endsWith('.html'));
  const broken = new Set(), problems = [];
  for (const [w, scheme] of [[1280, 'light'], [390, 'dark']]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, colorScheme: scheme });
    const page = await ctx.newPage();
    let errs = [];
    page.on('pageerror', e => errs.push(e.message));
    page.on('console', m => { if (m.type() === 'error' && !/fonts\.g|ERR_|net::/.test(m.text())) errs.push(m.text()); });
    for (const f of files) {
      errs = [];
      await page.goto('http://localhost:8765/' + f, { waitUntil: 'domcontentloaded' });
      const info = await page.evaluate(() => ({
        ov: document.documentElement.scrollWidth - window.innerWidth,
        links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => !/^(https?:|mailto:|#)/.test(h)),
        h1: document.querySelectorAll('h1').length
      }));
      for (const l of info.links) { let t = l.split('#')[0].replace(/^\//, ''); if (t === '') t = 'index.html'; if (t && !/\.[a-z0-9]+$/i.test(t)) t += '.html'; if (t && !fs.existsSync(path.join(DIST, t))) broken.add(`${f} -> ${l}`); }
      if (info.ov > 1) problems.push(`${w}px ${f}: horizontal overflow ${info.ov}px`);
      if (info.h1 !== 1) problems.push(`${f}: ${info.h1} h1`);
      if (errs.length) problems.push(`${w}px ${f}: ${errs.join(' | ')}`);
      if (shots.includes(f)) await page.screenshot({ path: `shot-${w}-${f.replace('.html', '')}.png`, fullPage: true });
    }
    await ctx.close();
  }
  // interactions
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const p = await ctx.newPage();
  await p.goto('http://localhost:8765/near-me.html#z-28117');
  await p.waitForTimeout(1500);
  console.log('near 28117 ->', (await p.$$eval('#nres .grow h3', a => a.slice(0, 4).map(x => x.textContent))).join(' | '), '/', await p.$$eval('#nres .mono', a => a.slice(0, 4).map(x => x.textContent).join(', ')));
  await p.goto('http://localhost:8765/directory.html');
  await p.selectOption('#ds', 'TX'); await p.check('#fd');
  console.log('directory TX + discord ->', await p.textContent('#dn'));
  await p.goto('http://localhost:8765/index.html');
  await p.fill('#zip', '10001'); await p.click('#homefind button');
  await p.waitForTimeout(1500);
  console.log('home zip -> ', p.url(), '|', (await p.$$eval('#nres .grow h3', a => a.slice(0, 2).map(x => x.textContent))).join(' | '));
  console.log('pages', files.length, '| broken internal links', broken.size, [...broken].slice(0, 10));
  console.log('problems', problems.length, problems.slice(0, 25));
  await browser.close(); server.close();
})();
