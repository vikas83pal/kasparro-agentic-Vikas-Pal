"""
Graph Nodes for LangGraph Workflow
Each node has a single responsibility and defined input/output.
"""
from typing import Dict, Any
from src.state import AgentState
from src.tools import (
    parse_product_data, 
    generate_questions,
    generate_benefits_block,
    generate_usage_block,
    generate_safety_block,
    generate_ingredients_block,
    generate_comparison_block
)
from src.models import (
    ProductPage, ComparisonPage, FAQPage, 
    Benefits, Safety, Usage, Ingredient
)

# ============================================================================
# NODE 1: PARSER
# ============================================================================

def parser_node(state: AgentState) -> Dict[str, Any]:
    """
    Responsibility: Parse and normalize raw product input.
    Input: raw_input (dict)
    Output: product_model (InternalProductModel)
    """
    raw = state['raw_input']
    product_model = parse_product_data.invoke(raw)
    return {"product_model": product_model}

# ============================================================================
# NODE 2: QUESTION GENERATOR
# ============================================================================

def question_generator_node(state: AgentState) -> Dict[str, Any]:
    """
    Responsibility: Generate 15+ categorized questions.
    Input: product_model
    Output: generated_questions (List[QuestionInput])
    """
    model = state['product_model']
    questions = generate_questions.invoke(model)
    return {"generated_questions": questions}

# ============================================================================
# NODE 3: CONTENT BLOCKS GENERATOR
# ============================================================================

def content_blocks_node(state: AgentState) -> Dict[str, Any]:
    """
    Responsibility: Generate reusable content blocks.
    Input: product_model
    Output: content_blocks (dict with benefits, usage, safety, ingredients)
    """
    model = state['product_model']
    
    benefits = generate_benefits_block.invoke(model)
    usage = generate_usage_block.invoke(model)
    safety = generate_safety_block.invoke(model)
    ingredients = generate_ingredients_block.invoke(model)
    
    return {
        "content_blocks": {
            "benefits": benefits,
            "usage": usage,
            "safety": safety,
            "ingredients": ingredients
        }
    }

# ============================================================================
# NODE 4: PAGE ASSEMBLER
# ============================================================================

def assembly_node(state: AgentState) -> Dict[str, Any]:
    """
    Responsibility: Assemble final pages using templates and content blocks.
    Input: product_model, generated_questions, content_blocks
    Output: product_page, faq_page, comparison_page
    """
    model = state['product_model']
    questions = state['generated_questions']
    blocks = state['content_blocks']
    
    # -------------------------
    # 1. Assemble Product Page
    # -------------------------
    ingredients_list = [
        Ingredient(
            ingredient=ing["name"],
            role=ing["role"]
        )
        for ing in blocks["ingredients"]
    ]
    
    product_page = ProductPage(
        name=model.product_name,
        price=model.price,
        concentration=model.concentration,
        ingredients=ingredients_list,
        benefits=Benefits(
            summary=blocks["benefits"]["summary"],
            bullets=blocks["benefits"]["bullets"]
        ),
        usage=Usage(
            how_to_use=blocks["usage"]["instructions"],
            dosage=blocks["usage"]["dosage"],
            timing=blocks["usage"]["timing"]
        ),
        safety=Safety(
            side_effects=blocks["safety"]["side_effects"],
            warnings=blocks["safety"]["warnings"]
        ),
        questions=questions[:5]  # Top 5 for product page
    )
    
    # -------------------------
    # 2. Assemble FAQ Page
    # -------------------------
    faq_page = FAQPage(
        title=f"FAQ - {model.product_name}",
        questions=questions  # All 15+ questions
    )
    
    # -------------------------
    # 3. Assemble Comparison Page
    # -------------------------
    # Create fictional Product B
    product_b = {
        "product_name": "RadiantGlow Vitamin C Concentrate",
        "concentration": "15% Vitamin C",
        "key_ingredients": ["Vitamin C", "Niacinamide", "Ferulic Acid"],
        "benefits": "Brightening, Anti-aging, Pore minimizing",
        "price": 899.0
    }
    
    # Generate comparison block
    comparison = generate_comparison_block.invoke({"model_a": model, "model_b": product_b})
    
    comparison_page = ComparisonPage(
        title="Product Comparison",
        product_a={
            "name": model.product_name,
            "concentration": model.concentration,
            "ingredients": model.key_ingredients,
            "benefits": model.benefits,
            "price": model.price
        },
        product_b=product_b,
        comparison=comparison
    )
    
    return {
        "product_page": product_page,
        "faq_page": faq_page,
        "comparison_page": comparison_page
    }
