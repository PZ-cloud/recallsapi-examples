// Check a product against US recall records with recallsapi.com.
// Node 18 or newer (built-in fetch), no dependencies. Usage:
//   RECALLSAPI_KEY=... node check.mjs upc=041548000121
//   RECALLSAPI_KEY=... node check.mjs brand=Outshine "name=fruit bars"

const API = "https://api.recallsapi.com";
const FIELDS = new Set(["upc", "model", "ndc", "lot", "brand", "name"]);

/** Turn key=value arguments into a query string, keeping only the fields /v1/check accepts. */
function buildQuery(argv) {
  const params = new URLSearchParams();
  for (const arg of argv) {
    const i = arg.indexOf("=");
    const field = arg.slice(0, i);
    if (i > 0 && FIELDS.has(field)) params.set(field, arg.slice(i + 1));
  }
  if ([...params].length === 0) throw new Error("Pass at least one of upc=, model=, ndc=, lot=, brand=, name=");
  return params.toString();
}

/** Call GET /v1/check and return the JSON body; throws with the API's own error message. */
async function check(query, key) {
  const res = await fetch(`${API}/v1/check?${query}`, {
    headers: { Authorization: `Bearer ${key}`, Accept: "application/json" },
  });
  const text = await res.text();
  let body;
  try { body = JSON.parse(text); } catch { body = null; }
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${body?.error?.message ?? text.slice(0, 300)}`);
  return body;
}

/** Print one line per match with its confidence, reasons and agency source link. */
function printMatches(result) {
  const matches = result.matches ?? [];
  if (matches.length === 0) {
    console.log("No matching recall found. No match is not a safety certification.");
    return;
  }
  for (const m of matches) {
    const r = m.recall;
    console.log(`[${m.confidence}] ${r.agency} ${r.recall_date ?? ""} ${r.title}`);
    console.log(`    why: ${(m.reasons ?? []).join(", ")}`);
    const link = r.url ?? r.source_url;
    if (link) console.log(`    agency notice: ${link}`);
  }
}

const key = process.env.RECALLSAPI_KEY;
if (!key) {
  console.error('Set RECALLSAPI_KEY. Free key: POST https://api.recallsapi.com/v1/keys with {"email": "you@example.com"}');
  process.exit(1);
}
try {
  printMatches(await check(buildQuery(process.argv.slice(2)), key));
} catch (err) {
  console.error(err.message);
  process.exit(1);
}
