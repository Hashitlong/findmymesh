// Runs on Netlify's scheduler and asks Netlify to rebuild the site.
// The rebuild re-pulls the MeshCore map snapshot and publishes any blog post whose date has arrived.
export default async () => {
  const hook = process.env.BUILD_HOOK_URL;
  if (!hook) return new Response('BUILD_HOOK_URL not set', { status: 500 });
  const r = await fetch(hook, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ trigger_title: 'nightly rebuild' }) });
  return new Response(`build hook ${r.status}`);
};
export const config = { schedule: '17 10 * * *' }; // 10:17 UTC = 6:17 AM Eastern, daily
