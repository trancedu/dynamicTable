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
        """Return a dictionary representation of the product."""
        return {
            "Name": self.name,
            "Price": self.price,
            "Quantity": self.quantity,
            "Description": self.description,
        }

    def update_from_dict(self, data: dict) -> None:
        """Update the product attributes from a dictionary."""
        for key, value in data.items():
            # Here you might want to add type checking/conversion
            setattr(self, key.lower(), value)

    @property
    def display_attributes(self):
        """Return attribute metadata in format {DisplayName: (value, type)}"""
        return {
            "Name": (self.name, str),
            "Price": (self.price, float),
            "Quantity": (self.quantity, int),
            "Description": (self.description, str)
        }
