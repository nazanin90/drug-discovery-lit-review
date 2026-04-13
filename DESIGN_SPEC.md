# DESIGN_SPEC.md

## Overview
An ADK agent for **drug discovery literature review** that scans millions of biomedical papers via PubMed (and optionally arXiv/Semantic Scholar) to identify potential **drug-target interactions** and **side-effect correlations**. The agent uses the `@cyanheads/pubmed-mcp-server` MCP to search, retrieve, and analyze papers from NCBI's PubMed database.

The agent orchestrates a multi-step pipeline: (1) formulate precise biomedical search queries using MeSH terms, (2) search and retrieve relevant papers, (3) extract drug-target interactions and side-effect data from abstracts, and (4) synthesize findings into a structured report with citations.

## Example Use Cases
1. **"Find papers linking metformin to cancer targets"** - Searches PubMed for metformin + oncology targets, extracts interaction data, returns structured report with PMIDs
2. **"What side effects are correlated with SGLT2 inhibitors?"** - Searches for adverse events associated with the drug class, synthesizes findings across papers
3. **"Identify potential drug repurposing candidates for Alzheimer's from recent literature"** - Broad search for existing drugs showing neuroprotective signals
4. **"Summarize the evidence for interaction between drug X and target Y"** - Focused deep-dive on a specific drug-target pair
5. **"Compare side-effect profiles of JAK inhibitors from clinical trial publications"** - Cross-drug comparison from trial literature

## Tools Required
- **PubMed MCP Server** (`@cyanheads/pubmed-mcp-server`): Search PubMed, retrieve paper metadata/abstracts, access MeSH terms. No auth required (uses NCBI E-utilities public API, optionally with an API key for higher rate limits).
- **Google Search** (built-in `google_search`): For supplementary web searches when PubMed results are insufficient.

## Constraints & Safety Rules
- Never fabricate citations - all PMIDs and paper details must come from actual PubMed results
- Always include PMIDs and DOIs when available for traceability
- Clearly distinguish between established findings and preliminary/speculative correlations
- Disclaim that results are for research purposes only and not medical advice
- Do not recommend specific treatments or clinical decisions
- Limit searches to reasonable scope (max ~100 papers per query iteration)

## Success Criteria
- Agent correctly formulates MeSH-aware PubMed queries from natural language input
- Retrieves relevant papers (precision > 70% for top-20 results)
- Extracts drug names, target proteins, and side effects from abstracts
- Produces structured reports with proper citations (PMIDs)
- Handles ambiguous drug/target names by asking for clarification

## Edge Cases to Handle
1. **Ambiguous drug names** (e.g., "aspirin" vs "acetylsalicylic acid") - use MeSH mappings
2. **No results found** - suggest alternative search terms or broaden query
3. **Too many results** - refine query with date ranges, study types, or MeSH qualifiers
4. **Non-English papers** - filter to English or note language limitations
5. **Retracted papers** - flag retraction status if available
