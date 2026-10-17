from agents.analyse import analyser_image
from agents.llm_decision import LLMDecisionAgent
from agents.evaluation import EvaluationAgent

class Orchestrator:

    def __init__(self):
        self.llm = LLMDecisionAgent()
        self.evaluator = EvaluationAgent()

    def process(self, image, original_path, compress_function):

        # 1️⃣ Analyse
        features = analyser_image(image)

        # 2️⃣ Décision IA
        decision = self.llm.decide(features)

        # 3️⃣ Compression
        compressed_path = compress_function(image, decision)

        # 4️⃣ Évaluation
        metrics = self.evaluator.evaluate(original_path, compressed_path)

        return {
            "features": features,
            "decision": decision,
            "metrics": metrics,
            "compressed_path":compressed_path
        }