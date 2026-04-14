# MiroOrca Quick Start

Get MiroOrca running in under 5 minutes using Docker.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- An API key from any of: OpenAI, Anthropic, Google, or [OpenRouter](https://openrouter.ai)
  *(or skip this and use Ollama for free local inference — see below)*

## Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/MiroOrca.git
cd MiroOrca
```

## Step 2 — Configure your environment

```bash
cp .env.example .env
```

Open `.env` in any text editor and fill in at minimum:

```env
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4o-mini
```

See the full [Configuration Guide](docs/configuration.md) for all options.

## Step 3 — Start MiroOrca

```bash
docker compose up -d
```

Docker will pull and start three containers:
- `miroorca-frontend` — Vue.js UI on port 3000
- `miroorca-backend` — Flask API on port 5001
- `miroorca-neo4j` — Neo4j graph database on port 7474/7687

## Step 4 — Open the UI

Visit **http://localhost:3000** in your browser.

You should see the MiroOrca home screen. Click **New Simulation** to begin.

---

## Using Ollama (Free, No API Key)

If you want to run everything locally at no cost:

```bash
# Install Ollama from https://ollama.com then:
ollama pull qwen2.5:14b
ollama pull nomic-embed-text

# Then in .env set:
# LLM_API_KEY=ollama
# LLM_BASE_URL=http://host.docker.internal:11434/v1
# LLM_MODEL_NAME=qwen2.5:14b
```

Then run `docker compose up -d` as normal.

---

## Stopping MiroOrca

```bash
docker compose down
```

To also remove all stored data (simulations, graphs):

```bash
docker compose down -v
```

---

## Troubleshooting

**Port already in use?**
Edit `docker-compose.yml` and change the host port mappings (left side of the colon).

**Neo4j won't start?**
Make sure Docker has at least 4GB of memory allocated (Docker Desktop → Settings → Resources).

**LLM errors?**
Check your API key in `.env` and confirm the `LLM_BASE_URL` matches your provider.

For more help, open an [Issue](../../issues).
