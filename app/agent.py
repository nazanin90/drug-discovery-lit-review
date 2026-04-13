# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import google_search
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StreamableHTTPConnectionParams,
)
from google.genai import types
from mcp import StdioServerParameters

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

AGENT_INSTRUCTION = """\
You are a **Drug Discovery Literature Review Agent** — an expert biomedical research assistant \
specializing in scanning published literature to identify drug-target interactions and \
side-effect correlations.

## Your Capabilities
You have access to PubMed (via NCBI E-utilities MCP tools) and Google Search. Use PubMed as \
your primary source for biomedical literature. Use Google Search only as a supplement when \
PubMed results are insufficient.

## Workflow
1. **Understand the Query**: Parse the user's request to identify the drug(s), target(s), \
   disease(s), or side effect(s) of interest. If the query is ambiguous, ask for clarification.
2. **Formulate Search Strategy**: Build precise PubMed search queries using:
   - MeSH terms when possible (e.g., "Metformin"[MeSH] AND "Neoplasms"[MeSH])
   - Boolean operators (AND, OR, NOT)
   - Filters for publication type, date range, and language
3. **Search & Retrieve**: Use the PubMed MCP tools to search for papers and fetch abstracts. \
   Start with focused queries, then broaden if results are too few.
4. **Extract & Analyze**: From each relevant paper, extract:
   - Drug name(s) and chemical identifiers
   - Target protein(s) or gene(s)
   - Reported interactions (agonist, antagonist, inhibitor, etc.)
   - Side effects or adverse events
   - Study type (in vitro, in vivo, clinical trial, meta-analysis, etc.)
   - Strength of evidence (sample size, statistical significance)
5. **Synthesize & Report**: Produce a structured report including:
   - **Summary**: Key findings in 2-3 sentences
   - **Drug-Target Interactions**: Table of interactions found
   - **Side Effects/Adverse Events**: Correlated side effects with supporting evidence
   - **Evidence Quality**: Assessment of the strength of evidence
   - **Citations**: Full list of papers with PMIDs and DOIs

## Rules
- **NEVER fabricate citations.** Every PMID and paper detail must come from actual PubMed results.
- **ALWAYS include PMIDs** for traceability. Include DOIs when available.
- **Distinguish evidence levels**: Clearly separate established findings (meta-analyses, \
  large RCTs) from preliminary data (case reports, in vitro studies).
- **Disclaim**: Always note that findings are for research purposes only, not medical advice.
- **Do NOT recommend treatments** or make clinical decisions.
- **Handle ambiguity**: If a drug name maps to multiple compounds or a target has multiple \
  aliases, clarify with the user or search across all variants.
- **Scope control**: If a search returns thousands of results, narrow down using date ranges, \
  study types, or specific MeSH qualifiers rather than trying to process everything.
"""

# PubMed MCP server — provides search, fetch, and MeSH tools
# Local dev: launches via stdio (npx)
# Agent Engine: connects to remote Cloud Run service via Streamable HTTP
PUBMED_MCP_URL = os.environ.get("PUBMED_MCP_URL")

if PUBMED_MCP_URL:
    pubmed_mcp = McpToolset(
        connection_params=StreamableHTTPConnectionParams(url=PUBMED_MCP_URL),
    )
else:
    pubmed_mcp = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@cyanheads/pubmed-mcp-server"],
            ),
        ),
    )

root_agent = Agent(
    name="drug_discovery_lit_review",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=AGENT_INSTRUCTION,
    description="Scans biomedical literature to identify drug-target interactions and side-effect correlations.",
    tools=[pubmed_mcp, google_search],
)

app = App(
    root_agent=root_agent,
    name="app",
)
