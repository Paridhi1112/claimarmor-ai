# Changelog

All notable changes to ClaimArmor AI are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- `app/app_utils/__init__.py` — makes `app_utils` a proper Python package with explicit exports
- `.env.example` — environment variable template for onboarding contributors
- `CHANGELOG.md` — this file
- `tests/eval/datasets/claim-scenarios-dataset.json` — domain-specific eval dataset with realistic insurance claim scenarios
- Real unit tests replacing the placeholder in `tests/unit/test_dummy.py`

### Changed
- `docs/policy.txt` — expanded from a 5-line placeholder to a realistic synthetic auto insurance policy document
- `tests/eval/datasets/basic-dataset.json` — updated to domain-relevant scenarios (diminished value, OEM parts, rental coverage)
- `README.md` — fixed broken markdown (unclosed code block), corrected project structure tree, added `.env.example` reference

### Fixed
- Corrected project structure in README (was incorrectly showing `claimarmor-agent/` as the root)
- Closed the unclosed code block in the README Quick Start section

---

## [0.1.0] — 2026-06-21

### Added
- Initial project scaffold via `agents-cli` using the `adk_a2a` template
- Three-agent architecture:
  - **Negotiator** — supervisor orchestrator, 17c DV calculator, demand letter drafter
  - **Policy Auditor** — unstructured policy document parser, outputs structured JSON
  - **Parts Scout** — live web search agent using DuckDuckGo for regional parts/labor pricing
- `search_live_market_data` custom tool (DuckDuckGo-backed RAG)
- Exponential retry wrapper (`HttpRetryOptions`) for concurrent sub-agent API resilience
- Agent Runtime / A2A wrapper (`AgentEngineApp`)
- OpenTelemetry telemetry export to Cloud Trace and Cloud Logging
- Pydantic `Feedback` model for structured feedback logging
- Integration tests for agent streaming
- Architecture diagram (ClaimArmor Architecture Diagram.png)
- Kaggle 5-Day AI Agents Intensive Capstone submission
