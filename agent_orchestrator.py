#!/usr/bin/env python3
"""
agent_orchestrator.py

Combine Neo4j graph lookup + your RAG QA pipeline into one answer() entrypoint.
Reads NEO4J_URI, NEO4J_USER, NEO4J_PASS from env; imports real `qa`.
"""

import os
import re
from neo4j import GraphDatabase

# Import the actual RetrievalQA you built earlier
from retriever_rerank_rag import qa

# ─── CONFIG FROM ENV ──────────────────────────────────────────────────────────
NEO4J_URI  = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "yourStrongPassword")  # set this in your environment

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

# ─── GRAPH LOOKUP ──────────────────────────────────────────────────────────────
def graph_lookup_resnet_backbone():
    cypher = """
    MATCH (p:Paper)-[:DESCRIBES]->(m:Method)
    WHERE toLower(m.name) CONTAINS "resnet"
    RETURN DISTINCT p.id AS paper, m.name AS method
    ORDER BY p.id
    """
    with driver.session() as session:
        return [f"{rec['paper']} → {rec['method']}" for rec in session.run(cypher)]

# ─── ORCHESTRATOR ──────────────────────────────────────────────────────────────
def answer(question: str) -> str:
    q = question.lower().strip()

    # 1) Graph route for ResNet backbone
    if "resnet backbone" in q or re.search(r"\bresnet\b", q):
        hits = graph_lookup_resnet_backbone()
        if hits:
            return "📊 **Graph result:**\n" + "\n".join(f"- {h}" for h in hits)

    # 2) Fallback to your RAG QA chain
    rag = qa({"query": question})
    ans = rag["result"]
    # Format source docs
    srcs = ""
    for doc in rag.get("source_documents", []):
        snippet = doc.page_content.replace("\n", " ")
        srcs += f"- {snippet[:150]}…\n"
    return f"🤖 **RAG answer:**\n{ans}\n\n📜 **Sources:**\n{srcs}"

# ─── TEST RUN ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    q = "Which approaches used ResNet backbone?"
    print("Question:", q)
    print("\n" + answer(q))
