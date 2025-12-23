# reposurfer_orchestrator/query.py

def query_repository(question: str):
    from phase_4_retrieval.runner import retrieve_context
    from phase_5_reasoning.runner import run_llm

    context = retrieve_context(question)
    answer = run_llm(question, context)

    return answer
