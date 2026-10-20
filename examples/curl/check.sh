#!/bin/sh
# Check a product barcode against US recall records with recallsapi.com.
# Usage: RECALLSAPI_KEY=... ./check.sh 041548000121
set -eu

UPC="${1:-041548000121}"

# Refuse to run without a key; a free key is emailed after POST /v1/keys.
if [ -z "${RECALLSAPI_KEY:-}" ]; then
  echo "Set RECALLSAPI_KEY first. Free key: curl -X POST https://api.recallsapi.com/v1/keys -H 'content-type: application/json' -d '{\"email\": \"you@example.com\"}'" >&2
  exit 1
fi

# Product check by UPC (name, brand, model, ndc and lot work the same way).
curl -sS --get "https://api.recallsapi.com/v1/check" \
  --data-urlencode "upc=${UPC}" \
  -H "Authorization: Bearer ${RECALLSAPI_KEY}"
echo
