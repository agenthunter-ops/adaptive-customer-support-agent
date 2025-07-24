# 🤖 Adaptive Customer Support Agent – Expanded README

A production-ready AI platform that delivers contextual, 24/7 banking support. It fuses LangChain-powered agents, Retrieval-Augmented (RAG), and GPT-4 reasoning to resolve 23 + banking intents in seconds while smoothly escalating edge-cases to humans.

## 📋 Table of Contents
- [🚀 Why This Project Matters](#🚀-why-this-project-matters)
- [✨ Feature Highlights](#✨-feature-highlights)
- [🏗️ High-Level Architecture](#🏗️-high-level-architecture)
- [🛠️ Tech Stack](#🛠️-tech-stack)
- [📂 Directory Overview](#📂-directory-overview)
- [⚡ Quick Start Guide](#⚡-quick-start-guide)
- [🧪 Testing & Quality](#🧪-testing--quality)
- [🔌 API Cheatsheet](#🔌-api-cheatsheet)
- [📈 Observability & Monitoring](#📈-observability--monitoring)
- [🚀 Deployment Recipes](#🚀-deployment-recipes)
- [🤝 Contributing](#🤝-contributing)
- [📝 License](#📝-license)

## 🚀 Why This Project Matters
Traditional service desks crumble under high volume, inconsistent answers, and after-hours gaps. Our Adaptive Agent:

- Resolves common banking questions (balances, fraud, loans, card issues) in 88% first-contact resolution.  
- Escalates gracefully with full transcript + ticket ID when confidence |REST JSON| B(FastAPI)
  C[Streamlit Demo] -->|WebSocket| B
end
subgraph Core
  B --> D{IntentClassifier}
  D --> E[RAGRetriever]
  E --> F[GPT-4Responder]
  F --> G{NeedEscalation?}
  G -- yes --> H[Create Ticket → Human]
  G -- no --> I[Send Reply]
end
subgraph Data
  J[(MongoDB)]
  K[(Redis)]
  L[(FAISS / Chroma)]
end
B -- sessions --> J & K
E -- vectors --> L
H -- ticket log --> J
```

## 🛠️ Tech Stack
| Layer | Primary Tools / Versions |
|-------|-------------------------|
| Agents | LangChain 0.2, LangGraph 0.0.46, OpenAI GPT-4 |
| Backend | FastAPI 0.111, Python 3.11, asyncio |
| Persistence | MongoDB 6, Redis 7 |
| RAG | FAISS 1.8 OR Chroma 0.5 |
| DevOps | Docker, Azure DevOps, LangSmith, Pytest 8 |

## 📂 Directory Overview
```
src/
  agents/        # intent_classifier.py, conversation_agent.py, rag_agent.py, escalation_agent.py
  core/          # config.py, database.py, vector_store.py, llm_client.py, memory.py
  channels/      # fastapi_channel.py (REST), streamlit_channel.py (demo UI)
  routing/       # workflow_router.py, intent_router.py
  tools/         # banking_tools.py, knowledge_base.py, customer_tools.py
  data/          # banking_intents.json, knowledge_base docs
tests/           # pytest unit + integration
docker/          # Dockerfile, docker-compose.yml
docs/            # architecture & deployment guides
```

## ⚡ Quick Start Guide
```bash
# 1. Clone & configure
git clone https://github.com/you/adaptive-support.git
cd adaptive-support
cp .env.example .env   # add OPENAI_API_KEY, Mongo URI, etc.

# 2. Launch everything with Docker
docker compose -f docker/docker-compose.yml up --build -d

# 3. Explore
open http://localhost:8000/docs      # Swagger
open http://localhost:8501           # Streamlit demo
```
### Curl Smoke Test
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"demo123","message":"Show my recent transactions"}'
```

## 🧪 Testing & Quality
```bash
pytest -q           # fast run
pytest --cov=src    # coverage report (goal ≥90%)
```
CI runs lint + tests on Python 3.11 & 3.12. Fail-fast if coverage dips.

## 🔌 API Cheatsheet
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/chat` | POST | Primary conversation (JSON body: `session_id`, `message`) |
| `/api/v1/classify` | POST | Isolated intent detection |
| `/api/v1/sessions/{id}` | GET | Fetch full transcript |
| `/api/v1/escalations` | GET | List open tickets |

All endpoints accept `Authorization: Bearer ` when auth enabled.

## 📈 Observability & Monitoring
- **LangSmith**: captures every LangChain call; view token counts & latencies.  
- **Prometheus**: optional `/metrics` endpoint for QPS, P95 latency, cache hits.  
- **Alerts**: webhook fires if escalation rate >15% or GPT error rate >2%.

## 🚀 Deployment Recipes
### Docker-Compose Prod
```bash
docker compose -f docker/docker-compose.yml --env-file .env-prod up -d --scale app=3
```
### Kubernetes (snippet)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: adaptive-support }
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: your-reg/adaptive-support:latest
        envFrom: [{ secretRef: { name: support-secrets } }]
        ports: [{ containerPort: 8000 }]
        readinessProbe: { httpGet: { path: /ready, port: 8000 }, initialDelaySeconds: 5 }
```

## 🤝 Contributing
1. **Fork → Branch (`feature/x`) → PR**.  
2. Include unit tests; keep coverage ≥90%.  
3. Follow black + flake8. Pre-commit hooks auto-format.

## 📝 License
MIT – free for commercial & private use. Contributions welcome!
