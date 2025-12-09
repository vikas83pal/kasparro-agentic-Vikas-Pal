# Kasparro AI Agentic Content Generation System

A production-style, end-to-end agentic content generation system built to satisfy the Kasparro Applied AI Engineer assignment.

This repository demonstrates a modular multi-agent architecture that autonomously produces structured, machine-readable pages (FAQ, Product Page, and Comparison Page) from a product JSON input.

## Repository Layout

```
kasparro-ai-agentic-content-generation-system-Hacker/
├── README.md
├── docs/
│   └── projectdocumentation.md
├── src/
│   ├── __init__.py
│   ├── main.py                # entrypoint / orchestrator runner
│   ├── orchestrator.py        # orchestrator (DAG + message passing)
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── parser_agent.py    # parse & internal model
│   │   ├── qgen_agent.py      # question generation (>=15 Qs)
│   │   ├── block_agent.py     # reusable content logic blocks
│   │   ├── template_agent.py  # template engine + renderers
│   │   └── assembler_agent.py # page assembly agents
│   ├── templates/
│   │   ├── faq_template.json
│   │   ├── product_template.json
│   │   └── comparison_template.json
│   └── outputs/
│       ├── faq.json
│       ├── product_page.json
│       └── comparison_page.json
├── tests/
│   └── smoke_test.py
├── requirements.txt
├── Dockerfile
└── setup_files.py            # (internal setup helper)
```

## Quick Start

### Prerequisites
- Python 3.8+
- No external dependencies required (pure Python implementation)

### Installation & Running Locally

1. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the pipeline:**
   ```bash
   python -m src.main
   ```

The pipeline will produce three JSON outputs:
- `src/outputs/faq.json` - Frequently asked questions
- `src/outputs/product_page.json` - Complete product page
- `src/outputs/comparison_page.json` - Product comparison with fictional competitor

## How It Works

### System Architecture

The system implements a lightweight agent framework in Python where:

- **Each agent** is a single-responsibility class with `run(input)` → `output` contract
- **Agents are wired in a DAG** by an `Orchestrator` which feeds outputs explicitly (no hidden global state)
- **Reusable content logic blocks** are Python functions centralized in `block_agent.py`
- **Template engine** (custom implementation) resolves blocks and outputs final JSON

### Agent Responsibilities

#### 1. **ParserAgent** (`parser_agent.py`)
Normalizes and validates product input.

**Input:** Raw product dictionary
**Output:** Normalized internal product model with:
- Lowercased, space-normalized keys
- Validated required fields
- Parsed lists (ingredients, skin types)
- Numeric price conversion

#### 2. **QuestionGenAgent** (`qgen_agent.py`)
Generates at least 15 categorized user questions using rule-based templates.

**Input:** Internal product model
**Output:** List of questions with:
- `question`: The question text
- `category`: Category (Informational, Usage, Safety, Purchase, Comparison, Other)
- `answer_hint`: Suggested answer or relevant product data

#### 3. **BlockAgent** (`block_agent.py`)
Collection of reusable transformation functions for content generation.

**Methods:**
- `benefits_block()` - Structured benefits with bullets
- `usage_block()` - Usage instructions with dosage/timing
- `safety_block()` - Safety info and warnings
- `ingredients_block()` - Ingredient list with role classification
- `compare_ingredients_block()` - Comparative analysis of two products

#### 4. **TemplateAgent** (`template_agent.py`)
Simple template engine that:
1. Resolves model references (e.g., `{{model.price}}`)
2. Calls BlockAgent for dynamic blocks
3. Assembles final JSON output

#### 5. **AssemblerAgent** (`assembler_agent.py`)
High-level orchestration that:
1. Invokes TemplateAgent for each required page
2. Manages output file writing
3. Creates fictional product B for comparisons
4. Collects and returns all outputs

### Orchestration Graph

```
Raw Product 
    ↓
[ParserAgent] → ProductModel
    ↓
[QuestionGenAgent] → Questions
    ↓
[AssemblerAgent] → [TemplateAgent + BlockAgent calls] → JSON Outputs
```

### Template Engine Design

Templates are JSON objects with field definitions:

```json
{
  "field_name": "static value or {{model.key}} or {\"block\": \"block_name\"}"
}
```

- **Static values:** Used as-is
- **Model references:** `{{model.field_name}}` resolves to model values
- **Block calls:** `{"block": "method_name"}` invokes BlockAgent methods
- **Questions field:** Automatically populated with question list

## Example Usage

### Input Product
```json
{
  "Product Name": "GlowBoost Vitamin C Serum",
  "Concentration": "10% Vitamin C",
  "Skin Type": "Oily, Combination",
  "Key Ingredients": "Vitamin C, Hyaluronic Acid",
  "Benefits": "Brightening, Fades dark spots",
  "How to Use": "Apply 2–3 drops in the morning before sunscreen",
  "Side Effects": "Mild tingling for sensitive skin",
  "Price": "₹699"
}
```

### Output Examples

