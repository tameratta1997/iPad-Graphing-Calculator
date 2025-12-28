#!/usr/bin/env python3
"""Simple Calculator Program"""

try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    operation = input("Enter operation (+, -, *, /, **, %): ").strip()
    
    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else "Error: Cannot divide by zero!",
        '**': lambda a, b: a ** b,
        '%': lambda a, b: a % b if b != 0 else "Error: Cannot perform modulo with zero!"
    }
    
    if operation in operations:
        result = operations[operation](num1, num2)
        print(f"\nResult: {result}")
    else:
        print(f"Error: Invalid operation '{operation}'")

except ValueError:
    print("Error: Please enter valid numbers")
