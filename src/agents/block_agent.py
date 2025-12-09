
from typing import Dict, Any, List


class BlockAgent:
   

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
