"""
Test module for LSP bridge verification.
"""


class Calculator:
    """A simple calculator class."""
    
    def __init__(self, initial_value: int = 0):
        """Initialize calculator with an initial value."""
        self.value = initial_value
    
    def add(self, x: int) -> int:
        """Add a number to the current value."""
        self.value += x
        return self.value
    
    def subtract(self, x: int) -> int:
        """Subtract a number from the current value."""
        self.value -= x
        return self.value
    
    def multiply(self, x: int) -> int:
        """Multiply the current value by a number."""
        self.value *= x
        return self.value
    
    def divide(self, x: int) -> float:
        """Divide the current value by a number."""
        if x == 0:
            raise ValueError("Cannot divide by zero")
        self.value /= x
        return self.value
    
    def get_value(self) -> int:
        """Get the current value."""
        return self.value


def create_calculator(initial: int = 0) -> Calculator:
    """Factory function to create a calculator."""
    return Calculator(initial)


def main():
    """Main function demonstrating calculator usage."""
    calc = create_calculator(10)
    
    result = calc.add(5)
    print(f"After adding 5: {result}")
    
    result = calc.subtract(3)
    print(f"After subtracting 3: {result}")
    
    result = calc.multiply(2)
    print(f"After multiplying by 2: {result}")
    
    final_value = calc.get_value()
    print(f"Final value: {final_value}")


if __name__ == "__main__":
    main()
