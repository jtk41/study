from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class CoffeeOrder:
    base: str
    size: str
    milk: str = "none"
    syrups: Tuple[str, ...] = ()
    sugar: int = 0
    iced: bool = False
    price: float = 0.0
    description: str = ""

    def __str__(self) -> str:
        return self.description if self.description else f"Coffee order: {self.price} rub"


class CoffeeOrderBuilder:
    
    BASE_PRICES = {
        "espresso": 200,
        "americano": 250, 
        "latte": 300,
        "cappuccino": 320
    }
    
    SIZE_MULTIPLIERS = {
        "small": 1.0,
        "medium": 1.2,
        "large": 1.4
    }
    
    MILK_PRICES = {
        "none": 0,
        "whole": 30,
        "skim": 30,
        "oat": 60,
        "soy": 50
    }
    
    SYRUP_PRICE = 40
    ICED_PRICE = 20
    
    MAX_SUGAR = 5
    MAX_SYRUPS = 4
    
    VALID_BASES = {"espresso", "americano", "latte", "cappuccino"}
    VALID_SIZES = {"small", "medium", "large"}
    VALID_MILKS = {"none", "whole", "skim", "oat", "soy"}
    
    def __init__(self) -> None:
        self._base: Optional[str] = None
        self._size: Optional[str] = None
        self._milk: str = "none"
        self._syrups: set[str] = set()
        self._sugar: int = 0
        self._iced: bool = False
    
    def set_base(self, base: str) -> 'CoffeeOrderBuilder':
        if base not in self.VALID_BASES:
            raise ValueError(f"Invalid base: {base}. Must be one of {list(self.VALID_BASES)}")
        self._base = base
        return self
    
    def set_size(self, size: str) -> 'CoffeeOrderBuilder':
        if size not in self.VALID_SIZES:
            raise ValueError(f"Invalid size: {size}. Must be one of {list(self.VALID_SIZES)}")
        self._size = size
        return self
    
    def set_milk(self, milk: str) -> 'CoffeeOrderBuilder':
        if milk not in self.VALID_MILKS:
            raise ValueError(f"Invalid milk: {milk}. Must be one of {list(self.VALID_MILKS)}")
        self._milk = milk
        return self
    
    def add_syrup(self, syrup: str) -> 'CoffeeOrderBuilder':
        if len(self._syrups) >= self.MAX_SYRUPS:
            raise ValueError(f"Cannot add more than {self.MAX_SYRUPS} syrups")
        self._syrups.add(syrup)
        return self
    
    def set_sugar(self, teaspoons: int) -> 'CoffeeOrderBuilder':
        if not 0 <= teaspoons <= self.MAX_SUGAR:
            raise ValueError(f"Sugar must be between 0 and {self.MAX_SUGAR}")
        self._sugar = teaspoons
        return self
    
    def set_iced(self, iced: bool = True) -> 'CoffeeOrderBuilder':
        self._iced = iced
        return self
    
    def clear_extras(self) -> 'CoffeeOrderBuilder':
        self._milk = "none"
        self._syrups.clear()
        self._sugar = 0
        self._iced = False
        return self
    
    def _calculate_price(self) -> float:
        if self._base is None or self._size is None:
            raise ValueError("Base and size are required to calculate price")
        
        base_price = self.BASE_PRICES[self._base]
        size_multiplier = self.SIZE_MULTIPLIERS[self._size]
        milk_price = self.MILK_PRICES[self._milk]
        syrup_price = len(self._syrups) * self.SYRUP_PRICE
        iced_price = self.ICED_PRICE if self._iced else 0
        
        price = base_price * size_multiplier + milk_price + syrup_price + iced_price
        return round(price, 2)
    
    def _generate_description(self) -> str:
        if self._base is None or self._size is None:
            return ""
        
        parts = [f"{self._size} {self._base}"]
        
        if self._milk != "none":
            parts.append(f"with {self._milk} milk")
        
        if self._syrups:
            syrup_list = ", ".join(self._syrups)
            parts.append(f"+{syrup_list}")
        
        if self._iced:
            parts.append("(iced)")
        
        if self._sugar > 0:
            parts.append(f"{self._sugar} tsp sugar")
        
        return " ".join(parts)
    
    def build(self) -> CoffeeOrder:
        if self._base is None:
            raise ValueError("Base is required")
        if self._size is None:
            raise ValueError("Size is required")
        
        price = self._calculate_price()
        description = self._generate_description()
        
        return CoffeeOrder(
            base=self._base,
            size=self._size,
            milk=self._milk,
            syrups=tuple(self._syrups),
            sugar=self._sugar,
            iced=self._iced,
            price=price,
            description=description
        )


if __name__ == "__main__":
    builder = CoffeeOrderBuilder()
    order1 = builder.set_base("latte").set_size("medium").set_milk("oat").add_syrup("vanilla").set_sugar(2).build()
    
    assert order1.base == "latte"
    assert order1.size == "medium"
    assert order1.milk == "oat"
    assert "vanilla" in order1.syrups
    assert order1.sugar == 2
    assert order1.price > 0
    assert "medium latte" in order1.description
    assert "oat milk" in order1.description
    assert "vanilla" in order1.description
    assert "2 tsp sugar" in order1.description
    
    order2 = builder.set_base("espresso").set_size("small").clear_extras().build()
    
    assert order2.base == "espresso"
    assert order2.size == "small"
    assert order2.milk == "none"
    assert len(order2.syrups) == 0
    assert order2.sugar == 0
    assert not order2.iced
    
    assert order1.base == "latte"
    assert order1.milk == "oat"
    assert order1.price != order2.price
    
    try:
        builder = CoffeeOrderBuilder()
        builder.set_size("medium").build()
        assert False, "Should have raised ValueError for missing base"
    except ValueError:
        pass
    
    try:
        builder = CoffeeOrderBuilder()
        builder.set_base("latte").build()
        assert False, "Should have raised ValueError for missing size"
    except ValueError:
        pass
    
    try:
        builder = CoffeeOrderBuilder()
        builder.set_base("latte").set_size("medium").set_sugar(6)
        assert False, "Should have raised ValueError for too much sugar"
    except ValueError:
        pass
    
    try:
        builder = CoffeeOrderBuilder()
        builder.set_base("latte").set_size("medium")
        for i in range(5):
            builder.add_syrup(f"syrup{i}")
        assert False, "Should have raised ValueError for too many syrups"
    except ValueError:
        pass
    
    builder = CoffeeOrderBuilder()
    order3 = builder.set_base("americano").set_size("large").add_syrup("caramel").add_syrup("caramel").build()
    assert len(order3.syrups) == 1
    price_with_one_syrup = order3.price
    
    builder.clear_extras()
    order4 = builder.set_base("americano").set_size("large").add_syrup("caramel").build()
    assert len(order4.syrups) == 1
    assert order4.price == price_with_one_syrup
    
    builder = CoffeeOrderBuilder()
    order_no_ice = builder.set_base("cappuccino").set_size("small").build()
    
    builder.clear_extras()
    order_with_ice = builder.set_base("cappuccino").set_size("small").set_iced(True).build()
    
    assert order_with_ice.price == order_no_ice.price + CoffeeOrderBuilder.ICED_PRICE
    assert order_with_ice.iced
    assert not order_no_ice.iced
    
    builder = CoffeeOrderBuilder()
    simple_order = builder.set_base("espresso").set_size("small").build()
    assert "small espresso" in simple_order.description
    assert "milk" not in simple_order.description
    assert "sugar" not in simple_order.description
    assert "iced" not in simple_order.description
    
    assert str(simple_order) == simple_order.description
    
    print("All tests passed!")
