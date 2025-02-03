class FinancialProduct:
    def __init__(self, name: str, price: float, quantity: int, description: str):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description

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
