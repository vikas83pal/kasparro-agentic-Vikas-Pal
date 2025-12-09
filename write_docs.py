

import os

doc_content = """# Kasparro AI Agentic Content Generation System - Project Documentation

## Executive Summary

This document provides detailed technical specifications for the Kasparro AI Agentic Content Generation System - a production-style, end-to-end multi-agent framework for autonomously generating structured, machine-readable marketing content (FAQ, Product Page, and Comparison Page) from product JSON input.

The system demonstrates advanced software engineering principles including:
- **Modular Architecture:** Loosely-coupled agents with single responsibilities
- **Explicit Message Passing:** DAG-based orchestration with transparent data flow
- **Reusable Components:** Shared content logic blocks for consistent content generation
- **Template-Driven Design:** Configurable template engine for flexible output formatting

---

## Problem Statement

**Challenge:** Design a modular multi-agent system that autonomously produces structured, machine-readable pages from minimal product data, using clearly defined agents with explicit message-passing, reusable content logic blocks, and a custom template engine.

**Requirements:**
1. Accept product data as JSON input
2. Generate at least 15 categorized FAQ questions
3. Produce three distinct output pages: FAQ, Product Page, and Comparison Page
4. Use modular agent architecture with clear boundaries
5. Implement explicit message-passing between agents (no hidden global state)
6. Create reusable content logic blocks
7. Build custom template engine for output generation
8. Generate valid JSON outputs suitable for machine processing
9. Support extensibility for multiple products

---

## Solution Overview

The system implements a **Directed Acyclic Graph (DAG)** orchestrator that coordinates five specialized agents:

```
Input Product JSON
        ↓
   [ParserAgent]  → Normalized Product Model
        ↓
 [QuestionGenAgent] → 15+ Categorized Questions
        ↓
  [AssemblerAgent]
        ├─→ [TemplateAgent] + [BlockAgent] → FAQ JSON
        ├─→ [TemplateAgent] + [BlockAgent] → Product Page JSON
        └─→ [TemplateAgent] + [BlockAgent] → Comparison JSON
        ↓
   JSON Outputs
```

---

## System Architecture

### Agent Specifications

#### 1. ParserAgent (`src/agents/parser_agent.py`)
- Normalizes field names (lowercase, underscore-separated)
- Validates required fields
- Parses comma-separated lists
- Converts price to numeric value

#### 2. QuestionGenAgent (`src/agents/qgen_agent.py`)
- Generates 15+ categorized questions
- Categories: Informational, Usage, Safety, Purchase, Comparison, Other
- Provides answer hints based on product data

#### 3. BlockAgent (`src/agents/block_agent.py`)
- Reusable content transformation functions
- Methods: benefits_block, usage_block, safety_block, ingredients_block, compare_ingredients_block
- Pure, stateless functions

#### 4. TemplateAgent (`src/agents/template_agent.py`)
- Custom template rendering engine
- Resolves model references: {{model.field_name}}
- Invokes blocks: {"block": "method_name"}
- Processes nested structures recursively

#### 5. AssemblerAgent (`src/agents/assembler_agent.py`)
- Orchestrates page assembly
- Creates fictional product B for comparison
- Manages file I/O to src/outputs/

### Orchestrator Pattern

DAG-based message-passing orchestrator with explicit data flow:
- No hidden global state
- Clear visibility into agent interactions
- Composable and extensible

---

## Data Flow

```
RAW_PRODUCT → ParserAgent → NORMALIZED_MODEL
                                ↓
                        QuestionGenAgent → QUESTIONS
                                ↓
                        AssemblerAgent → JSON OUTPUTS
                        (invokes TemplateAgent + BlockAgent)
```

---

## Key Design Principles

1. **Single Responsibility:** Each agent has one reason to change
2. **Explicit Message-Passing:** All data flows are visible
3. **Composability:** Agents can be reused and combined
4. **Testability:** Components can be tested independently
5. **Extensibility:** Easy to add new agents/blocks/templates

---

## Output Structure

### FAQ Output
- Title with product name
- Array of 10+ questions with category and hints

### Product Page Output
- Product name, price, concentration
- Structured ingredients, benefits, usage, safety
- Full questions array

### Comparison Output
- Comparison of ingredients
- Fictional product B specification
- Set-based analysis (common, unique to A, unique to B)

---

## Running the System

```bash
# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
python -m src.main

# Test
python tests/smoke_test.py
```

---

## Extension Points

### Add New Agent
Create new agent file with run() method and register in orchestrator.

### Add New Block
Add method to BlockAgent following the pattern:
```python
def new_block(self, model: Dict[str, Any]) -> Any:
    # Transform and return
```

### Add New Template
Create JSON file in src/templates/ and register in TEMPLATES dict.

---

## Production Roadmap

1. Database storage for templates and products
2. Queue-based workers (Celery/Kafka)
3. API layer for external access
4. Enhanced error handling and logging
5. LLM integration for intelligent content
6. Multi-language support
7. Analytics and monitoring

---

## Technical Stack

- **Language:** Python 3.8+
- **Dependencies:** None (pure Python)
- **Deployment:** Docker-compatible
- **Testing:** Pytest-compatible smoke tests

---

## Success Criteria

- ✅ Generates 3 valid JSON files
- ✅ FAQ has 15+ questions
- ✅ All agents follow SRP
- ✅ Explicit message-passing throughout
- ✅ Extensible and maintainable design

---

**Version:** 1.0  
**Date:** December 9, 2025  
**Status:** Complete
"""

with open('docs/projectdocumentation.md', 'w', encoding='utf-8') as f:
    f.write(doc_content)

print('Updated projectdocumentation.md')
