# Drug Discovery Literature Review Agent

An AI agent that scans biomedical papers via [PubMed](https://pubmed.ncbi.nlm.nih.gov/) to identify drug-target interactions and side-effect correlations. Given a natural language query, it formulates MeSH-aware PubMed searches, retrieves and analyzes paper abstracts, and produces structured reports with full citations.

Built with [Google ADK](https://google.github.io/adk-docs/) and the [`@cyanheads/pubmed-mcp-server`](https://www.npmjs.com/package/@cyanheads/pubmed-mcp-server) MCP for PubMed access.

## How It Works

1. **Formulates search queries** using MeSH terms and Boolean operators
2. **Searches PubMed** via NCBI E-utilities to retrieve relevant papers
3. **Extracts** drug names, target proteins, interactions, and side effects from abstracts
4. **Synthesizes** findings into a structured report with PMIDs and DOIs

## Requirements

- **Python 3.10+**
- **Node.js 22+** (required by the PubMed MCP server)
- **uv** — Python package manager ([install](https://docs.astral.sh/uv/getting-started/installation/))
- **Google Cloud SDK** — authenticated with a GCP project ([install](https://cloud.google.com/sdk/docs/install))
- **Terraform** — for infrastructure deployment ([install](https://developer.hashicorp.com/terraform/downloads))

## Quick Start

```bash
# Install dependencies
make install

# Launch the interactive playground
make playground
```

The playground opens a web UI at `http://localhost:8501` where you can chat with the agent.

## Example Questions

**Basic literature search**
- "Search PubMed for recent papers on metformin and cancer"
- "Find papers about aspirin and cardiovascular side effects"

**Drug-target interactions**
- "What are known drug-target interactions for imatinib (Gleevec)?"
- "Find papers linking SGLT2 inhibitors to kidney protection targets"
- "What proteins does rapamycin interact with beyond mTOR?"

**Side-effect correlations**
- "What side effects are reported for JAK inhibitors in rheumatoid arthritis trials?"
- "Find correlations between statin use and diabetes risk in recent literature"

**Drug repurposing**
- "Identify potential drug repurposing candidates for Alzheimer's disease from papers published in the last 2 years"
- "Are there papers suggesting metformin has anti-aging effects? Summarize the evidence."

**Multi-drug comparison**
- "Compare side-effect profiles of tofacitinib vs baricitinib"

## Project Structure

```
drug-discovery-lit-review/
├── app/
│   ├── agent.py               # Agent definition and instructions
│   ├── agent_engine_app.py    # Agent Engine deployment wrapper
│   └── app_utils/             # Deployment and telemetry helpers
├── .github/workflows/         # CI/CD pipelines (GitHub Actions)
├── deployment/terraform/      # Infrastructure as code
├── notebooks/                 # Prototyping and evaluation notebooks
├── tests/
│   ├── eval/                  # Evaluation config and datasets
│   ├── integration/           # Integration tests
│   ├── unit/                  # Unit tests
│   └── load_test/             # Load testing
├── DESIGN_SPEC.md             # Agent design specification
├── Makefile
└── pyproject.toml
```

## Commands

| Command              | Description                                      |
|----------------------|--------------------------------------------------|
| `make install`       | Install dependencies                             |
| `make playground`    | Launch interactive web UI                        |
| `make test`          | Run tests                                        |
| `make lint`          | Run code quality checks                          |
| `make eval`          | Run evaluation against evalsets                  |
| `make deploy`        | Deploy agent to Agent Engine                     |
| `make setup-dev-env` | Set up dev environment resources (Terraform)     |

## Deployment

```bash
gcloud config set project <your-project-id>
make deploy
```

To set up production infrastructure with CI/CD, run `uvx agent-starter-pack setup-cicd`.
See the [deployment guide](https://googlecloudplatform.github.io/agent-starter-pack/guide/deployment) for details.

## Disclaimer

This agent is for **research purposes only**. It does not provide medical advice and should not be used for clinical decision-making.

## License

[Apache 2.0](LICENSE)
