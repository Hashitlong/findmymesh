// Runs every morning after the nightly rebuild. If the build published a post today,
// tells Bing (and the other IndexNow engines) about it so it gets crawled promptly.
const SITE = 'https://findmymesh.com';
const KEY = '8237112c02e54a96babd88a83e894507'; // key file is hosted at the site root

export default async () => {
  const r = await fetch(`${SITE}/indexnow-today.json`, { cache: 'no-store' });
  if (!r.ok) return new Response(`indexnow-today.json ${r.status}`, { status: 500 });
  const { generated, urls } = await r.json();
  const today = new Date().toLocaleDateString('en-CA', { timeZone: 'America/New_York' }); // YYYY-MM-DD
  if (generated !== today) return new Response(`list is from ${generated}, not today; nothing sent`);
  if (!urls || !urls.length) return new Response('no new pages today');
  const res = await fetch('https://api.indexnow.org/indexnow', {
    method: 'POST', headers: { 'content-type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ host: 'findmymesh.com', key: KEY, keyLocation: `${SITE}/${KEY}.txt`, urlList: urls }),
  });
  return new Response(`IndexNow ${res.status} for ${urls.length} URLs: ${urls.join(', ')}`);
};
export const config = { schedule: '47 10 * * *' }; // 10:47 UTC, 30 min after the nightly rebuild
