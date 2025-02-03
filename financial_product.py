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
    def dependencies(self):
        """Return attribute dependencies {field: [dependent_fields]}"""
        return {
            "price": ["total"],
            "quantity": ["total"]
        }
