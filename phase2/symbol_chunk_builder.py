import os
import ast

class SymbolChunkBuilder:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self._ast_cache = {}
        self._source_cache = {}

    def build_chunks(self, symbol_graph: dict):
        chunks = []

        for node in symbol_graph.get("nodes", []):
            if node["type"] not in {"class", "method", "function"}:
                continue

            chunk = self._build_chunk(node)
            if chunk:
                chunks.append(chunk)

        return chunks

    def _build_chunk(self, node: dict):
        if node['type']!="class":
            return None
        rel_path = node["file"]
        abs_path = os.path.join(self.repo_root,"source", rel_path)
        if not os.path.exists(abs_path):
            return None
        
        tree, source_lines = self._parse_file(abs_path)

        for ast_node in ast.walk(tree):
            if isinstance(ast_node,ast.ClassDef) and ast_node.name == node["id"]:
                code_text = self._extract_node_text(ast_node, source_lines)
                docstring = ast.get_docstring(ast_node)

                text_parts=[
                    f"class {ast_node.name} defines in {rel_path}",

                ]
                if docstring:
                    text_parts.append(f"docstring:\n{docstring}")
                text_parts.append("code:\n"+ code_text)
                
                return {
                "symbol_id": node["id"],
                "symbol_type": "class",
                "file": rel_path,
                "text": "\n\n".join(text_parts),
                "metadata": {}                   
                }
        return None


    def _parse_file(self, file_path: str):
        if file_path in self._ast_cache:
            return self._ast_cache[file_path], self._source_cache[file_path]

        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)
        self._ast_cache[file_path] = tree
        self._source_cache[file_path] = source.splitlines()

        return tree, self._source_cache[file_path]

    def _extract_node_text(self, ast_node, source_lines):
        start = ast_node.lineno - 1
        end = ast_node.end_lineno
        return "\n".join(source_lines[start:end])
