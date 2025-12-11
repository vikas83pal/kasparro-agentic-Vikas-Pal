"""
LangChain Agents Module
Real agent components with clear responsibilities using LangChain's agent framework.
"""
from typing import List, Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.output_parsers import JsonOutputParser

from src.tools import (
    parse_product_data,
    generate_questions,
    generate_benefits_block,
    generate_usage_block,
    generate_safety_block,
    generate_ingredients_block,
    generate_comparison_block
)
from src.models import InternalProductModel, QuestionInput

# ============================================================================
# AGENT 1: PARSER AGENT
# ============================================================================

class ParserAgent:
    """
    Agent responsible for parsing and normalizing raw product data.
    Uses the parse_product_data tool to transform input into internal model.
    """
    
    def __init__(self):
        self.name = "ParserAgent"
        self.tools = [parse_product_data]
        self.description = "Parses raw product JSON into normalized internal model"
    
    def invoke(self, raw_input: Dict[str, Any]) -> InternalProductModel:
        """Execute the parsing tool and return normalized model."""
        result = parse_product_data.invoke(raw_input)
        return result


# ============================================================================
# AGENT 2: QUESTION GENERATION AGENT
# ============================================================================

class QuestionGeneratorAgent:
    """
    Agent responsible for generating categorized user questions.
    Uses rule-based templates to create 15+ questions across categories.
    """
    
    def __init__(self):
        self.name = "QuestionGeneratorAgent"
        self.tools = [generate_questions]
        self.description = "Generates categorized FAQ questions from product data"
    
    def invoke(self, product_model: InternalProductModel) -> List[QuestionInput]:
        """Execute question generation tool."""
        result = generate_questions.invoke(product_model)
        return result


# ============================================================================
# AGENT 3: CONTENT BLOCK AGENT
# ============================================================================

class ContentBlockAgent:
    """
    Agent responsible for generating reusable content blocks.
    Orchestrates multiple block-generation tools to create structured content.
    """
    
    def __init__(self):
        self.name = "ContentBlockAgent"
        self.tools = [
            generate_benefits_block,
            generate_usage_block,
            generate_safety_block,
            generate_ingredients_block
        ]
        self.description = "Generates reusable content blocks (benefits, usage, safety, ingredients)"
    
    def invoke(self, product_model: InternalProductModel) -> Dict[str, Any]:
        """Execute all content block tools and aggregate results."""
        return {
            "benefits": generate_benefits_block.invoke(product_model),
            "usage": generate_usage_block.invoke(product_model),
            "safety": generate_safety_block.invoke(product_model),
            "ingredients": generate_ingredients_block.invoke(product_model)
        }


# ============================================================================
# AGENT 4: COMPARISON AGENT
# ============================================================================

class ComparisonAgent:
    """
    Agent responsible for comparing two products.
    Creates fictional Product B and generates comparison analysis.
    """
    
    def __init__(self):
        self.name = "ComparisonAgent"
        self.tools = [generate_comparison_block]
        self.description = "Compares Product A with fictional Product B"
    
    def create_fictional_product(self) -> Dict[str, Any]:
        """Generate a fictional competitor product for comparison."""
        return {
            "product_name": "RadiantGlow Vitamin C Concentrate",
            "concentration": "15% Vitamin C",
            "key_ingredients": ["Vitamin C", "Niacinamide", "Ferulic Acid"],
            "benefits": "Brightening, Anti-aging, Pore minimizing",
            "price": 899.0
        }
    
    def invoke(self, product_model: InternalProductModel) -> Dict[str, Any]:
        """Execute comparison tool with fictional product."""
        product_b = self.create_fictional_product()
        comparison = generate_comparison_block.invoke({
            "model_a": product_model,
            "model_b": product_b
        })
        return {
            "product_b": product_b,
            "comparison": comparison
        }


# ============================================================================
# AGENT 5: ASSEMBLY AGENT
# ============================================================================

class AssemblyAgent:
    """
    Agent responsible for assembling final JSON pages.
    Combines outputs from other agents into structured page objects.
    """
    
    def __init__(self):
        self.name = "AssemblyAgent"
        self.tools = []  # Uses composition, not tools
        self.description = "Assembles final JSON pages from agent outputs"
    
    def invoke(
        self,
        product_model: InternalProductModel,
        questions: List[QuestionInput],
        content_blocks: Dict[str, Any],
        comparison_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assemble all three output pages."""
        from src.models import ProductPage, FAQPage, ComparisonPage, Benefits, Usage, Safety, Ingredient
        
        # Build ingredients list
        ingredients_list = [
            Ingredient(ingredient=ing["name"], role=ing["role"])
            for ing in content_blocks["ingredients"]
        ]
        
        # Assemble Product Page
        product_page = ProductPage(
            name=product_model.product_name,
            price=product_model.price,
            concentration=product_model.concentration,
            ingredients=ingredients_list,
            benefits=Benefits(
                summary=content_blocks["benefits"]["summary"],
                bullets=content_blocks["benefits"]["bullets"]
            ),
            usage=Usage(
                how_to_use=content_blocks["usage"]["instructions"],
                dosage=content_blocks["usage"]["dosage"],
                timing=content_blocks["usage"]["timing"]
            ),
            safety=Safety(
                side_effects=content_blocks["safety"]["side_effects"],
                warnings=content_blocks["safety"]["warnings"]
            ),
            questions=questions[:5]
        )
        
        # Assemble FAQ Page
        faq_page = FAQPage(
            title=f"FAQ - {product_model.product_name}",
            questions=questions
        )
        
        # Assemble Comparison Page
        comparison_page = ComparisonPage(
            title="Product Comparison",
            product_a={
                "name": product_model.product_name,
                "concentration": product_model.concentration,
                "ingredients": product_model.key_ingredients,
                "benefits": product_model.benefits,
                "price": product_model.price
            },
            product_b=comparison_data["product_b"],
            comparison=comparison_data["comparison"]
        )
        
        return {
            "product_page": product_page,
            "faq_page": faq_page,
            "comparison_page": comparison_page
        }


# ============================================================================
# AGENT REGISTRY
# ============================================================================

def get_all_agents() -> Dict[str, Any]:
    """Returns all available agents for the orchestrator."""
    return {
        "parser": ParserAgent(),
        "question_generator": QuestionGeneratorAgent(),
        "content_blocks": ContentBlockAgent(),
        "comparison": ComparisonAgent(),
        "assembly": AssemblyAgent()
    }