#### FAQ Output (`faq.json`)
```json
{
  "title": "FAQ - GlowBoost Vitamin C Serum",
  "questions": [
    {
      "question": "What is GlowBoost Vitamin C Serum?",
      "category": "Informational",
      "answer_hint": "GlowBoost Vitamin C Serum with 10% Vitamin C."
    },
    // ... more questions
  ]
}
```

#### Product Page Output (`product_page.json`)
```json
{
  "name": "GlowBoost Vitamin C Serum",
  "price": 699.0,
  "concentration": "10% Vitamin C",
  "ingredients": [
    {"ingredient": "Vitamin C", "role": "active"},
    {"ingredient": "Hyaluronic Acid", "role": "active"}
  ],
  "benefits": {
    "summary": "Provides Brightening, Fades dark spots.",
    "bullets": ["Brightening", "Fades dark spots"]
  },
  "usage": {
    "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
    "dosage": "2-3 drops",
    "timing": "Morning before sunscreen"
  },
  "safety": {
    "side_effects": "Mild tingling for sensitive skin",
    "warnings": ["Patch test before use"]
  },
  "questions": [ /* questions array */ ]
}
```

#### Comparison Output (`comparison_page.json`)
```json
{
  "title": "Comparison",
  "compare": {
    "common": ["vitamin c"],
    "only_a": ["hyaluronic acid"],
    "only_b": ["niacinamide"]
  },
  "product_b": {
    "product_name": "RadiantBlend Vitamin C Concentrate",
    "concentration": "12% Vitamin C",
    "key_ingredients": ["Vitamin C", "Niacinamide"],
    "benefits": "Brightening, Hydration",
    "price": 899.0
  }
}
```

## Docker Support

### Build the container:
```bash
docker build -t kasparro-ai-content-gen .
```

### Run the container:
```bash
docker run --rm -v $(pwd)/src/outputs:/app/src/outputs kasparro-ai-content-gen
```

## Testing

Run the smoke test to verify the orchestrator functionality:

```bash
python -m pytest tests/smoke_test.py -v
```

Or directly:
```bash
python tests/smoke_test.py
```

The smoke test verifies:
- Orchestrator produces all three JSON outputs
- Each output has the required structure and fields
- Questions are properly generated
- Product and comparison data are assembled correctly

## Design Principles

### Modularity
- Each agent has a single responsibility
- Agents are loosely coupled via explicit message passing
- Easy to replace or extend individual agents

### Explicitness
- No hidden global state
- Clear data flow through DAG
- Template definitions are transparent

### Extensibility
- New agents can be added to the DAG
- New blocks can be added to BlockAgent
- Templates are configurable
- Easy to support multiple products

### Simplicity
- No external framework dependencies
- Pure Python implementation
- Minimal overhead, maximum clarity

## Scopes & Assumptions

- **Input:** Single product dataset (GlowBoost Vitamin C Serum) with predefined schema
- **Data Enrichment:** No external web calls; all content derived from provided fields
- **Product B:** Fictional product constructed locally for comparisons
- **Extensibility:** System designed to support multiple products by replacing input JSON

## Production Considerations & Next Steps

1. **Replace inline templates** with a templating store and versioned templates
2. **Add queue-based workers** (Celery, Kafka) to scale agents and enable async processing
3. **Implement logging & telemetry** for observability and debugging
4. **Add type validation** with Pydantic for stricter schemas
5. **Implement retry logic** and comprehensive error handling
6. **Add unit tests** for each agent and integration tests for the orchestrator
7. **Add database support** to store generated content and track lineage
8. **Implement caching** to avoid regenerating content
9. **Add API layer** for external access (FastAPI/Flask)
10. **Add monitoring & alerts** for production deployments

## Architecture Decisions

### Why a Custom Template Engine?
- Demonstrates understanding of templating concepts
- Lightweight and transparent
- Easy to extend for custom block interactions
- Shows control over the content generation flow

### Why No External Frameworks?
- Emphasizes core agent design and orchestration patterns
- Easier to understand and modify
- Pure Python keeps system portable
- Demonstrates software engineering fundamentals

### Why Explicit Message Passing?
- Clear visibility into data flow
- Easier to debug and test
- No surprising side effects from hidden state
- Aligns with functional programming principles

## File Structure Explanation

| File | Purpose |
|------|---------|
| `src/main.py` | Entry point; initializes agents and orchestrator |
| `src/orchestrator.py` | DAG runner; coordinates agent execution |
| `src/agents/parser_agent.py` | Normalizes raw product data |
| `src/agents/qgen_agent.py` | Generates categorized questions |
| `src/agents/block_agent.py` | Reusable content transformation functions |
| `src/agents/template_agent.py` | Template rendering engine |
| `src/agents/assembler_agent.py` | Page assembly and file writing |
| `src/templates/*.json` | Template definitions for each page type |
| `src/outputs/*.json` | Generated output files |
| `tests/smoke_test.py` | Integration test suite |

## License

MIT

## Author

Built as part of the Kasparro Applied AI Engineer assignment.

---

**Questions or Issues?** Check `docs/projectdocumentation.md` for detailed technical specifications.
