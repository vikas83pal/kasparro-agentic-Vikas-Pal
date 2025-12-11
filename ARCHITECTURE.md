# System Architecture

This system uses **LangGraph** to orchestrate a multi-agent workflow for content generation.

## Graph Design

The workflow is a linear StateGraph processing data from raw input to final JSON outputs.

### State (`AgentState`)
- **raw_input**: Dictionary containing the initial product data.
- **product_model**: Validated internal Pydantic model (`InternalProductModel`).
- **generated_questions**: List of generated questions (`QuestionInput`).
- **product_page**: Final structured product page object.
- **comparison_page**: Final structured comparison page object.
- **faq_page**: Final structured FAQ page object.

### Nodes

1.  **`parser_node`**:
    -   **Responsibility**: Validation and Normalization.
    -   **Tools Used**: `parse_product_data`
    -   **Output**: Updates `product_model` in state.

2.  **`generation_node`**:
    -   **Responsibility**: Content Creation (Questions).
    -   **Tools Used**: `generate_questions_rule_based` (can be swapped for LLM).
    -   **Output**: Updates `generated_questions` in state.

3.  **`assembly_node`**:
    -   **Responsibility**: Page Assembly.
    -   **Tools Used**: `format_usage_section`, `format_ingredients_section`.
    -   **Output**: Updates `product_page`, `faq_page`, `comparison_page`.

## Tools (`src/tools.py`)

-   **@tool** decorators are used to define reusable logic blocks.
-   Tools are Pydantic-typed for validation and LLM compatibility.

## Data Models (`src/models.py`)

-   All data structures are defined using **Pydantic** for Type Safety and automatic JSON serialization.
