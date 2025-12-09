
import json
import re
from typing import Dict, Any


class TemplateAgent:
    

    def __init__(self, block_interface):
        self.block = block_interface

    def render(self, template_def: Dict[str, Any], model: Dict[str, Any], questions=None) -> Dict[str, Any]:
        out = {}
        for field, spec in template_def.items():
            out[field] = self._process_value(spec, model, questions)
        return out

    def _process_value(self, spec: Any, model: Dict[str, Any], questions=None) -> Any:
      
        if isinstance(spec, str):
           
            if '{{' in spec and '}}' in spec:
                result = spec
                pattern = r'\{\{model\.([a-z_]+)\}\}'
                for match in re.finditer(pattern, spec):
                    key = match.group(1)
                    value = model.get(key)
                    result = result.replace(match.group(0), str(value) if value is not None else '')
                return result
     
            elif spec == 'questions' and questions is not None:
                return questions
            else:
                return spec
        elif isinstance(spec, dict):
            if spec.get('block'):

                block_name = spec['block']
                fn = getattr(self.block, block_name)
                if block_name == 'compare_ingredients_block':
                    return fn(model, spec.get('with'))
                else:
                    return fn(model)
            else:
              
                return {k: self._process_value(v, model, questions) for k, v in spec.items()}
        else:
            return spec
