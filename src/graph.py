"""
LangGraph Definition
Orchestration graph that coordinates the multi-agent workflow.
"""
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes import (
    parser_node, 
    question_generator_node, 
    content_blocks_node,
    assembly_node
)

def create_graph():
    """
    Creates and compiles the content generation workflow.
    
    Graph Structure:
    ┌─────────────┐
    │   START     │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │   Parser    │  → Normalize input data
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Question   │  → Generate 15+ questions
    │  Generator  │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Content    │  → Generate reusable blocks
    │   Blocks    │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Assembler  │  → Build final pages
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │    END      │
    └─────────────┘
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes with clear responsibilities
    workflow.add_node("parser", parser_node)
    workflow.add_node("question_generator", question_generator_node)
    workflow.add_node("content_blocks", content_blocks_node)
    workflow.add_node("assembler", assembly_node)
    
    # Define edges (linear DAG)
    workflow.set_entry_point("parser")
    workflow.add_edge("parser", "question_generator")
    workflow.add_edge("question_generator", "content_blocks")
    workflow.add_edge("content_blocks", "assembler")
    workflow.add_edge("assembler", END)
    
    return workflow.compile()
