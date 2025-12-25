from pathlib import Path
from reposurfer.core.clone.phase0_runner import run_phase0
from reposurfer.core.symbol_graph.phase1_runner import run_phase1
from reposurfer.core.symbol_graph.phase1_graph_runner import run_phase1_7
from reposurfer.core.embeddings.phase2_runner import run_phase2
from reposurfer.core.embeddings.phase2_embed_runner import run_embedding
from reposurfer.core.reasoning.phase3_runner import run_phase3

class RepoSurferApp:
    def __init__(self, storage_root: str = "storage/repos"):
        self.storage_root = Path(storage_root)

    def index_repo(self, repo_url: str):
        """
        Full indexing pipeline (Phase 0 → Phase 2.3)
        """
        run_phase0(repo_url)

        owner, name = repo_url.rstrip("/").split("/")[-2:]
        repo_dir = self.storage_root / f"{owner}__{name}"

        run_phase1(str(repo_dir))
        run_phase1_7(str(repo_dir))
        run_phase2(str(repo_dir))
        run_embedding(str(repo_dir))

        print("✅ Repository indexed successfully")

    def query(self, repo_path: str, issue: str):
        """
        Retrieval + reasoning
        """
        run_phase3(repo_path, issue)
