"""
LangChain Orchestrator
Coordinates multi-agent workflow using LangChain's chain composition.
"""
from typing import Dict, Any
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableParallel
from src.agents import (
    ParserAgent,
    QuestionGeneratorAgent,
    ContentBlockAgent,
    ComparisonAgent,
    AssemblyAgent,
    get_all_agents
)

class ContentGenerationOrchestrator:
    """
    LangChain-based orchestrator that coordinates multiple agents.
    Uses RunnableSequence for sequential agent execution.
    """
    
    def __init__(self):
        # Initialize all agents
        self.agents = get_all_agents()
        self.parser = self.agents["parser"]
        self.question_generator = self.agents["question_generator"]
        self.content_blocks = self.agents["content_blocks"]
        self.comparison = self.agents["comparison"]
        self.assembly = self.agents["assembly"]
    
    def create_chain(self):
        """
        Creates a LangChain RunnableSequence for the content generation workflow.
        
        Flow:
        1. Parser Agent → product_model
        2. Parallel: Question Generator + Content Blocks + Comparison
        3. Assembly Agent → final pages
        """
        
        # Step 1: Parse input
        parse_step = RunnableLambda(
            lambda x: {
                "raw_input": x["raw_input"],
                "product_model": self.parser.invoke(x["raw_input"])
            }
        )
        
        # Step 2: Generate content (can run in parallel conceptually)
        generate_step = RunnableLambda(
            lambda x: {
                **x,
                "questions": self.question_generator.invoke(x["product_model"]),
                "content_blocks": self.content_blocks.invoke(x["product_model"]),
                "comparison_data": self.comparison.invoke(x["product_model"])
            }
        )
        
        # Step 3: Assemble final pages
        assemble_step = RunnableLambda(
            lambda x: {
                **x,
                "outputs": self.assembly.invoke(
                    product_model=x["product_model"],
                    questions=x["questions"],
                    content_blocks=x["content_blocks"],
                    comparison_data=x["comparison_data"]
                )
            }
        )
        
        # Compose the chain
        chain = parse_step | generate_step | assemble_step
        return chain
    
    def run(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the full content generation pipeline.
        
        Args:
            raw_input: Raw product data dictionary
            
        Returns:
            Dictionary containing all generated pages
        """
        chain = self.create_chain()
        result = chain.invoke({"raw_input": raw_input})
        return result["outputs"]


def create_orchestrator() -> ContentGenerationOrchestrator:
    """Factory function to create the orchestrator."""
    return ContentGenerationOrchestrator()
