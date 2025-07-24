# 🤖 Adaptive Customer Support Agent

A **production-ready**, enterprise-grade AI platform delivering **contextual, 24/7 banking support**. Combining LangChain-powered agent workflows, Retrieval-Augmented Generation (RAG), and GPT-4 reasoning to resolve **23+ specialised banking intents** in under 800 ms median latency, with seamless human escalation when needed. This README dives into every aspect of setup, usage, architecture, and contribution to ensure you have all the information in one place.

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
11. [🔧 Configuration Details](#🔧-configuration-details)  
12. [🤝 Contributing](#🤝-contributing)  
13. [📝 License](#📝-license)

## 🚀 Why This Project Matters

Modern financial institutions face persistent customer support challenges:

- **High Volume & Costs**: Human agents can’t scale economically to meet 24/7 demand.  
- **Inconsistent Answers**: Knowledge silos lead to conflicting information.  
- **Slow Response**: Peak-hour overloads create long wait times.  
- **Limited After-Hours**: Inaccessible support outside business hours frustrates customers.  

Our Adaptive Customer Support Agent solves these by:

1. **Instant 24/7 Responses**: Automates routine queries with  88% resolution on initial interaction.  
4. **Seamless Escalation**: Human handoff with full transcript and ticket reference when confidence |REST JSON| B(FastAPI)
    C[Streamlit Demo] -->|WebSocket| B
  end

  Subgraph Core Agents
    B --> D{Intent Classifier}
    D --> E[RAG Retriever]
    E --> F[GPT-4 Responder]
    F --> G{Escalation?}
    G -- Yes --> H[Escalation Agent → Ticket]
    G -- No  --> I[Return Reply]
  end

  Subgraph Data Stores
    J[(MongoDB)]
    K[(Redis Cache)]
    L[(FAISS / Chroma Vector DB)]
  end

  B -- sessions → J & K  
  E -- vector queries → L  
  H -- tickets → J
```

## 🛠️ Tech Stack

| Layer                | Technologies & Versions                                            |
|----------------------|--------------------------------------------------------------------|
| **AI & Agents**      | LangChain 0.2 · LangGraph 0.0.46 · OpenAI GPT-4 · Sentence-Transformers 2.7 |
| **Backend**          | FastAPI 0.111 · Python 3.11 · asyncio                              |
| **Storage**          | MongoDB 6 · Redis 7 · FAISS 1.8 / Chroma 0.5                       |
| **DevOps & CI/CD**   | Docker · Azure DevOps · LangSmith · Pytest 8 + pytest-asyncio      |
| **Testing & QA**     | pytest · pytest-mock · pytest-asyncio · coverage                   |
| **Monitoring**       | Prometheus (optional) · `/metrics` endpoint · LangSmith            |

## 📂 Directory Overview

```
adaptive-customer-support-agent/
├── main.py                               # Entry point (FastAPI + optional Streamlit)
├── .env.example                          # Environment variables template
├── requirements.txt                      # Python dependencies
├── docker/                               # Dockerfile, docker-compose.yml
├── src/
│   ├── agents/                           # Core AI agents
│   │   ├── intent_classifier.py
│   │   ├── conversation_agent.py
│   │   ├── rag_agent.py
│   │   └── escalation_agent.py
│   ├── core/                            # Utilities & config
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── vector_store.py
│   │   ├── llm_client.py
│   │   └── memory.py
│   ├── channels/                        # API & UI channels
│   │   ├── fastapi_channel.py
│   │   └── streamlit_channel.py
│   ├── routing/                         # Workflow & intent routers
│   │   ├── workflow_router.py
│   │   └── intent_router.py
│   ├── tools/                           # Domain-specific tools
│   │   ├── banking_tools.py
│   │   ├── knowledge_base.py
│   │   └── customer_tools.py
│   └── data/                            # Static data files
│       ├── banking_intents.json
│       └── knowledge_docs/              # Markdown docs for RAG
├── tests/
│   ├── test_agents.py
│   ├── test_api.py
│   ├── test_routing.py
│   └── test_integration.py
└── docs/
    ├── ARCHITECTURE.md
    ├── DEPLOYMENT.md
    └── API_DOCS.md
```

## ⚡ Quick Start Guide

1. **Clone & Configure**  
   ```bash
   git clone https://github.com/yourusername/adaptive-customer-support-agent.git
   cd adaptive-customer-support-agent
   cp .env.example .env
   # Edit .env: set OPENAI_API_KEY, MONGODB_URI, REDIS_URL, VECTOR_STORE, etc.
   ```

2. **Launch via Docker**  
   ```bash
   docker compose -f docker/docker-compose.yml up --build -d
   ```

3. **Explore**  
   - **FastAPI Swagger UI**: http://localhost:8000/docs  
   - **Streamlit Demo**:      http://localhost:8501  

4. **Smoke Test**  
   ```bash
   curl -X POST http://localhost:8000/api/v1/chat \
     -H "Content-Type: application/json" \
     -d '{"session_id":"demo123","message":"Show my recent transactions"}'
   ```

## 🧪 Testing & Quality

- **Run All Tests**:  
  ```bash
  pytest --maxfail=1 --disable-warnings -q
  ```
- **Coverage**:  
  ```bash
  pytest --cov=src --cov-report=term-missing
  ```
  Aim: **≥ 90%** overall coverage.  
- **Performance**:  
  - Concurrency tests sending 100+ parallel chat requests.  
  - Latency benchmarks under 2s for 99% of requests.  
- **CI Pipeline**:  
  - **Stages**: Lint → Unit Tests → Integration Tests → Coverage → Docker Build → Deploy  
  - **Matrix**: Python 3.11 & 3.12 on Ubuntu latest  

## 🔌 API Cheatsheet

| Endpoint                        | Method | Description                                                |
|---------------------------------|--------|------------------------------------------------------------|
| **POST** `/api/v1/chat`         | Chat   | Main chat endpoint; body: `session_id`, `message`          |
| **POST** `/api/v1/classify`     | Intent | Classify free-text intent.                                 |
| **GET**  `/api/v1/sessions/{id}`| Session| Retrieve entire conversation transcript.                   |
| **DELETE** `/api/v1/sessions/{id}`| Delete| End session & cleanup data.                              |
| **GET**  `/api/v1/escalations`  | Tickets| List open/resolved escalation tickets.                     |
| **GET**  `/metrics`             | Metrics| Prometheus-style metrics: QPS, latency, cache hit rate.    |

_All endpoints support `Authorisation: Bearer ` if auth is enabled._

## 📈 Observability & Monitoring

- **LangSmith**:  
  - Trace all LangChain calls: classification, retrieval, generation.  
  - Dashboards for token usage, retrieval latency, and LLM response quality.  

- **Prometheus & Grafana**:  
  - Expose `/metrics` for QPS, P95/P99 latencies, error rates.  
  - Dashboards for active sessions, escalation rates, and cache-hit ratios.  

- **Alerting**:  
  - Webhooks or email if the escalation rate > 15%.  
  - Alerts if GPT-4 errors exceed 2%.  

## 🚀 Deployment Recipes

### Docker-Compose Production
```bash
docker compose \
  -f docker/docker-compose.yml \
  --env-file .env-prod \
  up -d --scale app=3
```

### Kubernetes Deployment Snippet
```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: adaptive-support-agent }
spec:
  replicas: 3
  selector:
    matchLabels: { app: adaptive-support-agent }
  template:
    metadata:
      labels: { app: adaptive-support-agent }
    spec:
      containers:
      - name: app
        image: your-registry/adaptive-support: latest
        envFrom: 
          - secretRef: { name: support-secrets }
        ports:
          - containerPort: 8000
        readinessProbe:
          httpGet: { path: /ready, port: 8000 }
          initialDelaySeconds: 5
```

### AWS ECS Fargate Task Definition
```json
{
  "family": "adaptive-support-agent",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam:::role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "adaptive-support",
      "image": ".dkr.ecr..amazonaws.com/adaptive-support:latest",
      "portMappings": [{ "containerPort": 8000 }],
      "environment": [{ "name": "MONGODB_URI", "value": "..." }],
      "secrets": [{ "name": "OPENAI_API_KEY", "valueFrom": "arn:aws:..." }]
    }
  ]
}
```

## 🔧 Configuration Details

| Variable                   | Description                                      | Example                                     |
|----------------------------|--------------------------------------------------|---------------------------------------------|
| `OPENAI_API_KEY`           | OpenAI API key for GPT-4                         | `sk-...`                                    |
| `MONGODB_URI`              | MongoDB connection string                        | `mongodb+srv://user:pass@cluster.mongodb.net` |
| `MONGODB_DATABASE`         | Database name                                    | `adaptive_support`                          |
| `REDIS_URL`                | Redis connection URL (optional)                  | `redis://localhost:6379`                    |
| `VECTOR_STORE`             | `faiss` or `chroma`                              | `faiss`                                     |
| `VECTOR_DIRECTORY`         | Directory for FAISS index persistence            | `./src/data/faiss_index`                    |
| `MAX_HISTORY_MESSAGES`     | Number of turns to cache in memory               | `15`                                        |
| `SIMILARITY_TOP_K`         | Number of RAG docs to retrieve per query         | `4`                                         |
| `LOG_LEVEL`                | Application log verbosity                        | `INFO`                                      |
| `WORKERS`                  | Uvicorn worker count                             | `4`                                         |
| `CACHE_TTL`                | Seconds to cache static responses                | `3600`                                      |

## 🤝 Contributing

We welcome contributions from developers, AI researchers, and banking experts:

1. **Fork & Branch**  
   ```bash
   git clone https://github.com/yourusername/adaptive-customer-support-agent.git
   cd adaptive-customer-support-agent
   git checkout -b feature/your-feature
   ```
2. **Implement & Test**  
   - Add code, tests (> 90% coverage), and update docs.  
   - Use pre-commit hooks (`black`, `flake8`, `mypy`).  

3. **Commit & PR**  
   ```bash
   git add.
   git commit -m "feat: description of your feature"
   git push origin feature/your-feature
   ```
4. **Review & Merge**  
   - CI checks must pass (lint, tests, coverage).  
   - Address review feedback.  

## 📝 License

**MIT License** – free for personal and commercial use.  
See [LICENSE](LICENSE) for full text.

