from langchain_core.tools import tool

# create a tool

@tool
def multiply(a: int, b: int) -> int:
    """Returns the product of a and b."""
    return a * b

print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.tool_call_schema)
print(multiply.invoke({"a": 2, "b": 3}))
