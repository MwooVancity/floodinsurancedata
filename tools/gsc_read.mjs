// floodinsurancedata.com Search Console (read only): 28-day totals, top queries/pages, sitemaps, one URL inspection.
// Uses the calcscrape service account (owner access on this property). Run from the calcscrape folder: node ../floodinsurance/tools/gsc_read.mjs
import { getGSCAccessToken } from 'file:///C:/Users/mwoo7/Desktop/calcscrape/tools/lib/gsc-auth.mjs';
const SITE = 'https://floodinsurancedata.com/';
const tok = await getGSCAccessToken();
const H = { Authorization: `Bearer ${tok}`, 'Content-Type': 'application/json' };
const day = d => new Date(Date.now() - d * 864e5).toISOString().slice(0, 10);
const q = async body => (await (await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(SITE)}/searchAnalytics/query`,
  { method: 'POST', headers: H, body: JSON.stringify({ startDate: day(30), endDate: day(2), ...body }) })).json());
const tot = await q({});
console.log('28d totals:', JSON.stringify(tot.rows?.[0] ?? tot).slice(0, 200));
for (const dim of ['query', 'page']) {
  const r = await q({ dimensions: [dim], rowLimit: 10 });
  console.log(`top ${dim}:`); (r.rows || []).forEach(x => console.log(`  ${x.keys[0]} | impr ${x.impressions} clicks ${x.clicks} pos ${x.position.toFixed(1)}`));
}
const byday = await q({ dimensions: ['date'] });
console.log('days with data:', (byday.rows || []).length, 'first:', byday.rows?.[0]?.keys[0], 'last:', byday.rows?.at(-1)?.keys[0]);
const sm = await (await fetch(`https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(SITE)}/sitemaps`, { headers: H })).json();
(sm.sitemap || []).forEach(s => console.log('sitemap', s.path, 'submitted', s.contents?.map(c => c.submitted).join('/'), 'errors', s.errors, 'warnings', s.warnings, 'last read', s.lastDownloaded));
const ins = await (await fetch('https://searchconsole.googleapis.com/v1/urlInspection/index:inspect', { method: 'POST', headers: H,
  body: JSON.stringify({ inspectionUrl: SITE + 'flood-insurance/louisiana/', siteUrl: SITE }) })).json();
const r = ins.inspectionResult || {};
console.log('louisiana index:', r.indexStatusResult?.coverageState, '| last crawl', r.indexStatusResult?.lastCrawlTime);
(r.richResultsResult?.detectedItems || []).forEach(d => console.log('rich:', d.richResultType, JSON.stringify(d.items?.map(i => (i.issues || []).map(x => x.issueMessage))).slice(0, 300)));
