from agents.analyse import analyser_image
from agents.llm_decision import LLMDecisionAgent
from agents.evaluation import EvaluationAgent

class Orchestrator:
    def __init__(self):
        self.llm = LLMDecisionAgent()
        self.evaluator = EvaluationAgent()

    def analyser_image(self, image):
        return analyser_image(image)
