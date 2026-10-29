/* Live Amazon product photos.
   Finds product images on the page and works out each one's ASIN from, in order:
   a data-asin attribute, an images/products/<ASIN>.jpg file name, or the Amazon
   /dp/<ASIN> link the image sits inside. Asks our Netlify service (mm-amazon-api,
   Amazon Creators API) for current photos, max 10 ASINs per call, and swaps them in.
   If the service or a photo fails, the image already in the page stays, so nothing
   ever shows broken because of this script. */
(function () {
  var API = '/api/items';
  var RE_ASIN = /^[A-Z0-9]{10}$/;
  function asinFor(img) {
    var a = img.getAttribute('data-asin');
    if (a && RE_ASIN.test(a)) return a;
    var src = img.getAttribute('src') || '';
    if (/(^|\/)(heroes|logo)/i.test(src) || /logo/i.test(img.className || '')) return null;
    var m = src.match(/products\/([A-Z0-9]{10})\.(?:jpe?g|png|webp)/);
    if (m) return m[1];
    var link = img.closest && img.closest('a[href*="/dp/"]');
    if (link) { m = link.getAttribute('href').match(/\/dp\/([A-Z0-9]{10})/); if (m) return m[1]; }
    return null;
  }
  var FALLBACK_CSS = '.amz-fallback{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;width:100%;height:100%;min-height:150px;padding:14px;box-sizing:border-box;text-align:center;font-weight:600;font-size:14px;line-height:1.35;color:inherit}' +
    '.amz-fallback b{display:inline-block;font-size:15px;max-width:22ch}.amz-fallback span{text-decoration:none}' +
    '.amz-fallback>span{display:inline-block;padding:7px 14px;border-radius:999px;background:var(--accent,#c0392b);color:var(--on-accent,#fff);font-size:13px}';
  // Amazon blocks some listings from the API (ItemNotAccessible), so there is no licensed photo to show.
  // Instead of an empty box, show the product name and a "See it on Amazon" pill (the box already links to Amazon).
  function fallback(img) {
    if (img.getAttribute('data-amz-done')) return;
    img.setAttribute('data-amz-done', 'fallback');
    if (!document.getElementById('amz-fallback-css')) {
      var st = document.createElement('style'); st.id = 'amz-fallback-css'; st.textContent = FALLBACK_CSS; document.head.appendChild(st);
    }
    var name = img.getAttribute('alt') || '';
    if (!name) { var card = img.closest('.product-card, .card, .pc'); var t = card && card.querySelector('.pc-title, .card-title, h3, h4'); name = t ? t.textContent.trim() : ''; }
    var box = document.createElement('span'); box.className = 'amz-fallback';
    box.innerHTML = (name ? '<b></b>' : '') + '<span>See it on Amazon</span>';
    if (name) box.firstChild.textContent = name;
    img.style.display = 'none';
    img.parentNode.insertBefore(box, img.nextSibling);
  }
  function swap(img, url) {
    if (url) img.setAttribute('data-amz-done', 'live');
    if (!url || img.getAttribute('src') === url) return;
    var original = img.getAttribute('src'), origSet = img.getAttribute('srcset');
    var pic = img.parentNode && img.parentNode.tagName === 'PICTURE' ? img.parentNode : null;
    var sources = pic ? Array.prototype.slice.call(pic.querySelectorAll('source')) : [];
    img.onerror = function () {
      img.onerror = null;
      img.removeAttribute('data-amz-done'); fallback(img);
      sources.forEach(function (s) { pic.insertBefore(s, img); });
      if (origSet) img.setAttribute('srcset', origSet);
      img.setAttribute('src', original);
    };
    sources.forEach(function (s) { pic.removeChild(s); });
    img.removeAttribute('srcset');
    img.setAttribute('src', url);
  }
  // Amazon throttles bursts (502/429): retry a batch up to 3 times, waiting 1.5s, 3s, 6s.
  function getBatch(list, attempt) {
    return fetch(API + '?asins=' + list.join(','), { mode: 'cors' })
      .then(function (r) { if (r.ok) return r.json(); throw new Error(r.status); })
      .catch(function () {
        if (attempt >= 3) return null;
        return new Promise(function (res) { setTimeout(res, 1500 * Math.pow(2, attempt)); })
          .then(function () { return getBatch(list, attempt + 1); });
      });
  }
  function run() {
    if (!window.fetch) return;
    var imgs = [], asins = [];
    Array.prototype.forEach.call(document.querySelectorAll('img'), function (img) {
      var a = asinFor(img);
      if (!a) return;
      imgs.push([img, a]);
      if (asins.indexOf(a) < 0) asins.push(a);
    });
    if (!asins.length) return;
    asins.sort(); // same ASIN set -> same URL -> served from cache
    var batches = [];
    for (var k = 0; k < asins.length; k += 10) batches.push(asins.slice(k, k + 10));
    (function next(b) {
      if (b >= batches.length) {
        imgs.forEach(function (p) { if (!p[0].getAttribute('data-amz-done')) fallback(p[0]); });
        return;
      }
      getBatch(batches[b], 0)
        .then(function (d) {
          if (!d || !d.items) return;
          imgs.forEach(function (p) {
            var it = d.items[p[1]];
            swap(p[0], it && it.image && it.image.url);
          });
          // price readout, when the page has a slot for it (Amazon wants a timestamp next to any price)
          Array.prototype.forEach.call(document.querySelectorAll('.pprice[data-asin]'), function (el) {
            var it = d.items[el.getAttribute('data-asin')];
            var pr = it && it.offer && it.offer.price && it.offer.price.display;
            if (!pr) return;
            var t = d.fetchedAt ? new Date(d.fetchedAt) : new Date();
            el.textContent = pr + ' on Amazon';
            var s = document.createElement('small'); s.className = 'sub';
            s.textContent = ' as of ' + t.toLocaleDateString() + ' ' + t.toLocaleTimeString([], {hour: 'numeric', minute: '2-digit'}) + '. Product prices and availability are accurate as of the date/time indicated and are subject to change. Any price and availability information displayed on Amazon at the time of purchase will apply to the purchase of this product.';
            el.appendChild(s); el.hidden = false;
          });
        })
        .catch(function () {})
        .then(function () { next(b + 1); });
    })(0);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
