import pytest
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from calculator import (
    calculate_simple_interest,
    calculate_compound_interest,
    calculate_tax
)

class TestSimpleInterest:
    def test_calculate_simple_interest_positive_values(self):
        result = calculate_simple_interest(1000, 5, 2)
        expected = 1000 * 5 * 2 / 100
        assert result == expected
        
        result = calculate_simple_interest(5000, 3.5, 4)
        expected = 5000 * 3.5 * 4 / 100
        assert result == expected
    
    def test_calculate_simple_interest_zero_values(self):
        result = calculate_simple_interest(0, 5, 2)
        assert result == 0
        
        result = calculate_simple_interest(1000, 0, 2)
        assert result == 0
        
        result = calculate_simple_interest(1000, 5, 0)
        assert result == 0
        
        result = calculate_simple_interest(0, 0, 0)
        assert result == 0
    
    def test_calculate_simple_interest_negative_values(self):
        with pytest.raises(ValueError, match="Аргументы должны быть неотрицательными"):
            calculate_simple_interest(-1000, 5, 2)
        
        with pytest.raises(ValueError, match="Аргументы должны быть неотрицательными"):
            calculate_simple_interest(1000, -5, 2)
        
        with pytest.raises(ValueError, match="Аргументы должны быть неотрицательными"):
            calculate_simple_interest(1000, 5, -2)
        
        with pytest.raises(ValueError, match="Аргументы должны быть неотрицательными"):
            calculate_simple_interest(-1000, -5, -2)


class TestCompoundInterest:
    def test_calculate_compound_interest_positive_values(self):
        result = calculate_compound_interest(1000, 5, 2, n=1)
        expected = 1000 * (1 + 5/(100*1))**(1*2) - 1000
        assert abs(result - expected) < 0.001
        
        result = calculate_compound_interest(1000, 12, 1, n=4)
        expected = 1000 * (1 + 12/(100*4))**(4*1) - 1000
        assert abs(result - expected) < 0.001
    
    def test_calculate_compound_interest_zero_values(self):
        result = calculate_compound_interest(0, 5, 2, n=1)
        assert result == 0
        
        result = calculate_compound_interest(1000, 0, 2, n=1)
        assert result == 0
        
        result = calculate_compound_interest(1000, 5, 0, n=1)
        assert result == 0
    
    def test_calculate_compound_interest_negative_values(self):
        with pytest.raises(ValueError, match="Аргументы должны быть неотрицательными"):
            calculate_compound_interest(-1000, 5, 2, n=1)
        
        with pytest.raises(ValueError, match="Аргументы должны быть неотрицательными"):
            calculate_compound_interest(1000, -5, 2, n=1)
        
        with pytest.raises(ValueError, match="Аргументы должны быть неотрицательными"):
            calculate_compound_interest(1000, 5, -2, n=1)
    
    def test_calculate_compound_interest_invalid_n(self):
        with pytest.raises(ValueError, match="n должно быть целым положительным числом"):
            calculate_compound_interest(1000, 5, 2, n=0)
        
        with pytest.raises(ValueError, match="n должно быть целым положительным числом"):
            calculate_compound_interest(1000, 5, 2, n=-1)
        
        with pytest.raises(ValueError, match="n должно быть целым положительным числом"):
            calculate_compound_interest(1000, 5, 2, n=1.5)


class TestTaxCalculator:
    def test_calculate_tax_positive_values(self):
        result = calculate_tax(1000, 20)
        expected = 1000 * 20 / 100
        assert result == expected
        
        result = calculate_tax(500, 7.5)
        expected = 500 * 7.5 / 100
        assert result == expected
    
    def test_calculate_tax_zero_values(self):
        result = calculate_tax(0, 20)
        assert result == 0
        
        result = calculate_tax(1000, 0)
        assert result == 0
    
    def test_calculate_tax_edge_cases(self):
        result = calculate_tax(1000, 100)
        assert result == 1000
        
        result = calculate_tax(1000, 0)
        assert result == 0
    
    def test_calculate_tax_invalid_tax_rate(self):
        with pytest.raises(ValueError, match="Налоговая ставка должна быть между 0 и 100"):
            calculate_tax(1000, -5)
        
        with pytest.raises(ValueError, match="Налоговая ставка должна быть между 0 и 100"):
            calculate_tax(1000, 105)