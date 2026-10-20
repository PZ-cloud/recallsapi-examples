# recallsapi.com examples

Copy-paste examples for [recallsapi.com](https://recallsapi.com): one API and MCP server over US recall records, matched by UPC, model number, NDC, lot code or VIN.

- Recall records from 9 US agencies: CPSC, FDA (food, drug and device enforcement reports), NHTSA, US Coast Guard, FAA, HUD, NIOSH, MSHA and USDA FSIS (history loaded; daily FSIS updates coming soon).
- 132,914 recall records on 2026-10-20 (sum of the per-source counts at https://api.recallsapi.com/v1/health, read 2026-10-20 21:46 UTC; the live number is always at that address, no key needed).
- Every match carries a confidence level (exact, strong, possible), the reasons it matched, and the agency notice link.
- Docs: https://recallsapi.com/docs/ . Pricing: https://recallsapi.com/pricing (Free plan: 100 API calls a day; paid plans from $29 a month add daily catalog alerts). OpenAPI 3.1: https://recallsapi.com/openapi.json

A match is information to review against the agency notice, not a safety, legal or compliance determination. No match is not a safety certification.

## 1. Get a free key

```sh
curl -X POST https://api.recallsapi.com/v1/keys \
  -H "content-type: application/json" \
  -d '{"email": "you@example.com"}'
```

The key is emailed to that inbox; it is never shown in the response. Keep it in an environment variable, never in code:

```sh
export RECALLSAPI_KEY="your key"
```

## 2. curl

```sh
curl -s "https://api.recallsapi.com/v1/check?upc=041548000121" \
  -H "Authorization: Bearer $RECALLSAPI_KEY"
```

`/v1/check` takes any of `upc`, `model`, `ndc`, `lot`, `brand`, `name`. More calls (search, vehicles, one recall, health): [examples/curl/more.sh](examples/curl/more.sh).

## 3. Python (standard library only)

```sh
python3 examples/python/check.py --upc 041548000121
python3 examples/python/check.py --brand "Outshine" --name "fruit bars"
```

Source: [examples/python/check.py](examples/python/check.py)

## 4. JavaScript (Node 18 or newer, no dependencies)

```sh
node examples/javascript/check.mjs upc=041548000121
```

Source: [examples/javascript/check.mjs](examples/javascript/check.mjs)

## 5. MCP server

Endpoint: `https://api.recallsapi.com/mcp` (Streamable HTTP). Tools, all read-only:

| Tool | What it does |
|---|---|
| `check_product` | Is this product recalled? Name and brand, UPC/EAN/GTIN, model, NDC or lot |
| `search_recalls` | Full-text search across the recall records |
| `check_vehicle` | NHTSA recall campaigns by VIN, or by make, model and year |
| `get_recall` | The full record for one recall id |

`initialize` and `tools/list` answer without a key; tool calls need the free key as a bearer header.

Claude Code:

```sh
claude mcp add --transport http recallsapi https://api.recallsapi.com/mcp \
  --header "Authorization: Bearer $RECALLSAPI_KEY"
```

Project `.mcp.json` (Claude Code), [examples/mcp/mcp.json](examples/mcp/mcp.json):

```json
{
  "mcpServers": {
    "recallsapi": {
      "type": "http",
      "url": "https://api.recallsapi.com/mcp",
      "headers": { "Authorization": "Bearer ${RECALLSAPI_KEY}" }
    }
  }
}
```

Cursor: [examples/mcp/cursor.json](examples/mcp/cursor.json). Claude Desktop (through `mcp-remote`): [examples/mcp/claude-desktop.json](examples/mcp/claude-desktop.json).

Also listed in the official MCP registry as `com.recallsapi/recallsapi`. Full MCP docs: https://recallsapi.com/docs/mcp

## 6. AI agents without an account (x402)

Agents can pay per call in USDC on Base with no key: $0.02 per `/v1/check`, $0.01 per `/v1/recalls` and `/v1/vehicles`. A keyless call answers HTTP 402 with the payment terms. Details: https://recallsapi.com/docs/agents

## What is in this repository

Example code and configuration only. The recallsapi.com service itself is not open source and is not in this repository.

## License

The example code is MIT licensed, see [LICENSE](LICENSE). The licence does not cover the recallsapi.com service, its data or its names. Use of the API is governed by https://recallsapi.com/terms .

Operated by PrimeZen LLC (Texas). Questions: hello@recallsapi.com
