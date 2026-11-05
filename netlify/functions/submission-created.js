// Runs automatically on every Netlify Forms submission (event-triggered function).
// Emails the submission to Roger so it can be reviewed. It never adds anything to the site:
// a group only goes on findmymesh.com after Roger approves it and site/groups.json is edited.
// Uses the team-level RESEND_API_KEY (same sender the Mooresville Marketing client sites use).

const TO = process.env.LISTING_NOTIFY_TO || 'roger@mooresvillemarketing.com';
const FROM = 'Find My Mesh <support@mooresvillemarketing.com>';

exports.handler = async (event) => {
  let payload = {};
  try { payload = JSON.parse(event.body || '{}').payload || {}; } catch (e) { /* keep empty */ }
  const fields = payload.ordered_human_fields || [];
  const data = payload.data || {};
  const name = data.name || 'unnamed';
  const state = data.state || '?';

  const lines = [
    'New submission on findmymesh.com (form: ' + (payload.form_name || 'listing') + ').',
    'Nothing has been added to the site. It waits for your OK.',
    '',
    ...fields.map((f) => f.title + ': ' + (f.value === undefined || f.value === null ? '' : String(f.value))),
    '',
    'Submitted: ' + (payload.created_at || new Date().toISOString()),
    'Page: ' + (data.referrer || 'https://findmymesh.com/add'),
    '',
    'All submissions: https://app.netlify.com/projects/findmymesh/forms',
  ];

  if (!process.env.RESEND_API_KEY) {
    console.log('RESEND_API_KEY missing; submission not emailed');
    return { statusCode: 200, body: 'no key' };
  }
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: FROM,
      to: [TO],
      reply_to: data.email || undefined,
      subject: 'Find My Mesh: new group submission - ' + name + ' (' + state + ')',
      text: lines.join('\n'),
    }),
  });
  console.log('resend status', res.status, (await res.text()).slice(0, 200));
  return { statusCode: 200, body: 'ok' };
};
