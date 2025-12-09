
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
