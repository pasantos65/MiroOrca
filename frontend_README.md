# MiroOrca Frontend

Vue.js 3 + Vite + Tailwind CSS

## Structure

```
frontend/
├── src/
│   ├── views/                   — one view per simulation stage
│   │   ├── Home.vue             — Stage 0: create / open simulation
│   │   ├── GraphBuild.vue       — Stage 1: upload + graph extraction
│   │   ├── AgentSetup.vue       — Stage 2: review / edit personas
│   │   ├── SimulationRun.vue    — Stage 3: live simulation feed
│   │   ├── Report.vue           — Stage 4: read prediction report
│   │   └── Chat.vue             — Stage 5: chat with agents
│   ├── components/
│   │   ├── StepWizard.vue       — progress indicator (steps 1–5)
│   │   ├── AgentCard.vue        — individual persona display
│   │   ├── SimulationFeed.vue   — live post/reply stream
│   │   ├── GraphVisualizer.vue  — D3.js force-directed graph
│   │   └── SentimentChart.vue   — D3.js sentiment arc over rounds
│   ├── api/
│   │   └── client.js            — axios wrapper for all backend calls
│   ├── router/
│   │   └── index.js             — Vue Router (step-based routing)
│   ├── stores/
│   │   └── simulation.js        — Pinia store (simulation state)
│   ├── App.vue
│   └── main.js
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## Design Principles

- **Dark mode by default** — dark slate background, high-contrast text
- **Step wizard** — persistent top progress bar showing current stage
- **Live feed** — simulation posts appear in real time via polling
- **Agent cards** — click any agent to view full profile + history
- **Responsive** — works on desktop and tablet

## Development

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:3000 and proxies API calls to the backend at :5001.
