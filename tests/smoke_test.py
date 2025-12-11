"""
Smoke Test for LangChain Content Generation Pipeline
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_pipeline():
    """Test that the LangChain pipeline runs correctly."""
    from src.orchestrator import create_orchestrator
    from src.models import ProductPage, FAQPage, ComparisonPage
    
    # Input data
    raw_product = {
        'Product Name': 'GlowBoost Vitamin C Serum',
        'Concentration': '10% Vitamin C',
        'Skin Type': 'Oily, Combination',
        'Key Ingredients': 'Vitamin C, Hyaluronic Acid',
        'Benefits': 'Brightening, Fades dark spots',
        'How to Use': 'Apply 2–3 drops in the morning before sunscreen',
        'Side Effects': 'Mild tingling for sensitive skin',
        'Price': '₹699'
    }
    
    # Create orchestrator and run
    orchestrator = create_orchestrator()
    outputs = orchestrator.run(raw_product)
    
    # Assertions
    assert 'product_page' in outputs, "Should have product_page"
    assert 'faq_page' in outputs, "Should have faq_page"
    assert 'comparison_page' in outputs, "Should have comparison_page"
    
    # Validate types
    assert isinstance(outputs['product_page'], ProductPage)
    assert isinstance(outputs['faq_page'], FAQPage)
    assert isinstance(outputs['comparison_page'], ComparisonPage)
    
    # Validate content
    assert outputs['product_page'].name == 'GlowBoost Vitamin C Serum'
    assert outputs['product_page'].price == 699.0
    assert len(outputs['faq_page'].questions) >= 15
    
    print("✅ All tests passed!")
    return True

if __name__ == '__main__':
    try:
        test_pipeline()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
