import json
from phase2.retriever import RepoRetriever
from phase2.vector_store import VectorStore
from phase2.embedding_generator import EmbeddingGenerator

def run_retrieval(repo_path: str, query: str):
    with open(f"{repo_path}/symbol_graph.json") as f:
        symbol_graph = json.load(f)

    embedder = EmbeddingGenerator()
    repo_name = repo_path.split("/")[-1]
    store = VectorStore(collection_name=repo_name)

    retriever = RepoRetriever(store, symbol_graph, embedder)

    results = retriever.query(query)

    for r in results:
        print(f"\n--- {r['id']} ({r['type']}) ---")
        print(r.get("text", "")[:300])

if __name__ == "__main__":
    run_retrieval(
        "storage/repos/psf__requests",
        "JSON decode error while parsing response"
    )
