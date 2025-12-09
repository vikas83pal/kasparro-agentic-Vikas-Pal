
from typing import Dict, Any


class ParserAgent:

    REQUIRED = ['Product Name', 'Concentration', 'Skin Type', 'Key Ingredients', 'Benefits', 'How to Use', 'Side Effects', 'Price']

    def run(self, raw: Dict[str, Any]) -> Dict[str, Any]:
   
        model = {}
        for k in raw:
            model[k.lower().replace(' ', '_')] = raw[k]

        for r in self.REQUIRED:
            key = r.lower().replace(' ', '_')
            if key not in model:
                model[key] = None

 
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
