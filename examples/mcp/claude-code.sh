#!/bin/sh
# Add the recallsapi.com MCP server to Claude Code (remote, Streamable HTTP).
claude mcp add --transport http recallsapi https://api.recallsapi.com/mcp \
  --header "Authorization: Bearer ${RECALLSAPI_KEY:?Set RECALLSAPI_KEY first}"
