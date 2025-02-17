from src.calculator import evaluate_expression 

if __name__ == "__main__":
    while True:
        expression = input("Enter expression (or 'q' to quit): ")
        if expression.lower() in ("q", "quit"):
            break

        result = evaluate_expression(expression)
        print(result)