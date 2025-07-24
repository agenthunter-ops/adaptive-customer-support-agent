# ----------- Stage 1: Builder (installs deps) -----------------------------
    FROM python:3.11-slim AS builder

    ENV PIP_ROOT_USER_ACTION=ignore
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --user -r requirements.txt
    
    # ----------- Stage 2: Runtime --------------------------------------------
    FROM python:3.11-slim
    
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1 \
        LANG=C.UTF-8
    
    WORKDIR /app
    COPY --from=builder /root/.local /root/.local
    ENV PATH=/root/.local/bin:$PATH
    
    COPY . /app
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    