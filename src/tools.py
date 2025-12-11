"""
LangChain Tools for Content Generation
These are reusable content logic blocks wrapped as LangChain tools.
"""
from langchain_core.tools import tool
from src.models import InternalProductModel, QuestionInput
from typing import List, Dict, Any

# ============================================================================
# PARSING TOOLS
# ============================================================================

@tool
def parse_product_data(raw: Dict[str, Any]) -> InternalProductModel:
    """
    Normalizes and validates raw product data into internal model.
    Converts keys to snake_case, parses lists, and handles price formatting.
    """
    model_data = {}
    for k, v in raw.items():
        model_data[k.lower().replace(' ', '_')] = v
    
    # Handle list fields
    if isinstance(model_data.get('key_ingredients'), str):
        model_data['key_ingredients'] = [i.strip() for i in model_data['key_ingredients'].split(',')]
    
    if isinstance(model_data.get('skin_type'), str):
        model_data['skin_type'] = [s.strip() for s in model_data['skin_type'].split(',')]

    # Handle price
    p = model_data.get('price')
    try:
        if isinstance(p, str) and p.startswith('₹'):
            p = p.replace('₹', '').strip()
        model_data['price'] = float(p)
    except Exception:
        model_data['price'] = None

    return InternalProductModel(**model_data)

# ============================================================================
# QUESTION GENERATION TOOLS
# ============================================================================

@tool
def generate_questions(model: InternalProductModel) -> List[QuestionInput]:
    """
    Generates 15+ categorized user questions based on product data.
    Categories: Informational, Safety, Usage, Purchase, Comparison
    """
    name = model.product_name
    ingredients = ", ".join(model.key_ingredients)
    skin_types = ", ".join(model.skin_type)
    
    questions = [
        # Informational (5)
        QuestionInput(
            question=f"What is {name}?",
            category="Informational",
            answer_hint=f"{name} is a skincare product with {model.concentration}."
        ),
        QuestionInput(
            question="What are the key ingredients?",
            category="Informational",
            answer_hint=ingredients
        ),
        QuestionInput(
            question="What benefits does this product provide?",
            category="Informational",
            answer_hint=model.benefits or "See product description"
        ),
        QuestionInput(
            question="What skin types is this suitable for?",
            category="Informational",
            answer_hint=skin_types
        ),
        QuestionInput(
            question="What is the concentration of the active ingredient?",
            category="Informational",
            answer_hint=model.concentration or "Refer to packaging"
        ),
        
        # Usage (4)
        QuestionInput(
            question="How do I use this product?",
            category="Usage",
            answer_hint=model.how_to_use or "Follow packaging instructions"
        ),
        QuestionInput(
            question="When should I apply this product?",
            category="Usage",
            answer_hint="In the morning before sunscreen"
        ),
        QuestionInput(
            question="How much product should I apply?",
            category="Usage",
            answer_hint="2-3 drops per application"
        ),
        QuestionInput(
            question="Can I use this with other skincare products?",
            category="Usage",
            answer_hint="Yes, but avoid layering with strong actives like retinol"
        ),
        
        # Safety (3)
        QuestionInput(
            question="Are there any side effects?",
            category="Safety",
            answer_hint=model.side_effects or "No known side effects"
        ),
        QuestionInput(
            question="Is this safe for sensitive skin?",
            category="Safety",
            answer_hint="May cause mild tingling. Do a patch test first."
        ),
        QuestionInput(
            question="Can I use this product during pregnancy?",
            category="Safety",
            answer_hint="Consult your dermatologist before use"
        ),
        
        # Purchase (2)
        QuestionInput(
            question="What is the price?",
            category="Purchase",
            answer_hint=f"₹{int(model.price)}" if model.price else "Contact retailer"
        ),
        QuestionInput(
            question="Where can I buy this product?",
            category="Purchase",
            answer_hint="Available at authorized retailers and online stores"
        ),
        
        # Comparison (2)
        QuestionInput(
            question="How does this compare to other Vitamin C serums?",
            category="Comparison",
            answer_hint=f"Features {model.concentration} with {ingredients}"
        ),
        QuestionInput(
            question="What makes this product unique?",
            category="Comparison",
            answer_hint=f"Combines {ingredients} for enhanced {model.benefits}"
        ),
    ]
    
    return questions

# ============================================================================
# CONTENT LOGIC BLOCKS (Reusable Transformation Functions)
# ============================================================================

@tool
def generate_benefits_block(model: InternalProductModel) -> Dict[str, Any]:
    """
    Content block: Transforms benefits into structured format.
    Returns summary and bullet points.
    """
    benefits_list = [b.strip() for b in (model.benefits or "").split(',')]
    return {
        "summary": f"This product provides {model.benefits}.",
        "bullets": benefits_list
    }

@tool
def generate_usage_block(model: InternalProductModel) -> Dict[str, Any]:
    """
    Content block: Transforms usage instructions into structured format.
    Includes dosage and timing recommendations.
    """
    return {
        "instructions": model.how_to_use or "Follow packaging directions",
        "dosage": "2-3 drops",
        "timing": "Morning before sunscreen",
        "frequency": "Daily"
    }

@tool
def generate_safety_block(model: InternalProductModel) -> Dict[str, Any]:
    """
    Content block: Transforms safety information into structured format.
    Includes side effects and warnings.
    """
    return {
        "side_effects": model.side_effects or "None reported",
        "warnings": [
            "Perform a patch test before first use",
            "Avoid contact with eyes",
            "Store in a cool, dry place"
        ],
        "contraindications": ["Do not use on broken skin"]
    }

@tool
def generate_ingredients_block(model: InternalProductModel) -> List[Dict[str, str]]:
    """
    Content block: Transforms ingredients into structured format with roles.
    """
    active_ingredients = ['vitamin c', 'hyaluronic acid', 'niacinamide', 'retinol']
    return [
        {
            "name": ingredient,
            "role": "Active" if ingredient.lower() in active_ingredients else "Support",
            "benefit": _get_ingredient_benefit(ingredient)
        }
        for ingredient in model.key_ingredients
    ]

def _get_ingredient_benefit(ingredient: str) -> str:
    """Helper: Returns known benefit for common ingredients."""
    benefits_map = {
        "vitamin c": "Brightening and antioxidant protection",
        "hyaluronic acid": "Deep hydration and plumping",
        "niacinamide": "Pore minimizing and barrier repair",
        "retinol": "Anti-aging and cell turnover"
    }
    return benefits_map.get(ingredient.lower(), "Skin conditioning")

@tool
def generate_comparison_block(model_a: InternalProductModel, model_b: Dict[str, Any]) -> Dict[str, Any]:
    """
    Content block: Compares two products by ingredients, price, and benefits.
    """
    a_ings = set(i.lower() for i in model_a.key_ingredients)
    b_ings = set(i.lower() for i in model_b.get("key_ingredients", []))
    
    return {
        "common_ingredients": list(a_ings & b_ings),
        "unique_to_a": list(a_ings - b_ings),
        "unique_to_b": list(b_ings - a_ings),
        "price_difference": (model_b.get("price", 0) or 0) - (model_a.price or 0),
        "recommendation": "Choose based on your skin concerns and budget"
    }
