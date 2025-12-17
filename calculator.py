import math

def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Returns the difference of two numbers."""
    return a - b

def multiply(a, b):
    """Returns the product of two numbers."""
    return a * b

def divide(a, b):
    """Returns the division of two numbers. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a, b):
    """Returns a raised to the power of b."""
    return math.pow(a, b)

def sqrt(a):
    """Returns the square root of a."""
    if a < 0:
        raise ValueError("Cannot take square root of negative number")
    return math.sqrt(a)

def sin(a):
    """Returns the sine of a (in radians)."""
    return math.sin(a)

def cos(a):
    """Returns the cosine of a (in radians)."""
    return math.cos(a)

def tan(a):
    """Returns the tangent of a (in radians)."""
    return math.tan(a)

def log(a):
    """Returns the natural logarithm of a."""
    if a <= 0:
        raise ValueError("Cannot take log of non-positive number")
    return math.log(a)

def get_number(prompt):
    """Helper to get a valid number from user input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    print("Simple Calculator")
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("Q. Quit")

    while True:
        choice = input("\nEnter choice (1/2/3/4 or Q): ").upper()

        if choice == 'Q':
            print("Exiting calculator. Goodbye!")
            break

        if choice in ('1', '2', '3', '4'):
            num1 = get_number("Enter first number: ")
            num2 = get_number("Enter second number: ")

            try:
                if choice == '1':
                    print(f"{num1} + {num2} = {add(num1, num2)}")
                elif choice == '2':
                    print(f"{num1} - {num2} = {subtract(num1, num2)}")
                elif choice == '3':
                    print(f"{num1} * {num2} = {multiply(num1, num2)}")
                elif choice == '4':
                    result = divide(num1, num2)
                    print(f"{num1} / {num2} = {result}")
            except ValueError as e:
                print(f"Error: {e}")
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()

def bitwise_and(a, b):
    """Returns the bitwise AND of two integers."""
    return int(a) & int(b)

def bitwise_or(a, b):
    """Returns the bitwise OR of two integers."""
    return int(a) | int(b)

def bitwise_xor(a, b):
    """Returns the bitwise XOR of two integers."""
    return int(a) ^ int(b)

def bitwise_not(a):
    """Returns the bitwise NOT of an integer."""
    return ~int(a)

def left_shift(a, b):
    """Returns a left shifted by b bits."""
    return int(a) << int(b)

def right_shift(a, b):
    """Returns a right shifted by b bits."""
    return int(a) >> int(b)
