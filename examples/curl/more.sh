#!/bin/sh
# More recallsapi.com calls with curl. Each needs RECALLSAPI_KEY except /v1/health.
set -eu

API="https://api.recallsapi.com"
AUTH="Authorization: Bearer ${RECALLSAPI_KEY:?Set RECALLSAPI_KEY first}"

# Source freshness, no key needed.
curl -sS "$API/v1/health"; echo

# Search recall records by keyword and category (newest first, paged with cursor).
curl -sS --get "$API/v1/recalls" --data-urlencode "q=stroller" --data-urlencode "limit=5" -H "$AUTH"; echo

# Vehicle recall campaigns by make, model and year (or pass vin=).
curl -sS --get "$API/v1/vehicles" --data-urlencode "make=honda" --data-urlencode "model=cr-v" --data-urlencode "year=2017" -H "$AUTH"; echo

# One recall by id.
curl -sS "$API/v1/recalls/fda-H-1268-2026" -H "$AUTH"; echo
