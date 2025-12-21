def build_node_index(symbol_graph: dict):
    return {node["id"]: node for node in symbol_graph.get("nodes",[])}

def get_neighbors(symbol_graph: dict, node_id:str):
    neighbors = []
    for edge in symbol_graph.get("edges", []):
        if edge["source"] == node_id:
            neighbors.append(edge["target"])
        elif edge["target"] == node_id:
            neighbors.append(edge["source"])
    return neighbors
