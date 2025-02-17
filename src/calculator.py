def calculate(operator, num1, num2=None):
    """
    Performs a calculation based on the given operator and numbers.

    Args:
        operator (str): The operator to perform (e.g., "+", "-", "*", "/", "%", "^",
                       "add", "sub", "mul", "div", "mod", "pow").
        num1 (int/float): The first number.
        num2 (int/float, optional): The second number. Defaults to None.

    Raises:
        ValueError: If the input numbers or operator are invalid, or if the
                    operator requires two numbers but num2 is not provided.

    Returns:
        int/float: The result of the calculation.
    """

    if not isinstance(num1, (int, float)):
        raise ValueError(f"Invalid number \"{num1}\"")
    if num2 is not None and not isinstance(num2, (int, float)):
        raise ValueError(f"Invalid number \"{num2}\"")

    valid_operators = {"+", "-", "*", "/", "%", "^", "add", "sub", "mul", "div", "mod", "pow"}
    if operator not in valid_operators:
        raise ValueError(f"Invalid operator \"{operator}\"")

    if num2 is None:
        if operator in ("+", "add"):
            return num1
        elif operator in ("-", "sub"):
            return -num1
        else:
            raise ValueError("This operator requires two numbers")

    if operator in ("+", "add"):
        return num1 + num2
    elif operator in ("-", "sub"):
        return num1 - num2
    elif operator in ("*", "mul"):
        return num1 * num2
    elif operator in ("/", "div"):
        if num2 == 0:
            raise ValueError("Division by zero")
        return num1 / num2
    elif operator in ("%", "mod"):
        if num2 == 0:
            raise ValueError("Division by zero")
        return num1 % num2
    elif operator in ("^", "pow"):
        return num1 ** num2


def evaluate(expression):
    """
    Evaluates a mathematical expression given as a list.

    Args:
        expression (list): A list representing the mathematical expression.
                           It can contain numbers, operators, and nested lists.

    Raises:
        ValueError: If the expression is invalid or cannot be evaluated.

    Returns:
        int/float: The result of the evaluation.
    """

    if not isinstance(expression, list) or not expression:
        raise ValueError(f"Failed to evaluate \"{expression}\"")

    for i, item in enumerate(expression):
        if isinstance(item, list):
            try:
                expression[i] = evaluate(item)
            except ValueError as e:
                raise ValueError(str(e))

    if len(expression) == 1:
        return expression[0]

    try:
        operator = expression[0]
        if len(expression) == 2:
            return calculate(operator, expression[1])
        elif len(expression) == 3:
            return calculate(operator, expression[1], expression[2])
        else:
            raise ValueError(f"Failed to evaluate \"{expression}\"")
    except ValueError as e:
        raise ValueError(str(e))


def structure(expression):
    """
    Structures a mathematical expression given as a list, respecting operator precedence.

    Args:
        expression (list): A list representing the mathematical expression.

    Raises:
        ValueError: If the expression is invalid or cannot be structured.

    Returns:
        list: The structured expression as a nested list.
    """
    if not expression:
        return []
    if not isinstance(expression, list):
        raise ValueError(f"Failed to structure \"{expression}\"")
    if len(expression) < 2:  # Changed to < 2 to handle single-item lists after parsing
        raise ValueError(f"Failed to structure \"{expression}\"")

    num_operators = sum(1 for item in expression if isinstance(item, str))
    num_operands = len(expression) - num_operators

    if abs(num_operators - num_operands) > 1 or num_operators - num_operands == 0:
        raise ValueError(f"Failed to structure \"{expression}\"")

    level0_ops = {"^", "pow"}
    level1_ops = {"*", "/", "%", "mul", "div", "mod"}
    level2_ops = {"+", "-", "add", "sub"}

    def parse_expression(expression, operators, right_associative=False):
        i = len(expression) - 2 if right_associative else 1
        step = -2 if right_associative else 2

        while 0 < i < len(expression) - 1 if not right_associative else i >= 1:
            if isinstance(expression[i], str) and expression[i] in operators:
                left = expression[i - 1]
                op = expression[i]
                right = expression[i + 1]
                new_expression = expression[:i - 1] + [[op, left, right]] + expression[i + 2:]
                return parse_expression(new_expression, operators, right_associative)
            i += step
        return expression[0] if len(expression) == 1 else expression

    expression = parse_expression(expression, level0_ops, right_associative=True)
    for ops in [level1_ops, level2_ops]:
        if isinstance(expression, list):
            expression = parse_expression(expression, ops)

    # Handle invalid operators after initial parsing
    while isinstance(expression, list):
        invalid_ops = [
            i
            for i, item in enumerate(expression)
            if isinstance(item, str)
            and item not in level0_ops.union(level1_ops).union(level2_ops)
        ]

        if not invalid_ops:
            break

        i = min(invalid_ops)
        left = expression[i - 1]
        op = expression[i]
        right = expression[i + 1]
        expression = expression[:i - 1] + [[op, left, right]] + expression[i + 2:]

    return expression[0] if isinstance(expression, list) and len(expression) == 1 else expression

