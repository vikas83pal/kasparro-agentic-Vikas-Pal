# Project Documentation

## Problem Statement

Design and implement a **modular agentic automation system** that takes a product dataset and automatically generates structured, machine-readable content pages (FAQ, Product Page, Comparison Page).

## Solution Overview

This solution implements a **LangChain-based multi-agent system** with:

- **5 Real Agent Components** with clear responsibilities
- **LangChain RunnableSequence** for orchestration
- **@tool decorated functions** for reusable logic blocks
- **Pydantic models** for type-safe JSON output
- **Template definitions** for page structure

## Scopes & Assumptions

### In Scope
- Single product processing (GlowBoost Vitamin C Serum)
- 3 output pages: FAQ, Product, Comparison
- 16 categorized questions
- Fictional Product B for comparison

### Assumptions
- No external API calls required
- Rule-based content generation (LLM-ready architecture)
- All content derived from provided product data

## System Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    LANGCHAIN ORCHESTRATOR                       │
│                  (RunnableSequence Chain)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   RAW INPUT                                                     │
│       │                                                         │
│       ▼                                                         │
│   ┌─────────────────┐                                          │
│   │  PARSER AGENT   │  → Tool: parse_product_data              │
│   │  (Agent 1)      │  → Output: InternalProductModel          │
│   └────────┬────────┘                                          │
│            │                                                    │
│            ▼                                                    │
│   ┌─────────────────────────────────────────────────────┐      │
│   │              PARALLEL GENERATION                     │      │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │      │
│   │  │  QUESTION   │ │  CONTENT    │ │ COMPARISON  │   │      │
│   │  │  GENERATOR  │ │   BLOCK     │ │   AGENT     │   │      │
│   │  │  (Agent 2)  │ │  (Agent 3)  │ │  (Agent 4)  │   │      │
│   │  └─────────────┘ └─────────────┘ └─────────────┘   │      │
│   └─────────────────────┬───────────────────────────────┘      │
│                         │                                       │
│                         ▼                                       │
│   ┌─────────────────┐                                          │
│   │ ASSEMBLY AGENT  │  → Combines all outputs                  │
│   │    (Agent 5)    │  → Creates final JSON pages              │
│   └────────┬────────┘                                          │
│            │                                                    │
│            ▼                                                    │
│   ┌─────────────────────────────────────────────────────┐      │
│   │                    OUTPUTS                           │      │
│   │   faq.json    product_page.json    comparison.json  │      │
│   └─────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Components

| Agent | Class | Responsibility | Tools Used |
|-------|-------|----------------|------------|
| **Agent 1** | `ParserAgent` | Normalize raw input | `parse_product_data` |
| **Agent 2** | `QuestionGeneratorAgent` | Generate 16 Q&As | `generate_questions` |
| **Agent 3** | `ContentBlockAgent` | Create content blocks | 4 block tools |
| **Agent 4** | `ComparisonAgent` | Compare products | `generate_comparison_block` |
| **Agent 5** | `AssemblyAgent` | Assemble JSON pages | Composition |

### LangChain Components Used

| Component | Purpose |
|-----------|---------|
| `@tool` decorator | Define reusable logic blocks |
| `RunnableLambda` | Wrap agent execution |
| `RunnableSequence` | Chain agents together |
| `Pydantic BaseModel` | Type-safe data models |

### Tools (Reusable Logic Blocks)

| Tool | File | Purpose |
|------|------|---------|
| `parse_product_data` | `tools.py` | Normalize keys, parse lists |
| `generate_questions` | `tools.py` | Create 16 categorized questions |
| `generate_benefits_block` | `tools.py` | Benefits summary + bullets |
| `generate_usage_block` | `tools.py` | Usage instructions |
| `generate_safety_block` | `tools.py` | Safety warnings |
| `generate_ingredients_block` | `tools.py` | Ingredient classification |
| `generate_comparison_block` | `tools.py` | Product comparison |

### Data Flow

```
Raw JSON → ParserAgent → InternalProductModel
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         Questions      ContentBlocks    Comparison
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                       AssemblyAgent
                              │
                              ▼
                    3 JSON Output Files
```

### Output Structure

All outputs are fully JSON-structured:

1. **faq.json**: `{ title, questions[] }`
2. **product_page.json**: `{ name, price, ingredients[], benefits{}, usage{}, safety{}, questions[] }`
3. **comparison_page.json**: `{ title, product_a{}, product_b{}, comparison{} }`
