graph TB
  subgraph UI
    Web[Web / Mobile] -->|REST| API
    Streamlit -->|WebSocket| API
  end

  subgraph Application
    API[FastAPI] --> Router(Workflow Router)
    Router --> Intent(Intent Classifier)
    Intent --> Draft(RAG + Draft LLM)
    Draft --> Check[Escalation Check]
    Check -- yes --> Escalate[Escalation Agent]
    Check -- no --> Reply[Send Reply]
  end

  subgraph Data
    Mongo[(MongoDB)]
    Redis[(Redis)]
    FAISS[(FAISS / Chroma)]
  end

  Draft --vector search--> FAISS
  API --session logs--> Mongo & Redis
  Escalate --ticket--> Mongo
