# Research Assistant Agent

This repo contains a hybrid Research Assistant that combines an exact Knowledge Graph (Neo4j) with a Retrieval‑Augmented Generation pipeline (FAISS + Cross‑Encoder + FLAN‑T5) behind a sleek Streamlit interface.

## Overview

This project demonstrates a two‑pronged approach to question answering over a corpus of research papers:

- **Structured Queries via Neo4j**  
  Exact, lightning‑fast answers for graph‑able questions (e.g. “Which approaches used ResNet backbone?”).

- **Free‑Form QA via RAG Pipeline**  
  Semantic search (FAISS) + keyword filtering + cross‑encoder reranking + an LLM (FLAN‑T5) to handle open‑ended queries.

---

## Features

- **Graph‑Based Retrieval** with Cypher queries for high‑precision lookups.  
- **Vector‑Based Retrieval** using FAISS for deep semantic similarity.  
- **Cross‑Encoder Reranking** to boost relevance of top FAISS hits.  
- **LLM‑Based Synthesis** with HuggingFace’s FLAN‑T5.  
- **Interactive UI** powered by Streamlit, complete with real‑time metrics and example prompts.  
- **Containerized Demo** via Docker Compose for one‑command deployment.

---

## Prerequisites

- **Docker** & **Docker Compose** (for containerized demo)  
- **Python 3.10+** and **pip** (for local development)  
- (Optional) **Conda** for environment management

---

## Installation

### Local Setup

1. **Clone the repository**  
   ```
   git clone https://github.com/abdulvahapmutlu/research-agent.git
   cd research-agent
   ```

2. **Create and activate your environment**  
   **Conda**:  
   ```
   conda env create -f environment.yml
   conda activate agent
   ```  
   **venv**:  
   ```
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   .\venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

4. **Set environment variables**  
   ```
   export NEO4J_URI="bolt://localhost:7687"
   export NEO4J_USER="neo4j"
   export NEO4J_PASS="password"
   ```  
   *Windows (PowerShell)*:  
   ```
   $env:NEO4J_URI="bolt://localhost:7687"
   $env:NEO4J_USER="neo4j"
   $env:NEO4J_PASS="password"
   ```

5. **Populate the Neo4j graph**  
   Make sure Neo4j is running (e.g. via `docker-compose up neo4j`), then:  
   ```
   python graph/import_to_neo4j.py
   ```

6. **Launch the Streamlit app**  
   ```
   streamlit run app.py
   ```  
   Open your browser at [http://localhost:8501](http://localhost:8501).

---

### Docker Compose (One‑Command Demo)

1. Add your Neo4j credentials into the `neo4j.environment` and `app.environment` sections of `docker-compose.yml`.  
2. Run:
   ```
   docker-compose up --build
   ```  
3. Browse to [http://localhost:8501](http://localhost:8501) for the live demo.

---

## Usage

- **Structured Questions** (graph route):  
  - “Which approaches use ResNet backbone?”  

- **Free‑Form Questions** (RAG fallback):  
  - “Summarize the Transformer training setup.”  

Type your query into the text box and hit **Ask**. The UI will display either a graph‑backed result or a generated answer with source snippets.

### ⚠️ Important Note ⚠️
This is a demo project; therefore, it is only for demonstration and it may not answer each query. To specialize, you need to recreate it with your own data or use an LLM API

---

## Configuration

- **Reader Model**: Override `google/flan-t5-large` by setting `READER_MODEL` in your environment.  
- **Streamlit Port**: Change via `streamlit run app.py --server.port <port>`.  
- **Neo4j**: Adjust bolt URI, username, and password via environment variables.

---

## Troubleshooting

- **AuthError**: Ensure your Neo4j password is ≥ 8 characters and matches the env vars.  
- **Slow RAG**: Reduce `SEMANTIC_K` or use a smaller reader model.  
- **Missing Index**: Rebuild with `python retriever_embeddings.py`.

## License

MIT License. See [LICENSE](LICENSE) for details.
