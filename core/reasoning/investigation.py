from reposurfer.core.reasoning.prompt_builder import build_investigation_prompt
from reposurfer.core.reasoning.llm_client import LLMClient

class InvestigationPlanner:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_plan(self, query: str, retrieved_symbols: list[dict]) -> str:
        messages = build_investigation_prompt(query, retrieved_symbols)
        return self.llm.generate(messages)
