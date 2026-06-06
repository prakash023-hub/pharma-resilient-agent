"""
OpenFDA MCP server for registration in TrueFoundry MCP Gateway.

Run locally:
    pip install fastmcp requests
    python mcp_server/openfda_server.py

Then register this server in TrueFoundry and copy the gateway URL into TFY_MCP_OPENFDA_URL.
"""

from __future__ import annotations

import requests
from fastmcp import FastMCP

mcp = FastMCP("openfda-drug-label")


@mcp.tool()
def lookup_drug_label(drug_name: str) -> str:
    """Look up FDA drug label indications for a brand or generic drug name."""
    url = (
        "https://api.fda.gov/drug/label.json"
        f"?search=openfda.brand_name:{drug_name}&limit=1"
    )
    response = requests.get(url, timeout=8)
    if response.status_code != 200:
        return f"No FDA label found for {drug_name}"

    results = response.json().get("results", [])
    if not results:
        return f"No FDA label found for {drug_name}"

    indications = results[0].get("indications_and_usage", ["No indications listed"])
    return str(indications[0])[:800]


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8787)
