# Public Technical Portfolio Strategy

## Purpose

Much of a user's strongest work may live inside a prior employer and cannot be made public. This strategy defines how to prove enterprise-scale design, build, operate, and communication capabilities through public or synthetic implementations that expose the **patterns, architecture, scale, and decision-making** — not the proprietary content.

## Guiding principle

**Do not recreate confidential systems. Recreate the architectural pattern.**

Every public project must:

1. Map to a real, missing portfolio capability.
2. Use public or fully synthetic data.
3. Include a runnable, deployed artifact with tests and observability.
4. Be explainable in an interview or client conversation.

No portfolio filler.

## Audit of existing public projects

### Example Analytics Studio

- **What it is:** Holding entity and public-facing brand.
- **What it demonstrates:** Product/business ownership, infrastructure decisions, AI-assisted delivery.
- **What it does not demonstrate:** A specific technical system. It is the umbrella, not the artifact.

### Example Analytics OS

- **What it is:** Reusable AI-native development framework.
- **Capabilities covered:** system architecture, technical leadership, agentic workflow patterns, project archetypes, documentation and governance standards.
- **Gaps:** It is a framework, not a deployed runtime. It does not show live data pipelines, ML, APIs, or evaluation at work.

### Example Vehicle Market Intelligence

- **What it is:** Full-stack automotive market analytics product.
- **Capabilities covered:** data ingestion, data engineering, forecasting/ML (price appreciation, ownership-cost forecasting), FastAPI backend, Next.js frontend, deployment, system architecture.
- **Gaps:** No workflow orchestration, limited testing/observability story, no agentic AI, no AI evaluation/governance, no synthetic enterprise-scale data pipeline.

### Example Public Data Dashboard

- **What it is:** Polished Streamlit demo with CDEC data.
- **Capabilities covered:** complete analytics product, public data integration, Streamlit frontend, automated tests and live checks, reliability.
- **Gaps:** Single data source, small scale, no orchestration, no ML/forecasting, no API, no agentic AI, no enterprise platform architecture.

## Portfolio capability matrix

| Capability | Example Vehicle Market Intelligence | Example Public Data Dashboard | Example Analytics OS |
|---|---|---|---|
| Enterprise analytics platform | strong | partial | partial |
| Data engineering / pipelines | strong | partial | partial |
| Forecasting / ML | partial | none | none |
| Agentic AI | none | none | strong |
| AI evaluation / governance | none | none | partial |
| APIs / backend systems | strong | partial | none |
| Frontend / data applications | strong | strong | none |
| Orchestration | partial | partial | partial |
| Testing / reliability | partial | strong | partial |
| Deployment / DevOps | strong | partial | none |
| System architecture | strong | partial | strong |
| Technical / business communication | partial | partial | strong |

### Actual gaps

- **End-to-end forecasting at scale:** No public project shows a multi-step, constraint-based, enterprise forecasting pipeline with scenario planning.
- **Production AI evaluation:** No public project shows how to measure, guardrail, and govern LLM/agent outputs.
- **Data orchestration at scale:** Airflow/DAG-based pipelines, data quality, and observability are not demonstrated publicly.
- **Architecture narrative:** Existing projects have code; the decision-making behind them is not always surfaced in ADRs and architecture write-ups.

## Recommended additional flagship projects

Only two new projects are needed to close the public evidence gaps.

### 1. Synthetic Enterprise Workforce Forecasting & Planning Platform

**Reason for existing:**
Directly recreates the architectural pattern of a real enterprise labor planning system using only synthetic data. It proves the ability to design, build, and operate a forecasting platform at scale.

**Architecture pattern (public/synthetic):**

```
data ingestion → transformation → forecasting → orchestration
    → APIs → scenario planning → UI → testing → observability → deployment
```

**Capabilities covered:**

- Enterprise analytics platform
- Data engineering / pipelines
- Forecasting / ML
- Orchestration
- APIs / backend systems
- Frontend / data applications
- Testing / reliability
- Deployment / DevOps
- System architecture
- Technical / business communication

**Suggested stack:** Python, Airflow, dbt or modular SQL, PostgreSQL/DuckDB, Prophet or custom smoothing, FastAPI, Next.js or Streamlit, Docker, GitHub Actions, Prometheus/logging.

**Public deliverables:**

- GitHub repo with README, architecture doc, and ADRs.
- Live deployed UI with scenario sliders.
- API with OpenAPI docs.
- Synthetic data generator and data-quality checks.
- CI/CD with tests and live health checks.

### 2. AI Evaluation & Governance Harness

**Reason for existing:**
Demonstrates production-grade thinking for agentic AI: how to evaluate LLM outputs, guard against drift, and govern agent behavior before shipping. This is the missing public counterpart to the AI OS work.

**What it does:**

- Prompt and model registry with versioning.
- Benchmark suites and regression tests.
- Evaluation metrics: accuracy, latency, cost, hallucination, safety.
- Guardrails and red-teaming harness.
- Report cards and CI integration.

**Capabilities covered:**

- Agentic AI
- AI evaluation / governance
- Testing / reliability
- System architecture
- Deployment / DevOps
- Technical / business communication

**Suggested stack:** Python, FastAPI, SQLite/PostgreSQL, Pydantic, OpenAI or open-source LLM clients, React or Streamlit, GitHub Actions, Docker.

**Public deliverables:**

- GitHub repo with evaluation framework and example tasks.
- Live dashboard of benchmark results.
- Guardrail templates and red-team examples.
- Architecture and governance write-up.

## Implementation order

1. Finish the **Synthetic Forecasting Platform** first. It addresses the broadest capability gaps and gives the strongest enterprise signal.
2. Build the **AI Evaluation Harness** second. It is narrower but critical for AI platform leadership positioning.
3. For each project, publish:
   - architecture decision records,
   - a technical blog/case-study post,
   - a short video or demo,
   - a sanitized "how this maps to my real work" narrative.

## Converting internal work into sanitized case studies

Use this protocol to move from confidential internal evidence to public case studies without exposing employer information.

### What to remove

- Proprietary source code, SQL, schemas, table names, DAG IDs.
- Internal dashboard/report names and URLs.
- Confidential financial figures, store-level data, customer data.
- Names of internal systems, vendors, or teams unless public.

### What to generalize

- Employer → industry or generic descriptor, e.g., "a large US home-improvement retailer."
- Business units → generic terms like "regions," "departments," or "locations."
- Specific product categories → "product lines" or "SKU families."
- Absolute dollar amounts → percentages, indices, or rounded order-of-magnitude ranges.

### What to keep

- Architecture patterns and system boundaries.
- Decision rationale and trade-offs.
- Scale metaphors (e.g., "~1,750 locations") expressed as approximate or synthetic.
- Business outcomes as relative/percentage impact.
- The shape of the problem, not the underlying data.

### Validation rule

If a sanitized detail would still allow a knowledgeable outsider to reverse-engineer the internal system or data, remove or further abstract it.
