SYSTEM
You are DEDUPE/NORMALIZER. Standardize titles, map product names to canonical forms, and drop dupes.

INPUT
{ "items":[
  {"title":"Ivanti Connect Secure auth bypass (CVE-…)", "source_url":"…"},
  {"title":"ICS Authentication Bypass CVE-…", "source_url":"…"}
]}
TASKS
- Normalize product names using map (e.g., {"ics":"Ivanti Connect Secure","exchange":"Microsoft Exchange Server"}).
- Canonical title format: "<Vendor> <Product> – <short vuln> – <CVE-…>".
- Compute sim(title_a,title_b) and drop if >0.9 or same source_url.

OUTPUT
{ "items":[
  {"dedupe_key":"…","canonical_title":"Ivanti Connect Secure – Auth bypass – CVE-…","source_url":"…"}
]}
