import os
import time
import streamlit as st
from agent_orchestrator import answer

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🧠 Research Assistant Agent",
    page_icon="🤖",
    layout="wide",
)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📚 Research Assistant")
    st.write(
        """
        This demos a **Knowledge Graph** (Neo4j) + **RAG QA Pipeline**  
        (FAISS + Cross‑Encoder + FLAN‑T5) all in one agent.
        """
    )
    st.markdown("---")
    st.subheader("Try questions like")
    st.markdown(
        "- Which approaches used ResNet backbone?\n"
        "- Which methods achieved >90% on CIFAR-10?\n"
        "- Summarize the Transformer training setup"
    )
    st.markdown("---")
    st.caption("Built with Streamlit • Free on Streamlit Community Cloud")

# ─── Main ───────────────────────────────────────────────────────────────────────
st.title("🧠 Research Assistant Agent")
st.markdown(
    """
    **Ask questions** about your corpus.  
    Graph‑answerable queries (e.g. ResNet backbone) hit Neo4j instantly.  
    Everything else falls back to RAG.
    """
)
st.markdown("---")

# ─── Metrics ────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
# Number of JSON docs
docs_dir = os.path.join("data", "text_json")
docs_count = sum(1 for f in os.listdir(docs_dir) if f.endswith(".json"))
# FAISS index files & size
index_dir = os.path.join("retriever", "faiss_index")
files = os.listdir(index_dir)
size_mb = sum(os.path.getsize(os.path.join(index_dir, f)) for f in files) / (1024**2)
col1.metric("📄 Papers Indexed", docs_count)
col2.metric("📚 Index Files", len(files))
col3.metric("💾 Index Size (MB)", f"{size_mb:.1f}")

st.markdown("---")

# ─── Query Input ────────────────────────────────────────────────────────────────
query = st.text_input(
    "💬 Your question here",
    value="Which approaches used ResNet backbone?",
    max_chars=200,
)

if st.button("🔎 Ask", use_container_width=True):
    with st.spinner("🤔 Thinking..."):
        t0 = time.time()
        resp = answer(query)
        elapsed = time.time() - t0

    st.markdown(f"**Answer** (in {elapsed:.2f}s)")
    st.write(resp)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.write(
    "© 2025 Your Name • "
    "[GitHub](https://github.com/yourusername) • "
    "[LinkedIn](https://linkedin.com/in/yourusername)"
)
