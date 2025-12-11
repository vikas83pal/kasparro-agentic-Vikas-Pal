# Kasparro AI Agentic Content Generation System

> **Built with LangChain** - A production-style multi-agent content generation system

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-✓-green.svg)](https://langchain.com)

---

## 📋 What's Implemented

This project demonstrates a **LangChain-based multi-agent system** with:

| Requirement | Implementation |
|-------------|----------------|
| **Real agent components** | 5 Agent classes with clear responsibilities |
| **LangChain orchestration** | `RunnableSequence` chain composition |
| **Model/tool calls** | `@tool` decorated functions |
| **Reusable logic blocks** | 7 tools in `tools.py` |
| **Templates** | JSON definitions in `templates/` |
| **JSON output** | 3 structured output files |
| **Architecture doc** | `docs/projectdocumentation.md` |

---

## 🏗️ Project Structure

```
kasparro-agentic-Vikas-Pal/
│
├── README.md
├── requirements.txt
├── Dockerfile
├── .gitignore
│
├── docs/
│   └── projectdocumentation.md    # System design & architecture
│
├──  src/
│   ├── __init__.py
│   ├── main.py                    # Entry point
│   ├── orchestrator.py            # LangChain RunnableSequence
│   ├── agents.py                  # 5 Agent components
│   ├── tools.py                   # 7 @tool functions
│   ├── models.py                  # Pydantic models
│   │
│   ├── templates/
│   │   ├── faq_template.json
│   │   ├── product_template.json
│   │   └── comparison_template.json
│   │
│   └── outputs/
│       ├── faq.json
│       ├── product_page.json
│       └── comparison_page.json
│
└── tests/
    └── smoke_test.py
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kasparro-agentic-Vikas-Pal.git
cd kasparro-agentic-Vikas-Pal

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python -m src.main
```

### Expected Output

```
============================================================
Kasparro AI Content Generation System
LangChain Multi-Agent Pipeline
============================================================

[1/4] Initializing LangChain orchestrator...
[2/4] Executing agent workflow...
      → ParserAgent: Normalizing input data
      → QuestionGeneratorAgent: Generating questions
      → ContentBlockAgent: Creating content blocks
      → ComparisonAgent: Building comparison
      → AssemblyAgent: Assembling pages
[3/4] Extracting outputs...
[4/4] Writing JSON outputs...

============================================================
SUCCESS! Generated files:
   • faq.json
   • product_page.json
   • comparison_page.json
============================================================
```

---

## 🧠 Architecture

### Agent Workflow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Parser    │───▶│  Question   │───▶│  Content    │
│   Agent     │    │  Generator  │    │   Blocks    │
└─────────────┘    └─────────────┘    └─────────────┘
                                            │
                   ┌────────────────────────┘
                   ▼
           ┌─────────────┐    ┌─────────────┐
           │ Comparison  │───▶│  Assembly   │───▶ JSON Outputs
           │   Agent     │    │   Agent     │
           └─────────────┘    └─────────────┘
```

### Agent Responsibilities

| Agent | Class | Tools | Output |
|-------|-------|-------|--------|
| **Parser** | `ParserAgent` | `parse_product_data` | `InternalProductModel` |
| **Question Generator** | `QuestionGeneratorAgent` | `generate_questions` | 16 Q&As |
| **Content Blocks** | `ContentBlockAgent` | 4 block tools | `Dict[str, Any]` |
| **Comparison** | `ComparisonAgent` | `generate_comparison_block` | Comparison data |
| **Assembly** | `AssemblyAgent` | - | 3 JSON pages |

### LangChain Components

- **`@tool`** - Wraps logic blocks as LangChain tools
- **`RunnableLambda`** - Wraps agent execution
- **`RunnableSequence`** - Chains agents (pipe `|` operator)
- **`Pydantic BaseModel`** - Type-safe models with JSON serialization

---

## 📤 Output Examples

### faq.json
```json
{
  "title": "FAQ - GlowBoost Vitamin C Serum",
  "questions": [
    {
      "question": "What is GlowBoost Vitamin C Serum?",
      "category": "Informational",
      "answer_hint": "..."
    }
  ]
}
```

### product_page.json
```json
{
  "name": "GlowBoost Vitamin C Serum",
  "price": 699.0,
  "ingredients": [...],
  "benefits": { "summary": "...", "bullets": [...] },
  "usage": { "instructions": "...", "dosage": "..." },
  "safety": { "side_effects": "...", "warnings": [...] }
}
```

### comparison_page.json
```json
{
  "title": "Product Comparison",
  "product_a": { ... },
  "product_b": { ... },
  "comparison": {
    "common_ingredients": [...],
    "unique_to_a": [...],
    "unique_to_b": [...]
  }
}
```

---

##  Documentation

See [`docs/projectdocumentation.md`](docs/projectdocumentation.md) for complete system design.

---

## 👤 Author

**Vikas Pal**

Built for the Kasparro Applied AI Engineer assignment.
