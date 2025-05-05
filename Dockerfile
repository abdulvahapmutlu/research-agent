FROM python:3.10-slim

# 1) System deps
RUN apt-get update && apt-get install -y \
    gcc libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Copy code
COPY . /app

# 3) Install Python deps
RUN pip install --no-cache-dir \
    streamlit \
    neo4j \
    langchain \
    transformers \
    sentence-transformers \
    faiss-cpu \
    python-dotenv

# 4) Expose Streamlit port
EXPOSE 8501

# 5) Entrypoint
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
