"""Check a product against US recall records with recallsapi.com.

Standard library only. Usage:
    RECALLSAPI_KEY=... python3 check.py --upc 041548000121
    RECALLSAPI_KEY=... python3 check.py --brand "Outshine" --name "fruit bars"
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.recallsapi.com"
FIELDS = ("upc", "model", "ndc", "lot", "brand", "name")


def build_query(args):
    """Return the query string from the identifiers given on the command line."""
    params = {f: getattr(args, f) for f in FIELDS if getattr(args, f)}
    if not params:
        raise SystemExit("Pass at least one of --upc, --model, --ndc, --lot, --brand, --name")
    return urllib.parse.urlencode(params)


def check(query, key):
    """Call GET /v1/check and return the decoded JSON body, or exit with the API's error message."""
    req = urllib.request.Request(
        f"{API}/v1/check?{query}",
        headers={
            "Authorization": f"Bearer {key}",
            "Accept": "application/json",
            # Name your client; some edge rules refuse the default Python-urllib agent.
            "User-Agent": "recallsapi-examples/1.0 (python)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", "replace")
        try:
            message = json.loads(body)["error"]["message"]
        except (ValueError, KeyError, TypeError):
            message = body[:300]
        raise SystemExit(f"HTTP {err.code}: {message}")
    except urllib.error.URLError as err:
        # python.org builds on macOS need "Install Certificates.command" run once for HTTPS.
        raise SystemExit(f"Could not reach {API}: {err.reason}")


def print_matches(result):
    """Print one line per match: confidence, agency, date, title and the agency source link."""
    matches = result.get("matches", [])
    if not matches:
        print("No matching recall found. No match is not a safety certification.")
        return
    for m in matches:
        r = m["recall"]
        print(f"[{m['confidence']}] {r.get('agency')} {r.get('recall_date', '')} {r.get('title')}")
        print(f"    why: {', '.join(m.get('reasons', []))}")
        link = r.get("url") or r.get("source_url")
        if link:
            print(f"    agency notice: {link}")


def main():
    """Parse arguments, read the key from the environment, run the check."""
    parser = argparse.ArgumentParser(description="US recall check by recallsapi.com")
    for f in FIELDS:
        parser.add_argument(f"--{f}")
    args = parser.parse_args()
    key = os.environ.get("RECALLSAPI_KEY")
    if not key:
        sys.exit("Set RECALLSAPI_KEY. Free key: POST https://api.recallsapi.com/v1/keys with {\"email\": \"you@example.com\"}")
    print_matches(check(build_query(args), key))


if __name__ == "__main__":
    main()
