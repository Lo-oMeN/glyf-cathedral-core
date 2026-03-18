"""Tests for calculator.py"""

import pytest
from calculator import add, subtract, multiply, divide, power, Calculator


def test_add():
    """Test add function."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    """Test subtract function."""
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
    assert subtract(0, 5) == -5


def test_multiply():
    """Test multiply function."""
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0


def test_divide():
    """Test divide function."""
    assert divide(6, 2) == 3
    assert divide(5, 2) == 2.5
    
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)


def test_power():
    """Test power function."""
    assert power(2, 3) == 8
    assert power(5, 0) == 1
    assert power(2, -1) == 0.5


class TestCalculator:
    """Tests for Calculator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()
    
    def test_store_and_recall(self):
        """Test store and recall methods."""
        self.calc.store(42)
        assert self.calc.recall() == 42
    
    def test_clear(self):
        """Test clear method."""
        self.calc.store(42)
        self.calc.clear()
        assert self.calc.recall() == 0
    
    def test_get_history(self):
        """Test get_history method."""
        self.calc.store(10)
        self.calc.clear()
        history = self.calc.get_history()
        assert len(history) == 2
        assert "stored 10" in history
