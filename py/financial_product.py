from dataclasses import dataclass

@dataclass
class FinancialProduct:
    _id: int
    _name: str
    _price: float
    _quantity: int
    _description: str

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if value < 0:
            raise ValueError("ID cannot be negative")
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = str(value)

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
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = str(value)

    @property
    def attributes(self):
        """Return attribute metadata in format {DisplayName: (value, type, default, setter)}"""
        return {
            "Name": (self.name, str, "", self.__class__.name.fset),
            "Price": (self.price, float, 0.0, self.__class__.price.fset),
            "Quantity": (self.quantity, int, 0, self.__class__.quantity.fset),
            "Description": (self.description, str, "", self.__class__.description.fset),
            "Total": (self.price * self.quantity, float, 0.0, None)
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
        if not value:
            raise ValueError("Expiration date cannot be empty")
        self._expiration = value

    @property
    def volatility(self) -> float:
        return self._volatility

    @volatility.setter
    def volatility(self, value: float):
        if value < 0:
            raise ValueError("Volatility cannot be negative")
        self._volatility = value

    @property
    def attributes(self):
        base = super().attributes
        return {
            **base,
            "Strike Price": (self.strike_price, float, 0.0, self.__class__.strike_price.fset),
            "Expiration": (self.expiration, str, "", self.__class__.expiration.fset),
            "Volatility": (self.volatility, float, 0.2, self.__class__.volatility.fset)
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
    def notional(self) -> float:
        return self._notional

    @notional.setter
    def notional(self, value: float):
        if value < 0:
            raise ValueError("Notional cannot be negative")
        self._notional = value

    @property
    def attributes(self):
        base = super().attributes
        return {
            **base,
            "Fixed Rate": (self.fixed_rate, float, 0.0, self.__class__.fixed_rate.fset),
            "Notional": (self.notional, float, 1_000_000.0, self.__class__.notional.fset)
        }

    @property
    def attribute_dependencies(self):
        return {
            **super().attribute_dependencies,
            "Fixed Rate": ["Total"],
            "Notional": ["Total"]
        }
