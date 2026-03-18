"""Calculator module with basic arithmetic operations."""


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: float, exponent: float) -> float:
    """Calculate base raised to the power of exponent."""
    return base ** exponent


class Calculator:
    """A simple calculator class with memory."""
    
    def __init__(self):
        self.memory = 0
        self.history = []
    
    def store(self, value: float) -> None:
        """Store a value in memory."""
        self.memory = value
        self.history.append(f"stored {value}")
    
    def recall(self) -> float:
        """Recall the value from memory."""
        return self.memory
    
    def clear(self) -> None:
        """Clear the memory."""
        self.memory = 0
        self.history.append("cleared")
    
    def get_history(self) -> list:
        """Get calculation history."""
        return self.history.copy()
