# MiroOrca Architecture

## System Overview

MiroOrca uses a three-tier decoupled architecture:

```
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND  (Vue.js 3, port 3000)                            │
│  Step wizard UI — 5 stages — D3.js visualizations           │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP / REST
┌────────────────────────▼────────────────────────────────────┐
│  BACKEND  (Flask, port 5001)                                │
│  3 API blueprints: graph | simulation | report              │
│  Services: OntologyGen → GraphBuilder → ProfileGen          │
│            SimulationRunner → ReportAgent                   │
└──────────┬──────────────────────────────┬───────────────────┘
           │                              │
┌──────────▼──────────┐      ┌────────────▼───────────────────┐
│  NEO4J  (port 7687) │      │  LLM PROVIDER  (your choice)   │
│  Knowledge graph    │      │  OpenAI / Claude / Ollama / etc │
│  Agent memory       │      │  Smart model routing            │
└─────────────────────┘      └────────────────────────────────┘
```

## Backend Domain Architecture

The backend is organized into three Flask blueprints, each owning a stage of the pipeline.

### `/api/graph` — Knowledge Graph Domain

Converts raw uploaded documents into a structured Neo4j knowledge graph.

```
Document (PDF/MD/TXT)
        ↓
OntologyGenerator      ← LLM extracts entities, relationships, themes
        ↓
GraphBuilderService    ← writes nodes and edges to Neo4j
        ↓
Neo4j Knowledge Graph
```

Long-running extraction is handled asynchronously via `TaskManager`. The frontend polls `/api/graph/status/<task_id>` until complete.

### `/api/simulation` — Simulation Domain

Prepares and runs the multi-agent social simulation.

```
Neo4j Knowledge Graph
        ↓
ProfileGenerator       ← LLM generates N agent personas from graph
        ↓
SimulationConfigGen    ← sets platform rules, round count, actions
        ↓
SimulationRunner       ← launches OASIS subprocess
        ↓  IPC (inter-process communication)
OASIS Engine           ← agents interact across Twitter/Reddit platforms
        ↓
Simulation Logs        ← action log, timeline, agent states
```

Supports pause, resume, and restart via subprocess signal handling.

### `/api/report` — Report Domain

Analyzes simulation results and enables post-simulation interaction.

```
Simulation Logs
        ↓
ReportAgent            ← ReACT reasoning loop
  think → query Neo4j → observe → think → ...
        ↓
Prediction Report      ← structured markdown + JSON verdict
        ↓
Agent Chat             ← query any individual agent's perspective
```

## Smart Model Routing

To balance cost and quality, MiroOrca routes LLM calls to two different models:

| Task | Model used | Why |
|---|---|---|
| Simulation rounds (high volume) | `LLM_MODEL_NAME` (default, cheap) | Many calls, speed matters |
| Ontology extraction | `SMART_MODEL_NAME` (stronger) | Foundation of everything downstream |
| Report generation | `SMART_MODEL_NAME` (stronger) | End-user-facing, quality matters |
| Profile generation | `LLM_MODEL_NAME` (default) | Medium volume, moderate reasoning |

If `SMART_MODEL_NAME` is not set, all tasks use `LLM_MODEL_NAME`.

## Data Flow & File Storage

```
uploads/
  <simulation_id>/
    source/                    ← uploaded documents
    ontology.json              ← extracted entity schema
    graph_summary.json         ← Neo4j graph summary
    agents/
      profiles.json            ← all generated personas
    simulation/
      config.json              ← platform rules, round count
      timeline.json            ← round-by-round event log
      actions.jsonl            ← full agent action stream
      top_agents.json          ← most influential agents
    report/
      report.md                ← human-readable report
      verdict.json             ← machine-readable scores
```

## Simulation Engine: OASIS

MiroOrca's simulation is powered by [OASIS](https://github.com/camel-ai/oasis) (Open Agent Social Interaction Simulations) by CAMEL-AI.

OASIS manages:
- Agent state and memory across rounds
- Platform environments (Twitter-like, Reddit-like)
- Action execution (CREATE_POST, REPLY, LIKE, REPOST, etc.)
- Inter-agent influence dynamics

MiroOrca wraps OASIS as a subprocess, communicating via IPC to enable pause/resume control and real-time feed streaming to the frontend.
