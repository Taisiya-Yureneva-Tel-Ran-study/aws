import json

OPERATORS = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y
}

def calculator(event, context):
    result = None
    error = None
    data = None
    
    message = event.get("Records")[0].get("Sns").get("Message")

    try:
        data = json.loads(message)
    except (json.JSONDecodeError, TypeError):
        error = "Error: Invalid JSON format"

    # Validate fields
    error = error or ("op1" not in data and "Error: Missing operand 'op1'")
    error = error or ("op2" not in data and "Error: Missing operand 'op2'")
    error = error or ("operator" not in data and "Error: Missing 'operator'")

    # Validate operands are numbers
    error = error or (not isinstance(data.get("op1"), (int, float)) and
                      f"Error: 'op1' is not a number")
    error = error or (not isinstance(data.get("op2"), (int, float)) and
                      f"Error: 'op2' is not a number")

    error = error or (data.get("operator") not in OPERATORS and
                      f"Error: Invalid operator '{data.get('operator')}'")

    if not error:
        try:
            result = OPERATORS[data["operator"]](data["op1"], data["op2"])
        except ZeroDivisionError:
            error = "Error: Division by zero"

    print(error if error else result)

    return result