"""
State Definition for LangGraph
Defines the shared state passed between nodes.
"""
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from src.models import InternalProductModel, ProductPage, ComparisonPage, FAQPage, QuestionInput

class AgentState(TypedDict):
    """
    Shared state for the content generation pipeline.
    Each field represents the output of a specific processing stage.
    """
    # Input
    raw_input: Dict[str, Any]
    
    # After Parser Node
    product_model: Optional[InternalProductModel]
    
    # After Question Generator Node
    generated_questions: List[QuestionInput]
    
    # After Content Blocks Node
    content_blocks: Optional[Dict[str, Any]]
    
    # After Assembly Node
    product_page: Optional[ProductPage]
    comparison_page: Optional[ComparisonPage]
    faq_page: Optional[FAQPage]
