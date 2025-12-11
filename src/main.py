"""
Main Entry Point
Runs the LangChain-based content generation pipeline.
"""
import json
import os
from src.orchestrator import create_orchestrator

# Setup paths
BASE = os.path.dirname(__file__)
OUTPUT_PATH = os.path.join(BASE, 'outputs')
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

# Input product (as specified in assignment)
RAW_PRODUCT = {
    'Product Name': 'GlowBoost Vitamin C Serum',
    'Concentration': '10% Vitamin C',
    'Skin Type': 'Oily, Combination',
    'Key Ingredients': 'Vitamin C, Hyaluronic Acid',
    'Benefits': 'Brightening, Fades dark spots',
    'How to Use': 'Apply 2–3 drops in the morning before sunscreen',
    'Side Effects': 'Mild tingling for sensitive skin',
    'Price': '₹699'
}

def run_pipeline():
    """Execute the LangChain content generation pipeline."""
    print("=" * 60)
    print("Kasparro AI Content Generation System")
    print("LangChain Multi-Agent Pipeline")
    print("=" * 60)
    
    # Create orchestrator
    print("\n[1/4] Initializing LangChain orchestrator...")
    orchestrator = create_orchestrator()
    
    # Run the chain
    print("[2/4] Executing agent workflow...")
    print("      → ParserAgent: Normalizing input data")
    print("      → QuestionGeneratorAgent: Generating questions")
    print("      → ContentBlockAgent: Creating content blocks")
    print("      → ComparisonAgent: Building comparison")
    print("      → AssemblyAgent: Assembling pages")
    
    outputs = orchestrator.run(RAW_PRODUCT)
    
    # Extract pages
    print("[3/4] Extracting outputs...")
    product_page = outputs['product_page']
    faq_page = outputs['faq_page']
    comparison_page = outputs['comparison_page']
    
    # Write to files
    print(f"[4/4] Writing JSON outputs to {OUTPUT_PATH}...")
    
    with open(os.path.join(OUTPUT_PATH, 'product_page.json'), 'w', encoding='utf-8') as f:
        json.dump(product_page.model_dump(), f, indent=2, ensure_ascii=False)
    
    with open(os.path.join(OUTPUT_PATH, 'faq.json'), 'w', encoding='utf-8') as f:
        json.dump(faq_page.model_dump(), f, indent=2, ensure_ascii=False)
    
    with open(os.path.join(OUTPUT_PATH, 'comparison_page.json'), 'w', encoding='utf-8') as f:
        json.dump(comparison_page.model_dump(), f, indent=2, ensure_ascii=False)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ SUCCESS! Generated files:")
    print("   • faq.json")
    print("   • product_page.json")
    print("   • comparison_page.json")
    print("=" * 60)
    
    # Stats
    print(f"\n📊 Statistics:")
    print(f"   Questions generated: {len(faq_page.questions)}")
    print(f"   Ingredients processed: {len(product_page.ingredients)}")
    print(f"   Content blocks created: 4 (benefits, usage, safety, ingredients)")

if __name__ == '__main__':
    run_pipeline()
