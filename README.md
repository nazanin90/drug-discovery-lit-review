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
# Authenticate with GCP
gcloud auth login
gcloud config set project <your-project-id>

# Install dependencies
make install

# (Optional) Add an NCBI API key for higher PubMed rate limits
echo "NCBI_API_KEY=your_key_here" > app/.env

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
├── deployment/
│   ├── mcp-server/            # PubMed MCP server Dockerfile (Cloud Run)
│   └── terraform/             # Infrastructure as code
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

The agent deploys to [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agent-engine/overview). Since Agent Engine doesn't support local MCP servers (stdio), the PubMed MCP server runs separately on Cloud Run.

### Architecture

```
User → Agent Engine (ADK agent) → Cloud Run (PubMed MCP server) → NCBI PubMed API
```

### Step 1: Deploy the PubMed MCP server to Cloud Run

```bash
cd deployment/mcp-server

gcloud run deploy pubmed-mcp-server \
  --source=. \
  --region=us-central1 \
  --port=8080 \
  --set-env-vars="MCP_TRANSPORT_TYPE=http,MCP_HTTP_PORT=8080,MCP_HTTP_HOST=0.0.0.0,MCP_LOG_LEVEL=info"
```

Optionally pass `NCBI_API_KEY` for higher rate limits (10 req/s vs 3 req/s):
```bash
--set-env-vars="...,NCBI_API_KEY=your_key_here"
```

### Step 2: Grant Agent Engine access to the MCP server

```bash
# Get your project number
PROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)")

# Grant the Agent Engine service account access
gcloud run services add-iam-policy-binding pubmed-mcp-server \
  --region=us-central1 \
  --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com" \
  --role=roles/run.invoker
```

### Step 3: Deploy the agent to Agent Engine

```bash
# Use the Cloud Run service URL from Step 1 output
make deploy PUBMED_MCP_URL=https://<your-cloud-run-url>/mcp
```

The agent automatically detects `PUBMED_MCP_URL` and switches from local stdio to remote Streamable HTTP connection. When running locally (`make playground`), it uses stdio instead.

## Disclaimer

This agent is for **research purposes only**. It does not provide medical advice and should not be used for clinical decision-making.

## License

[Apache 2.0](LICENSE)
