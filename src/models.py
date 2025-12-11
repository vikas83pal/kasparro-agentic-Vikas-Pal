from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# ============================================================================
# INPUT MODELS
# ============================================================================

class ProductInput(BaseModel):
    """Raw product data as received from external sources."""
    product_name: str = Field(alias="Product Name")
    concentration: Optional[str] = Field(None, alias="Concentration")
    skin_type: Optional[str] = Field(None, alias="Skin Type")
    key_ingredients: Optional[str] = Field(None, alias="Key Ingredients")
    benefits: Optional[str] = Field(None, alias="Benefits")
    how_to_use: Optional[str] = Field(None, alias="How to Use")
    side_effects: Optional[str] = Field(None, alias="Side Effects")
    price: Optional[str] = Field(None, alias="Price")

    class Config:
        populate_by_name = True

# ============================================================================
# INTERNAL MODELS
# ============================================================================

class InternalProductModel(BaseModel):
    """Normalized internal representation of product data."""
    product_name: str
    concentration: Optional[str] = None
    skin_type: List[str] = Field(default_factory=list)
    key_ingredients: List[str] = Field(default_factory=list)
    benefits: Optional[str] = None
    how_to_use: Optional[str] = None
    side_effects: Optional[str] = None
    price: Optional[float] = None

class QuestionInput(BaseModel):
    """A generated question with category and answer hint."""
    question: str
    category: str
    answer_hint: str

# ============================================================================
# CONTENT BLOCK MODELS
# ============================================================================

class Ingredient(BaseModel):
    """Structured ingredient with role classification."""
    ingredient: str
    role: str

class Benefits(BaseModel):
    """Structured benefits block."""
    summary: str
    bullets: List[str]

class Usage(BaseModel):
    """Structured usage instructions block."""
    how_to_use: Optional[str]
    dosage: str
    timing: str

class Safety(BaseModel):
    """Structured safety information block."""
    side_effects: Optional[str]
    warnings: List[str]

# ============================================================================
# OUTPUT PAGE MODELS
# ============================================================================

class ProductPage(BaseModel):
    """Complete product page structure."""
    name: str
    price: Optional[float]
    concentration: Optional[str]
    ingredients: List[Ingredient]
    benefits: Benefits
    usage: Usage
    safety: Safety
    questions: List[QuestionInput]

class FAQPage(BaseModel):
    """FAQ page structure with categorized questions."""
    title: str
    questions: List[QuestionInput]

class ComparisonPage(BaseModel):
    """Comparison page structure for two products."""
    title: str = "Product Comparison"
    product_a: Dict[str, Any]
    product_b: Dict[str, Any]
    comparison: Dict[str, Any]
