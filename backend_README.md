# MiroOrca Backend

Python 3.11+ / Flask REST API

## Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py       — registers all blueprints
│   │   ├── graph.py          — /api/graph  (document ingestion, graph build)
│   │   ├── simulation.py     — /api/simulation (run, pause, resume, status)
│   │   └── report.py         — /api/report (generate report, agent chat)
│   ├── services/
│   │   ├── ontology_generator.py   — LLM extracts entities/relationships
│   │   ├── graph_builder.py        — writes ontology to Neo4j
│   │   ├── profile_generator.py    — generates agent personas from graph
│   │   ├── simulation_runner.py    — launches OASIS subprocess, IPC handler
│   │   └── report_agent.py         — ReACT loop over simulation logs
│   ├── models/
│   │   └── task.py                 — async task manager (track long-running jobs)
│   ├── utils/
│   │   ├── logger.py               — rotating file + console logger
│   │   └── llm_client.py           — smart model routing (default vs smart)
│   ├── __init__.py                 — Flask app factory
│   └── config.py                   — loads and validates .env
├── scripts/
│   └── oasis_runner.py             — OASIS simulation entry point
├── uploads/                        — uploaded source documents (gitignored)
├── run.py                          — starts Flask on port 5001
└── pyproject.toml                  — Python deps (managed by uv)
```

## API Endpoints

### Graph Domain `/api/graph`
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/graph/upload` | Upload source document |
| POST | `/api/graph/build` | Start graph extraction (async) |
| GET  | `/api/graph/status/<task_id>` | Check extraction progress |
| GET  | `/api/graph/result` | Get completed graph data |

### Simulation Domain `/api/simulation`
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/simulation/prepare` | Generate agent profiles + config |
| POST | `/api/simulation/start` | Launch simulation |
| POST | `/api/simulation/pause` | Pause running simulation |
| POST | `/api/simulation/resume` | Resume paused simulation |
| GET  | `/api/simulation/status` | Get current simulation state |
| GET  | `/api/simulation/feed` | Stream live agent activity |

### Report Domain `/api/report`
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/report/generate` | Start report generation (async) |
| GET  | `/api/report/result` | Get completed report |
| POST | `/api/report/chat` | Chat with ReportAgent |
| GET  | `/api/report/agents` | List all simulated agents |
| POST | `/api/report/agent/chat` | Chat with a specific agent |

## Development

```bash
cd backend
uv sync
uv run python run.py
```
