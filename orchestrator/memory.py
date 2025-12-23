# reposurfer_orchestrator/memory.py

class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, question, answer):
        self.history.append((question, answer))

    def get_context(self):
        return self.history[-5:]
