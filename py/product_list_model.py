from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from database_operations import load_products, save_product

class ProductListModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.products = load_products()

    def rowCount(self, parent=QModelIndex()):
        return len(self.products)

    def columnCount(self, parent=QModelIndex()):
        return 2  # Name and Price

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
            
        product = self.products[index.row()]
        
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if index.column() == 0:
                return product.name
            elif index.column() == 1:
                return f"{product.price:.2f}"
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return ["Product Name", "Current Price"][section]
        return None

    def flags(self, index):
        flags = super().flags(index)
        if index.isValid():
            flags |= Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        return flags 

    def save_to_database(self):
        """Save all products to the database."""
        for product in self.products:
            # Implement saving logic for each product type
            pass 