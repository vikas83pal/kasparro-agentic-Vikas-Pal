
from typing import Dict, Any


class Orchestrator:

    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents

    def run(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:

        product_model = self.agents['parser'].run(raw_input)


        questions = self.agents['qgen'].run(product_model)

        outputs = self.agents['assembler'].run(product_model, questions)

        return outputs
