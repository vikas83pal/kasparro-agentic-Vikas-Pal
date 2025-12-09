
import json
import os
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

from agents.parser_agent import ParserAgent
from agents.qgen_agent import QuestionGenAgent
from agents.block_agent import BlockAgent
from agents.template_agent import TemplateAgent
from agents.assembler_agent import AssemblerAgent
from orchestrator import Orchestrator

BASE = os.path.dirname(__file__)
OUTPUT_PATH = os.path.join(BASE, 'outputs')
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)


FAQ_TEMPLATE = {
    'title': 'FAQ - {{model.product_name}}',
    'questions': 'questions'
}

PRODUCT_TEMPLATE = {
    'name': '{{model.product_name}}',
    'price': '{{model.price}}',
    'concentration': '{{model.concentration}}',
    'ingredients': {'block': 'ingredients_block'},
    'benefits': {'block': 'benefits_block'},
    'usage': {'block': 'usage_block'},
    'safety': {'block': 'safety_block'},
    'questions': 'questions'
}

COMPARISON_TEMPLATE = {
    'title': 'Comparison',
    'compare': {'block': 'compare_ingredients_block'}
}

TEMPLATES = {
    'faq': FAQ_TEMPLATE,
    'product_page': PRODUCT_TEMPLATE,
    'comparison': COMPARISON_TEMPLATE
}

# Input product
RAW_PRODUCT = {
    'Product Name': 'GlowBoost Vitamin C Serum',
    'Concentration': '10% Vitamin C',
    'Skin Type': 'Oily, Combination',
    'Key Ingredients': 'Vitamin C, Hyaluronic Acid',
    'Benefits': 'Brightening, Fades dark spots',
    'How to Use': 'Apply 2 drops in the morning before sunscreen',
    'Side Effects': 'Mild tingling for sensitive skin',
    'Price': '699'
}


def build_and_run():
    parser = ParserAgent()
    qgen = QuestionGenAgent()
    block = BlockAgent()
    template_agent = TemplateAgent(block)
    assembler = AssemblerAgent(template_agent, TEMPLATES, OUTPUT_PATH)

    orchestrator = Orchestrator({'parser': parser, 'qgen': qgen, 'assembler': assembler})
    outputs = orchestrator.run(RAW_PRODUCT)
    print('Outputs written to', OUTPUT_PATH)
    print('Generated files:')
    print('  - faq.json')
    print('  - product_page.json')
    print('  - comparison_page.json')


if __name__ == '__main__':
    build_and_run()
