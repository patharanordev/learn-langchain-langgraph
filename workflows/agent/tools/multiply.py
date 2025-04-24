from langchain_core.tools import tool

@tool
def multiply(a:int, b:int) -> int:
    """Multiply a and b"""
    return a * b
