#!/usr/bin/env python
"""Setup script to create all project files."""
import os

base = r'c:\Users\Lenovo\Downloads\kasparro_ai_project'
src = os.path.join(base, 'src')
agents_dir = os.path.join(src, 'agents')

# Create orchestrator.py
with open(os.path.join(src, 'orchestrator.py'), 'w', encoding='utf-8') as f:
    f.write('''# src/orchestrator.py
from typing import Dict, Any


class Orchestrator:
    """Simple DAG orchestrator. Runs agents in a defined order and passes outputs explicitly."""
    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents

    def run(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        # Parser
        product_model = self.agents['parser'].run(raw_input)

        # Questions
        questions = self.agents['qgen'].run(product_model)

        # Assemble pages
        outputs = self.agents['assembler'].run(product_model, questions)

        return outputs
''')

# Create parser_agent.py
with open(os.path.join(agents_dir, 'parser_agent.py'), 'w', encoding='utf-8') as f:
    f.write('''# src/agents/parser_agent.py
from typing import Dict, Any


class ParserAgent:
    """Normalize and validate product input."""
    REQUIRED = ['Product Name', 'Concentration', 'Skin Type', 'Key Ingredients', 'Benefits', 'How to Use', 'Side Effects', 'Price']

    def run(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        # Simple normalization
        model = {}
        for k in raw:
            model[k.lower().replace(' ', '_')] = raw[k]

        # Ensure required fields exist
        for r in self.REQUIRED:
            key = r.lower().replace(' ', '_')
            if key not in model:
                model[key] = None

        # Normalize lists
        if isinstance(model.get('key_ingredients'), str):
            model['key_ingredients'] = [i.strip() for i in model['key_ingredients'].split(',')]

        if isinstance(model.get('skin_type'), str):
            model['skin_type'] = [s.strip() for s in model['skin_type'].split(',')]

        # Price numeric
        p = model.get('price')
        try:
            if isinstance(p, str) and p.startswith('₹'):
                p = p.replace('₹', '').strip()
            model['price'] = float(p)
        except Exception:
            model['price'] = None

        return model
''')

# Create qgen_agent.py
with open(os.path.join(agents_dir, 'qgen_agent.py'), 'w', encoding='utf-8') as f:
    f.write('''# src/agents/qgen_agent.py
from typing import List, Dict


class QuestionGenAgent:
    """Generate categorized questions from the product model."""

    def run(self, model: Dict) -> List[Dict]:
        name = model.get('product_name')
        ingredients = model.get('key_ingredients', [])
        benefits = model.get('benefits')

        questions = []

        # Informational
        questions.append({'question': f'What is {name}?', 'category': 'Informational', 'answer_hint': f'{name} with {model.get("concentration")}.'})
        questions.append({'question': 'What are the key ingredients?', 'category': 'Informational', 'answer_hint': ', '.join(ingredients)})

        # Usage
        questions.append({'question': 'How do I use it?', 'category': 'Usage', 'answer_hint': model.get('how_to_use')})
        questions.append({'question': 'When should I apply this product?', 'category': 'Usage', 'answer_hint': 'In the morning before sunscreen'})

        # Safety
        questions.append({'question': 'Are there any side effects?', 'category': 'Safety', 'answer_hint': model.get('side_effects')})
        questions.append({'question': 'Is this safe for sensitive skin?', 'category': 'Safety', 'answer_hint': 'May cause mild tingling for sensitive skin'})

        # Purchase
        questions.append({'question': 'How much does it cost?', 'category': 'Purchase', 'answer_hint': f'₹{int(model.get("price")) if model.get("price") else "N/A"}'})
        questions.append({'question': 'Where can I buy it?', 'category': 'Purchase', 'answer_hint': 'Available from listed retailers'})

        # Comparison
        questions.append({'question': 'How does it compare to other vitamin C serums?', 'category': 'Comparison', 'answer_hint': '10% concentration and includes hyaluronic acid'})

        # Benefits / Efficacy
        questions.append({'question': 'What benefits can I expect?', 'category': 'Informational', 'answer_hint': benefits})
        questions.append({'question': 'Will it help fade dark spots?', 'category': 'Informational', 'answer_hint': 'Designed to help fade dark spots'})

        # Target audience
        questions.append({'question': 'What skin types is this for?', 'category': 'Informational', 'answer_hint': ', '.join(model.get('skin_type', []))})

        # Logistics
        questions.append({'question': 'How much should I apply?', 'category': 'Usage', 'answer_hint': '2–3 drops'})
        questions.append({'question': 'Can I use it with other actives (retinol/acid)?', 'category': 'Safety', 'answer_hint': 'Use caution with strong actives'})

        # Add one more to reach 15
        questions.append({'question': 'How soon will I see results?', 'category': 'Informational', 'answer_hint': 'Results may vary; visible improvement over weeks'})

        # Ensure at least 15
        if len(questions) < 15:
            while len(questions) < 15:
                questions.append({'question': f'Additional question {len(questions)+1}', 'category': 'Other', 'answer_hint': ''})

        return questions
''')

