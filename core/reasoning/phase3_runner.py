import json
from retrieval.retriever import RepoRetriever
from embeddings.vector_store import VectorStore
from embeddings.embedding_generator import EmbeddingGenerator
from reasoning.llm_client import LLMClient
from reasoning.investigation import InvestigationPlanner

def run_phase3(repo_path: str, query: str):
    with open(f"{repo_path}/symbol_graph.json") as f:
        symbol_graph = json.load(f)

    repo_name = repo_path.split("/")[-1]

    embedder = EmbeddingGenerator()
    store = VectorStore(collection_name=repo_name)
    retriever = RepoRetriever(store, symbol_graph, embedder)

    print("🔍 Retrieving relevant symbols...")
    retrieved = retriever.query(query, top_k=5)

    llm = LLMClient()
    planner = InvestigationPlanner(llm)

    print("\n🧠 Generating investigation plan...\n")
    plan = planner.generate_plan(query, retrieved)

    print(plan)


if __name__ == "__main__":
    run_phase3(
        "storage/repos/psf__requests",
        "Unable to override cookie policy in Session.prepare_request ",
    )
