from dataclasses import dataclass

@dataclass
class FinancialProduct:
    name: str
    _price: float
    _quantity: int
    description: str

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = int(value)

    @property
    def attributes(self):
        """Return attribute metadata in format {DisplayName: (value, type, default)}"""
        return {
            "Name": (self.name, str, ""),
            "Price": (self.price, float, 0.0),
            "Quantity": (self.quantity, int, 0),
            "Description": (self.description, str, ""),
            "Total": (self.price * self.quantity, float, 0.0)
        }

    @property
    def attribute_dependencies(self):
        """Return attribute dependencies {field: [dependent_fields]}"""
        return {
            "Price": ["Total"],
            "Quantity": ["Total"]
        }

@dataclass
class Option(FinancialProduct):
    _strike_price: float
    _expiration: str  # In real usage, use datetime.date
    _volatility: float

    @property
    def strike_price(self) -> float:
        return self._strike_price

    @strike_price.setter
    def strike_price(self, value: float):
        if value < 0:
            raise ValueError("Strike price cannot be negative")
        self._strike_price = value

    @property
    def expiration(self) -> str:
        return self._expiration

    @expiration.setter
    def expiration(self, value: str):
        # Simple validation for demonstration
        if not value:
            raise ValueError("Expiration date cannot be empty")
        self._expiration = value

    @property
    def attributes(self):
        base = super().attributes
        return {
            **base,
            "Strike Price": (self.strike_price, float, 0.0),
            "Expiration": (self.expiration, str, ""),
            "Volatility": (self._volatility, float, 0.2)
        }

    @property
    def attribute_dependencies(self):
        return {
            **super().attribute_dependencies,
            "Strike Price": ["Total"],
            "Volatility": ["Total"]
        }

@dataclass
class Swap(FinancialProduct):
    _fixed_rate: float
    _notional: float

    @property
    def fixed_rate(self) -> float:
        return self._fixed_rate

    @fixed_rate.setter
    def fixed_rate(self, value: float):
        if not -1 <= value <= 1:
            raise ValueError("Rate must be between -100% and 100%")
        self._fixed_rate = value

    @property
    def attributes(self):
        base = super().attributes
        return {
            **base,
            "Fixed Rate": (self.fixed_rate, float, 0.0),
            "Notional": (self._notional, float, 1_000_000.0)
        }

    @property
    def attribute_dependencies(self):
        return {
            **super().attribute_dependencies,
            "Fixed Rate": ["Total"],
            "Notional": ["Total"]
        }
