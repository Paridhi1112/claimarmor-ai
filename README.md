
# 🛡️ ClaimArmor AI: Intelligent Multi-Agent Claims Advocacy Swarm

**Track:** Agents for Business  
**Submission for:** Kaggle 5-Day AI Agents: Intensive Vibe Coding Capstone Project  
**Video Demo:** https://www.youtube.com/watch?v=w7IDOcQFHCA

ClaimArmor AI is an autonomous, event-driven multi-agent system engineered using the Google Agent Development Kit (ADK) and `agents-cli`. It automates insurance policy auditing via the Model Context Protocol (MCP) and extracts real-time regional parts and labor market intelligence to calculate accurate Diminished Value and generate authoritative insurance demand letters.

---

## 🛑 The Problem

In the modern insurance landscape, everyday consumers face a massive information and technical asymmetry. Adjusters utilize proprietary estimating software to generate repair offers that frequently default to aftermarket components and depressed, non-negotiated local auto body labor rates. 

Average policyholders lack the domain expertise to dissect complex, unstructured insurance policies or the real-time market data required to challenge these evaluations. This results in systemic claim undervaluation and unrecovered **Diminished Value** (the inherent loss in a vehicle's market worth even after perfect structural repairs).

## 💡 The Solution

ClaimArmor AI democratizes claims advocacy by automating the end-to-end claim review process. By abandoning the fragile single-agent paradigm in favor of a specialized multi-agent swarm, the system can reliably:
1. Parse unstructured legal policies locally using MCP.
2. Extract real-time regional labor and parts market intelligence via Agent Skills.
3. Programmatically calculate industry-standard Diminished Value (17c formula).
4. Synthesize inputs into an authoritative, data-backed formal demand letter.

---

## 🏗️ System Architecture

The project implements a hierarchical, parent-child multi-agent framework to isolate task scopes and minimize hallucination vectors.

![ClaimArmor AI Architecture](https://github.com/Paridhi1112/claimarmor-ai/blob/main/ClaimArmor%20Architecture%20Diagram.png)


### Swarm Nodes:
* **The Negotiator (Supervisor Node):** Evaluates overall state, executes mathematical formulas, drafts legal text, and manages Human-in-the-Loop (HITL) governance intercept loops.
* **The Policy Auditor (MCP Specialist):** Securely reads unstructured policy documents (`docs/policy.txt`) via a read-only filesystem attachment and converts parameters into a strict JSON payload.
* **The Parts Scout (Skill Node):** Leverages live web search capabilities (`duckduckgo_search`) to extract localized auto body labor rates and replacement asset valuations.

---

## ⚙️ Key Features Applied (Course Concepts)

* **Multi-Agent Orchestration (ADK):** Uses the ADK's native `sub_agents` routing to establish a strict execution graph.
* **Secure MCP Server:** Integrates `@modelcontextprotocol/server-filesystem` for sandboxed, read-only file access.
* **Dynamic Agent Skills:** Custom Python tooling for live RAG (Retrieval-Augmented Generation) via web search.
* **Human-in-the-Loop (HITL):** Enforces a mandatory intercept gateway (`approve_draft`) preventing final text assembly until explicit human confirmation.
* **Rate-Limit Backoff:** Outfitted with an exponential retry wrapper (`HttpRetryOptions`) to handle concurrent sub-agent API spikes gracefully.

---

## 🚀 Setup & Installation

### Prerequisites
* Python 3.11 or 3.12
* **uv**: Python package manager - [Install Instructions](https://docs.astral.sh/uv/getting-started/installation/)

### 1. Clone the Repository
```bash
git clone [https://github.com/Paridhi1112/claimarmor-ai.git](https://github.com/Paridhi1112/claimarmor-ai.git)
cd claimarmor-ai

## Project Structure

```

claimarmor-agent/
├── app/                     # Core agent code
│   ├── agent.py             # Main agent logic
│   ├── agent_runtime_app.py # Agent Runtime application logic
│   └── app_utils/           # App utilities and helpers
├── tests/                   # Unit, integration, and load tests
├── GEMINI.md                # AI-assisted development guide
└── pyproject.toml           # Project dependencies
```

> 💡 **Tip:** Use [Gemini CLI](https://github.com/google-gemini/gemini-cli) for AI-assisted development - project context is pre-configured in `GEMINI.md`.

## Requirements

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **agents-cli**: Agents CLI - Install with `uv tool install google-agents-cli`
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)


## Quick Start

Install `agents-cli` and its skills if not already installed:

```bash
uvx google-agents-cli setup
```

Install required packages:

```bash
agents-cli install
```

Test the agent with a local web server:

```bash
agents-cli playground
```

You can also use features from the [ADK](https://adk.dev/) CLI with `uv run adk`.

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `agents-cli install` | Install dependencies using uv                                                         |
| `agents-cli playground` | Launch local development environment                                                  |
| `agents-cli lint`    | Run code quality checks                                                               |
| `agents-cli eval`    | Evaluate agent behavior (generate, grade, analyze, and more — see `agents-cli eval --help`) |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests                                                        |
| `agents-cli deploy`  | Deploy agent to Agent Runtime                                                                |
| `agents-cli publish gemini-enterprise` | Register deployed agent to Gemini Enterprise                    |
| [A2A Inspector](https://github.com/a2aproject/a2a-inspector) | Launch A2A Protocol Inspector                                                        |

## 🛠️ Project Management

| Command | What It Does |
|---------|--------------|
| `agents-cli scaffold enhance` | Add CI/CD pipelines and Terraform infrastructure |
| `agents-cli infra cicd` | One-command setup of entire CI/CD pipeline + infrastructure |
| `agents-cli scaffold upgrade` | Auto-upgrade to latest version while preserving customizations |

---

## Development

Edit your agent logic in `app/agent.py` and test with `agents-cli playground` - it auto-reloads on save.

## Deployment

```bash
gcloud config set project <your-project-id>
agents-cli deploy
```

To add CI/CD and Terraform, run `agents-cli scaffold enhance`.
To set up your production infrastructure, run `agents-cli infra cicd`.

## Observability

Built-in telemetry exports to Cloud Trace, BigQuery, and Cloud Logging.

## A2A Inspector

This agent supports the [A2A Protocol](https://a2a-protocol.org/). Use the [A2A Inspector](https://github.com/a2aproject/a2a-inspector) to test interoperability.
See the [A2A Inspector docs](https://github.com/a2aproject/a2a-inspector) for details.
