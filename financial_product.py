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

    def set_name(self, value: str):
        self.name = value

    def set_price(self, value: float):
        self.price = value  # Uses property setter

    def set_quantity(self, value: int):
        self.quantity = value  # Uses property setter

    def set_description(self, value: str):
        self.description = value

    @property
    def attributes(self):
        """Return attribute metadata in format {DisplayName: (value, type, default, setter)}"""
        return {
            "Name": (self.name, str, "", self.set_name),
            "Price": (self.price, float, 0.0, self.set_price),
            "Quantity": (self.quantity, int, 0, self.set_quantity),
            "Description": (self.description, str, "", self.set_description),
            "Total": (self.price * self.quantity, float, 0.0, None)  # No setter for calculated field
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

    def set_strike_price(self, value: float):
        self.strike_price = value  # Uses property setter

    @property
    def expiration(self) -> str:
        return self._expiration

    @expiration.setter
    def expiration(self, value: str):
        # Simple validation for demonstration
        if not value:
            raise ValueError("Expiration date cannot be empty")
        self._expiration = value

    def set_expiration(self, value: str):
        self.expiration = value  # Uses property setter

    def set_volatility(self, value: float):
        if value < 0:
            raise ValueError("Volatility cannot be negative")
        self._volatility = value

    @property
    def attributes(self):
        base = super().attributes
        return {
            **base,
            "Strike Price": (self.strike_price, float, 0.0, self.set_strike_price),
            "Expiration": (self.expiration, str, "", self.set_expiration),
            "Volatility": (self._volatility, float, 0.2, self.set_volatility)
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

    def set_fixed_rate(self, value: float):
        self.fixed_rate = value  # Uses property setter

    @property
    def notional(self) -> float:
        return self._notional

    @notional.setter
    def notional(self, value: float):
        if value < 0:
            raise ValueError("Notional cannot be negative")
        self._notional = value

    def set_notional(self, value: float):
        self.notional = value

    @property
    def attributes(self):
        base = super().attributes
        return {
            **base,
            "Fixed Rate": (self.fixed_rate, float, 0.0, self.set_fixed_rate),
            "Notional": (self._notional, float, 1_000_000.0, self.set_notional)
        }

    @property
    def attribute_dependencies(self):
        return {
            **super().attribute_dependencies,
            "Fixed Rate": ["Total"],
            "Notional": ["Total"]
        }
