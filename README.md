# 🤖 Adaptive Customer Support Agent – Comprehensive README

A production-ready, enterprise-grade AI platform delivering **contextual, 24/7 banking support**. Combining LangChain-powered agent workflows, RetrievalAugmented Generation (RAG), and GPT-4 reasoning to resolve **23+ banking intents** in under 800 ms median latency, with seamless human escalation when needed.

## 📋 Table of Contents
1. [🚀 Why This Project Matters](#🚀-why-this-project-matters)  
2. [✨ Feature Highlights](#✨-feature-highlights)  
3. [🏗️ High-Level Architecture](#🏗️-high-level-architecture)  
4. [🛠️ Tech Stack](#🛠️-tech-stack)  
5. [📂 Directory Overview](#📂-directory-overview)  
6. [⚡ Quick Start Guide](#⚡-quick-start-guide)  
7. [🧪 Testing & Quality](#🧪-testing--quality)  
8. [🔌 API Cheatsheet](#🔌-api-cheatsheet)  
9. [📈 Observability & Monitoring](#📈-observability--monitoring)  
10. [🚀 Deployment Recipes](#🚀-deployment-recipes)  
11. [🤝 Contributing](#🤝-contributing)  
12. [📝 License](#📝-license)  

## 🚀 Why This Project Matters
Customer support in finance struggles with inconsistent answers, after-hours delays, and high costs. The Adaptive Agent:
- **Resolves** 23+ banking intents (balances, fraud, loans, cards, transfers) in under **800 ms** median latency.  
- **Achieves** >88% first-contact resolution by combining RAG context with GPT-4 reasoning.  
- **Escalates** gracefully when confidence |REST| B(FastAPI API)
    C[Streamlit Demo] -->|WebSocket| B
  end
  subgraph Core
    B --> D{Intent Classifier}
    D --> E[RAG Retriever]
    E --> F[GPT-4 Responder]
    F --> G{Escalation?}
    G -- Yes --> H[Create Ticket & Human]
    G -- No  --> I[Return Reply]
  end
  subgraph Data
    J[(MongoDB)]
    K[(Redis Cache)]
    L[(FAISS/Chroma Vector DB)]
  end
  B -- sessions→ J & K  
  E -- vectors→ L  
  H -- ticket→ J
```

## 🛠️ Tech Stack
| Layer           | Tools & Versions                                   |
|-----------------|----------------------------------------------------|
| **Agents & AI** | LangChain 0.2 · LangGraph 0.0.46 · OpenAI GPT-4 · Sentence-Transformers 2.7 |
| **Backend**     | FastAPI 0.111 · Python 3.11 · asyncio               |
| **Storage**     | MongoDB 6 · Redis 7 (cache) · FAISS 1.8 / Chroma 0.5 |
| **DevOps**      | Docker · Azure DevOps · LangSmith · Pytest 8         |

## 📂 Directory Overview
```
src/
  agents/        # intent_classifier.py, conversation_agent.py, rag_agent.py, escalation_agent.py
  core/          # config.py, database.py, vector_store.py, llm_client.py, memory.py
  channels/      # fastapi_channel.py, streamlit_channel.py
  routing/       # workflow_router.py, intent_router.py
  tools/         # banking_tools.py, knowledge_base.py, customer_tools.py
  data/          # banking_intents.json, knowledge_docs/
tests/           # pytest: unit, integration, performance
docker/          # Dockerfile, docker-compose.yml
docs/            # ARCHITECTURE.md, DEPLOYMENT.md, API_DOCS.md
main.py          # Entry point
README.md        # This file
```

## ⚡ Quick Start Guide
```bash
# 1. Clone & configure
git clone https://github.com/you/adaptive-support.git
cd adaptive-support
cp .env.example .env   # Provide OPENAI_API_KEY, Mongo URI, etc.

# 2. Launch with Docker
docker compose -f docker/docker-compose.yml up --build -d

# 3. Access
# – FastAPI Swagger: http://localhost:8000/docs
# – Streamlit Demo:  http://localhost:8501
```
**Smoke Test**  
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"demo123","message":"Show my recent transactions"}'
```

## 🧪 Testing & Quality
- **Run tests**: `pytest -q` (aim ≥90% coverage)  
- **CI**: Lint → Tests on Python 3.11 & 3.12 → Coverage check  
- **Performance**: Concurrency & latency benchmarks included  

## 🔌 API Cheatsheet
| Endpoint                         | Method | Purpose                                 |
|----------------------------------|--------|-----------------------------------------|
| POST `/api/v1/chat`              | Chat   | Conversational endpoint (session_id, message) |
| POST `/api/v1/classify`          | Intent | Standalone intent classification         |
| GET  `/api/v1/sessions/{id}`     | Session| Retrieve full conversation transcript    |
| GET  `/api/v1/escalations`       | Tickets| List open escalation tickets             |
| GET  `/metrics`                  | Metrics| Prometheus-style performance metrics     |

_All endpoints support `Authorization: Bearer ` when enabled._

## 📈 Observability & Monitoring
- **LangSmith**: Traces every LLM call; token & latency dashboards.  
- **Prometheus**: Optional `/metrics` for QPS, P95 latency, cache hit rate.  
- **Alerts**: Webhooks for high escalation rate (>15%) or GPT error rate (>2%).  

## 🚀 Deployment Recipes
### Docker-Compose Production
```bash
docker compose -f docker/docker-compose.yml --env-file .env-prod up -d --scale app=3
```
### Kubernetes Snippet
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
        readinessProbe:
          httpGet: { path: /ready, port: 8000 }
          initialDelaySeconds: 5
```

## 🤝 Contributing
1. **Fork** & create branch: `feature/x`  
2. **Implement** feature or fix; include unit tests (≥90% cov)  
3. **Lint** & **format** using Pre-commit hooks (`black`, `flake8`, `mypy`)  
4. **PR** → passes CI → merged ← celebrate!  

## 📝 License
**MIT License** – free for commercial & private use. Contributions welcome!