def get_next_token(expression_string, start_index):
    """
    Extracts the next token (operator or number) from the expression string.

    Args:
        expression_string (str): The mathematical expression string.
        start_index (int): The starting index for token extraction.

    Raises:
        ValueError: If the end of the string is reached or an invalid 
                    operator/number is found.

    Returns:
        str/int/float: The next token (operator or number).
    """

    if not expression_string or start_index >= len(expression_string):
        raise ValueError("End of string")

    expression_string = expression_string.replace(" ", "")  # Remove all spaces

    char = expression_string[start_index]

    if char.isalpha():  # Operator (e.g., "add", "sub")
        index = start_index
        operator = ""
        while index < len(expression_string) and expression_string[index].isalpha():
            operator += expression_string[index]
            index += 1

        # Consume any non-alphanumeric characters immediately following the operator
        while (
            index < len(expression_string)
            and not expression_string[index].isalnum()
            and expression_string[index] not in ("(", ")")
        ):
            operator += expression_string[index]
            index += 1

        valid_operators = {"add", "sub", "mul", "div", "mod", "pow"}
        if operator not in valid_operators:
            raise ValueError(f"Invalid operator \"{operator}\"")
        return operator

    if not char.isdigit() and not char.isalpha():  # Special symbol or invalid operator
        if char in {"+", "-", "*", "/", "%", "^", "(", ")"}:
            return char  # Valid operator or parenthesis
        else:
            index = start_index
            while (
                index < len(expression_string)
                and not expression_string[index].isalnum()
                and expression_string[index] not in ("(", ")")
            ):
                index += 1
            raise ValueError(f"Invalid operator \"{expression_string[start_index:index]}\"")

    index = start_index  # Number (integer or float)
    number = ""

    if char == "-":  # Handle negative numbers
        number += "-"
        index += 1

    while (
        index < len(expression_string)
        and (expression_string[index].isdigit() or expression_string[index] == ".")
    ):
        number += expression_string[index]
        index += 1

    try:
        return float(number) if "." in number else int(number)
    except ValueError:
        raise ValueError(f"Invalid number \"{number}\"")

def parse(expression_string):
    """
    Parses a mathematical expression string into a structured list.

    Args:
        expression_string (str): The mathematical expression string.

    Raises:
        ValueError: If the expression is invalid or contains unmatched parentheses.

    Returns:
        list: The structured expression as a nested list.
    """

    expression_string = expression_string.replace(" ", "")  # Remove spaces
    tokens = []

    while expression_string:
        try:
            next_token = get_next_token(expression_string, 0)
        except ValueError as e:
            raise ValueError(str(e))

        if next_token == ")":
            expression_string = expression_string.replace(")", "", 1)
            continue
        elif next_token == "(":
            paren_count = 1
            paren_index = 1

            while paren_count > 0 and paren_index < len(expression_string):
                if expression_string[paren_index] == "(":
                    paren_count += 1
                elif expression_string[paren_index] == ")":
                    paren_count -= 1
                paren_index += 1

            if paren_count > 0:
                raise ValueError("Unmatched parenthesis")

            next_token = parse(expression_string[1:paren_index - 1])
            expression_string = expression_string[paren_index - 1:].replace(")", "", 1)

        expression_string = expression_string.replace(str(next_token), "", 1)
        tokens.append(next_token)

    return structure(tokens)


def pre_parse(expression_string):
    """
    Checks for matching parentheses in the expression string.

    Args:
        expression_string (str): The mathematical expression string.

    Raises:
        ValueError: If parentheses are unmatched.
    """
    parentheses = [char for char in expression_string if char in ("(", ")")]
    open_paren_count = 0

    for char in parentheses:
        if open_paren_count < 0:
            raise ValueError("Unmatched parenthesis")
        if char == "(":
            open_paren_count += 1
        elif char == ")":
            open_paren_count -= 1

    if open_paren_count != 0:
        raise ValueError("Unmatched parenthesis")


def evaluate_expression(expression_string):
    """
    Evaluates a mathematical expression string.

    Args:
        expression_string (str): The mathematical expression string.

    Returns:
        int/float/str: The result of the evaluation or an error message.
    """
    try:
        pre_parse(expression_string)
        result = evaluate(parse(expression_string))
        return result
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    while True:
        expression = input("Enter expression (or 'q' to quit): ")
        if expression.lower() in ("q", "quit"):
            break

        result = evaluate_expression(expression)
        print(result)