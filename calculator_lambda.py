import json
import operator
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

def calculator(event, __):
    logger.debug(f"Received Event: {event}")
    result = None
    error = None
    data = None
    
    message = event.get("Records")[0].get("Sns").get("Message")

    data = json.loads(message)

    if data["operation"] not in OPERATORS:
        raise ValueError(f"Invalid operation '{data.get('operation')}'")

    try:
        result = OPERATORS[data["operation"]](data["op1"], data["op2"])
    except ZeroDivisionError:
        error = "Error: Division by zero"

    if error:
        logger.error(error)
    else:
        logger.info(f"Result: {result}")

    return result