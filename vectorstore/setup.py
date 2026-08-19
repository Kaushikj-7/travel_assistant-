"""
ChromaDB Vector Store Setup & Query Utilities (Chroma Cloud & Local Support).

Connects directly to Chroma Cloud using CloudClient (with local fallback).
Seeds the collection with verified factual chunks for Paris, Tokyo, and New York.
"""

import os
import chromadb
from dotenv import load_dotenv
from vectorstore.data import CITY_KNOWLEDGE, SUPPORTED_CITIES

load_dotenv()

# Module-level singletons
_client = None
_collection = None


def get_vectorstore():
    """Return the ChromaDB collection, initializing and seeding it in Chroma Cloud."""
    global _client, _collection

    if _collection is not None:
        return _collection

    api_key = os.getenv("CHROMA_API_KEY", "ck-48mQdd1EfhFkk3HBFjSVcpyFJ9VLx6omBuG2cDYiTWiU").strip()
    tenant = os.getenv("CHROMA_TENANT", "a84184bf-33bc-40c4-a487-e63e1b37eca3").strip()
    database = os.getenv("CHROMA_DATABASE", "travel_agent").strip()

    # 1. Attempt Chroma Cloud Client
    if api_key and not api_key.startswith("ck-your"):
        try:
            _client = chromadb.CloudClient(
                api_key=api_key,
                tenant=tenant,
                database=database,
            )
            _collection = _client.get_or_create_collection(
                name="city_knowledge",
                metadata={"hnsw:space": "cosine"},
            )
            print(f"Connected to Chroma Cloud (Tenant: {tenant[:8]}..., Database: {database})")
        except Exception as e:
            print(f"Notice: Chroma Cloud connection fallback ({e}). Using local ChromaDB.")
            _client = None
            _collection = None

    # 2. Local in-memory fallback client
    if _collection is None:
        _client = chromadb.Client()
        _collection = _client.get_or_create_collection(
            name="city_knowledge",
            metadata={"hnsw:space": "cosine"},
        )

    # Seed collection with knowledge chunks if empty
    try:
        if _collection.count() == 0:
            ids = []
            documents = []
            metadatas = []

            for city, chunks in CITY_KNOWLEDGE.items():
                for chunk in chunks:
                    ids.append(chunk["id"])
                    documents.append(chunk["text"])
                    metadatas.append({"city": city.lower()})

            _collection.add(ids=ids, documents=documents, metadatas=metadatas)
            print(f"Seeded {_collection.count()} knowledge chunks into ChromaDB collection 'city_knowledge'.")
    except Exception as e:
        print(f"Notice during seeding: {e}")

    return _collection


def query_vectorstore(query: str, n_results: int = 5) -> dict:
    """Query Chroma Cloud vector store and return matching results.

    Args:
        query: The search query string or city name.
        n_results: Maximum number of results to return.

    Returns:
        A dict with keys 'documents', 'metadatas', 'distances', and
        'found_city' (the matched city name in SUPPORTED_CITIES, or None).
    """
    query_clean = query.strip().lower()
    collection = get_vectorstore()

    # 1. Exact or keyword match against supported vectorstore cities
    matched_city = None
    for city in SUPPORTED_CITIES:
        if city in query_clean or (city == "new york" and ("nyc" in query_clean or "new york" in query_clean)):
            matched_city = city
            break

    # 2. Semantic vector query
    results = collection.query(query_texts=[query], n_results=n_results)

    docs = results["documents"][0] if (results and results.get("documents") and results["documents"]) else []
    metas = results["metadatas"][0] if (results and results.get("metadatas") and results["metadatas"]) else []
    dists = results["distances"][0] if (results and results.get("distances") and results["distances"]) else []

    # If keyword didn't match, check cosine distance threshold with high confidence
    if not matched_city and dists and metas:
        if dists[0] < 0.45:
            candidate = metas[0].get("city")
            if candidate in SUPPORTED_CITIES:
                matched_city = candidate

    # Filter documents to the matched city if matched
    if matched_city:
        matched_docs = [
            doc for doc, meta in zip(docs, metas) if meta.get("city") == matched_city
        ]
        if not matched_docs:
            filtered = collection.get(where={"city": matched_city}, limit=n_results)
            matched_docs = filtered["documents"] if filtered and filtered.get("documents") else docs
    else:
        matched_docs = []

    return {
        "documents": matched_docs,
        "metadatas": metas,
        "distances": dists,
        "found_city": matched_city,
    }
