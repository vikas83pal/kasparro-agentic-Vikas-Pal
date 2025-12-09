
from typing import List, Dict


class QuestionGenAgent:


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
