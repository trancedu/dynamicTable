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

    def to_dict(self) -> dict:
        """Return a dictionary representation using display_attributes metadata."""
        return {k: v[0] for k, v in self.display_attributes.items()}

    @property
    def display_attributes(self):
        """Return attribute metadata in format {DisplayName: (current_value, type, default)}"""
        # This is computed fresh each time - changes to the dict won't affect instance variables
        return {
            "Name": (self.name, str, ""),
            "Price": (self.price, float, 0.0),
            "Quantity": (self.quantity, int, 0),
            "Description": (self.description, str, "")
        }