# Create block_agent.py
with open(os.path.join(agents_dir, 'block_agent.py'), 'w', encoding='utf-8') as f:
    f.write('''# src/agents/block_agent.py
from typing import Dict, Any, List


class BlockAgent:
    """Reusable content logic blocks. Each method is stateless and pure: input -> output."""

    def benefits_block(self, model: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'summary': f"Provides {model.get('benefits')}.",
            'bullets': [b.strip() for b in (model.get('benefits') or '').split(',')] or []
        }

    def usage_block(self, model: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'how_to_use': model.get('how_to_use'),
            'dosage': '2-3 drops',
            'timing': 'Morning before sunscreen'
        }

    def safety_block(self, model: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'side_effects': model.get('side_effects'),
            'warnings': ['Patch test before use']
        }

    def ingredients_block(self, model: Dict[str, Any]) -> List[Dict[str, str]]:
        return [{'ingredient': i, 'role': 'active' if i.lower().strip() in ['vitamin c', 'hyaluronic acid'] else 'support'} for i in model.get('key_ingredients', [])]

    def compare_ingredients_block(self, model_a: Dict[str, Any], model_b: Dict[str, Any]) -> Dict[str, Any]:
        a_ings = set([i.lower() for i in model_a.get('key_ingredients', [])])
        b_ings = set([i.lower() for i in model_b.get('key_ingredients', [])])
        common = list(a_ings & b_ings)
        only_a = list(a_ings - b_ings)
        only_b = list(b_ings - a_ings)
        return {'common': common, 'only_a': only_a, 'only_b': only_b}
''')

# Create template_agent.py
with open(os.path.join(agents_dir, 'template_agent.py'), 'w', encoding='utf-8') as f:
    f.write('''# src/agents/template_agent.py
import json
from typing import Dict, Any


class TemplateAgent:
    """Simple template engine that resolves model refs and calls blocks via provided block_interface."""

    def __init__(self, block_interface):
        self.block = block_interface

    def render(self, template_def: Dict[str, Any], model: Dict[str, Any], questions=None) -> Dict[str, Any]:
        out = {}
        for field, spec in template_def.items():
            if isinstance(spec, str) and spec.startswith('{{') and spec.endswith('}}'):
                # model reference
                key = spec[2:-2].strip()
                out[field] = self._resolve_model_ref(key, model)
            elif isinstance(spec, dict) and spec.get('block'):
                block_name = spec['block']
                # call block
                fn = getattr(self.block, block_name)
                # some blocks take two args (compare)
                if block_name == 'compare_ingredients_block':
                    out[field] = fn(model, spec.get('with'))
                else:
                    out[field] = fn(model)
            elif field == 'questions' and questions is not None:
                out[field] = questions
            else:
                out[field] = spec
        return out

    def _resolve_model_ref(self, key: str, model: Dict[str, Any]):
        # simple dotted/key lookup
        if key.startswith('model.'):
            k = key[len('model.'):]
            return model.get(k)
        return None
''')

# Create assembler_agent.py
with open(os.path.join(agents_dir, 'assembler_agent.py'), 'w', encoding='utf-8') as f:
    f.write('''# src/agents/assembler_agent.py
import json
from typing import Dict, Any, List


class AssemblerAgent:
    def __init__(self, template_agent, templates: Dict[str, Dict[str, Any]], output_path: str):
        self.template_agent = template_agent
        self.templates = templates
        self.output_path = output_path

    def run(self, model: Dict[str, Any], questions: List[Dict[str, Any]]):
        outputs = {}

        # FAQ
        faq_json = self.template_agent.render(self.templates['faq'], model, questions=questions[:10])
        outputs['faq'] = faq_json
        with open(f'{self.output_path}/faq.json', 'w', encoding='utf8') as f:
            json.dump(faq_json, f, indent=2, ensure_ascii=False)

        # Product page
        product_json = self.template_agent.render(self.templates['product_page'], model, questions=questions)
        outputs['product_page'] = product_json
        with open(f'{self.output_path}/product_page.json', 'w', encoding='utf8') as f:
            json.dump(product_json, f, indent=2, ensure_ascii=False)

        # Comparison: create a fictional product B
        product_b = self._make_fictional_product_b(model)
        comparison_template = self.templates['comparison']
        comparison_template = json.loads(json.dumps(comparison_template))
        if 'compare' in comparison_template:
            comp_spec = comparison_template['compare']
            if isinstance(comp_spec, dict) and comp_spec.get('block') == 'compare_ingredients_block':
                comp_spec['with'] = product_b

        comparison_json = self.template_agent.render(comparison_template, model)
        comparison_json['product_b'] = product_b
        outputs['comparison'] = comparison_json
        with open(f'{self.output_path}/comparison_page.json', 'w', encoding='utf8') as f:
            json.dump(comparison_json, f, indent=2, ensure_ascii=False)

        return outputs

    def _make_fictional_product_b(self, a_model: Dict[str, Any]) -> Dict[str, Any]:
        # Fictional product B: same schema but different values
        return {
            'product_name': 'RadiantBlend Vitamin C Concentrate',
            'concentration': '12% Vitamin C',
            'skin_type': ['Dry', 'Combination'],
            'key_ingredients': ['Vitamin C', 'Niacinamide'],
            'benefits': 'Brightening, Hydration',
            'how_to_use': 'Apply at night',
            'side_effects': 'None commonly reported',
            'price': 899.0
        }
''')

# Create main.py
with open(os.path.join(src, 'main.py'), 'w', encoding='utf-8') as f:
    f.write('''# src/main.py
import json
import os
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

# Templates (kept inline for simplicity; in repo they are files)
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
    'How to Use': 'Apply 2–3 drops in the morning before sunscreen',
    'Side Effects': 'Mild tingling for sensitive skin',
    'Price': '₹699'
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


if __name__ == '__main__':
    build_and_run()
''')

print('All Python files created successfully!')
