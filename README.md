# Mathematical Calculator in Python

This project implements a mathematical calculator capable of evaluating complex mathematical expressions, including parentheses, operator precedence, and custom functions.

## Code Description

The code is organized into several key functions:

### 1. `calculate(operator, num1, num2=None)`

Performs basic arithmetic operations (+, -, *, /, %, ^) and named operations ("add", "sub", "mul", "div", "mod", "pow"). Accepts one or two numbers as input, depending on the operator.

### 2. `evaluate(expression)`

Evaluates a mathematical expression given as a list. This list can contain numbers, operators, and nested lists (to represent parentheses). The `evaluate` function handles recursion to resolve nested expressions.

### 3. `structure(expression)`

Structures a mathematical expression given as a list, respecting operator precedence. This function utilizes helper functions to parse the expression and identify operators at different precedence levels.

### 4. `get_next_token(expression_string, start_index)`

Parses a mathematical expression string and extracts the next token (operator or number). This function handles whitespace, numbers (integers and decimals), operators, and parentheses.

### 5. `parse(expression_string)`

Converts a mathematical expression string into a structured list of tokens, using the `get_next_token` and `structure` functions. This list is ready to be evaluated by the `evaluate` function.

### 6. `pre_parse(expression_string)`

Performs a pre-analysis of the expression string to check for unmatched parentheses.

### 7. `evaluate_expression(expression_string)`

Main function that orchestrates the entire evaluation process. It calls `pre_parse`, `parse`, and `evaluate` to obtain the final result. It also handles exceptions and returns formatted error messages.

## How to use

1.  Save the code in a file named `calculator.py` (or any name you prefer) in the `src` folder of your project.
2.  Run the script from the command line: `python calculator.py`
3.  Enter mathematical expressions when prompted. You can use numbers, operators (+, -, *, /, %, ^), parentheses, and named functions (add, sub, mul, div, mod, pow).
4.  To exit, type 'q' or 'quit'.
