from phase2.graph_utils import build_node_index, get_neighbors

class RepoRetriever:
    def __init__(self, vector_store, symbol_graph, embedder):
        self.vector_store = vector_store
        self.symbol_graph = symbol_graph
        self.embedder = embedder
        self.node_index = build_node_index(symbol_graph)

    def query(self, text: str, top_k: int = 5):
        query_vector = self.embedder.embed([text])[0]

        hits = self.vector_store.client.query_points(
            collection_name=self.vector_store.collection,
            query=query_vector,
            limit=top_k
        )

        expanded = {}
        for hit in hits:
            symbol_id = hit.payload["symbol_id"]
            expanded[symbol_id] = hit.payload

            # graph expansion
            neighbors = get_neighbors(self.symbol_graph, symbol_id)
            for nid in neighbors:
                if nid in self.node_index:
                    expanded[nid] = self.node_index[nid]

        return list(expanded.values())