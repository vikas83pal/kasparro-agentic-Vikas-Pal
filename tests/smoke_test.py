
import json
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents.parser_agent import ParserAgent
from src.agents.qgen_agent import QuestionGenAgent
from src.agents.block_agent import BlockAgent
from src.agents.template_agent import TemplateAgent
from src.agents.assembler_agent import AssemblerAgent
from src.orchestrator import Orchestrator


def test_orchestrator():
   

    output_path = '/tmp/test_outputs'
    os.makedirs(output_path, exist_ok=True)

    templates = {
        'faq': {
            'title': 'FAQ - {{model.product_name}}',
            'questions': 'questions'
        },
        'product_page': {
            'name': '{{model.product_name}}',
            'price': '{{model.price}}',
            'concentration': '{{model.concentration}}',
            'ingredients': {'block': 'ingredients_block'},
            'benefits': {'block': 'benefits_block'},
            'usage': {'block': 'usage_block'},
            'safety': {'block': 'safety_block'},
            'questions': 'questions'
        },
        'comparison': {
            'title': 'Comparison',
            'compare': {'block': 'compare_ingredients_block'}
        }
    }

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

    parser = ParserAgent()
    qgen = QuestionGenAgent()
    block = BlockAgent()
    template_agent = TemplateAgent(block)
    assembler = AssemblerAgent(template_agent, templates, output_path)

    orchestrator = Orchestrator({'parser': parser, 'qgen': qgen, 'assembler': assembler})
    outputs = orchestrator.run(raw_product)


    assert outputs is not None, "Orchestrator should return outputs"
    assert 'faq' in outputs, "Output should contain FAQ"
    assert 'product_page' in outputs, "Output should contain product_page"
    assert 'comparison' in outputs, "Output should contain comparison"

    faq = outputs['faq']
    assert 'title' in faq, "FAQ should have title"
    assert 'questions' in faq, "FAQ should have questions"
    assert len(faq['questions']) > 0, "FAQ should have questions"


    product = outputs['product_page']
    assert 'name' in product, "Product should have name"
    assert 'price' in product, "Product should have price"
    assert 'ingredients' in product, "Product should have ingredients"
    assert 'benefits' in product, "Product should have benefits"


    comparison = outputs['comparison']
    assert 'title' in comparison, "Comparison should have title"
    assert 'compare' in comparison, "Comparison should have compare"
    assert 'product_b' in comparison, "Comparison should have product_b"

    print("All smoke tests passed!")
    return True


if __name__ == '__main__':
    test_orchestrator()
