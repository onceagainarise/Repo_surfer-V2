# reposurfer_orchestrator/index.py

def index_repository(repo_path: str):
    # Phase 1
    from clone.runner import clone_repo
    clone_repo(repo_path)

    # Phase 2
    from symbol_graph.runner import build_symbol_graph
    build_symbol_graph(repo_path)

    # Phase 3
    from embeddings.runner import generate_embeddings
    generate_embeddings(repo_path)

    print("✅ Repository indexed successfully")
