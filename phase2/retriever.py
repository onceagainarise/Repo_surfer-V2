from phase2.graph_utils import build_node_index, get_neighbors

class RepoRetriever:
    def __init__(self, vector_store, symbol_graph, embedder):
        self.vector_store = vector_store
        self.symbol_graph = symbol_graph
        self.embedder = embedder
        self.node_index = build_node_index(symbol_graph)

    def query(self, text: str, top_k: int = 5):
        # 1️⃣ Embed query
        query_vector = self.embedder.embed([text])[0]

        # 2️⃣ Vector search (abstracted)
        hits = self.vector_store.search(query_vector, limit=top_k)

        results = {}
        
        # 3️⃣ Add vector hits
        for hit in hits:
            payload = hit.payload
            symbol_id = payload["symbol_id"]

            results[symbol_id] = {
                "symbol_id": symbol_id,
                "symbol_type": payload.get("symbol_type"),
                "file": payload.get("file"),
                "score": hit.score,
                "source": "vector"
            }

            # 4️⃣ Graph expansion
            neighbors = get_neighbors(self.symbol_graph, symbol_id)
            for nid in neighbors:
                if nid in self.node_index and nid not in results:
                    node = self.node_index[nid]
                    results[nid] = {
                        "symbol_id": nid,
                        "symbol_type": node["type"],
                        "file": node.get("file"),
                        "score": hit.score * 0.7,  # decay
                        "source": "graph"
                    }

        # 5️⃣ Sort by score
        return sorted(results.values(), key=lambda x: x["score"], reverse=True)
