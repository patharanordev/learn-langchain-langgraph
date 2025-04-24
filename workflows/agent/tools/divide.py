from langchain_core.tools import tool

@tool
def divide(a:int, b:int) -> int:
    """Divide a and b"""
    return a / b
