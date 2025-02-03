from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from financial_product import FinancialProduct

class FinancialProductModel(QAbstractTableModel):
    def __init__(self, product: FinancialProduct, parent=None):
        super().__init__(parent)
        self.product = product
        # Get a dictionary of attributes and store the keys for ordering.
        self.data_dict = self.product.to_dict()
        self.keys = list(self.data_dict.keys())

    def rowCount(self, parent=QModelIndex()):
        return len(self.keys)

    def columnCount(self, parent=QModelIndex()):
        # We have two columns: Attribute name and value.
        return 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        key = self.keys[index.row()]
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if index.column() == 0:
                # First column shows the attribute name.
                return key
            elif index.column() == 1:
                # Second column shows the attribute's value.
                return str(self.data_dict[key])
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            if section == 0:
                return "Attribute"
            elif section == 1:
                return "Value"
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        # Make the value column editable
        if index.column() == 1:
            return (Qt.ItemFlag.ItemIsEditable |
                    Qt.ItemFlag.ItemIsEnabled |
                    Qt.ItemFlag.ItemIsSelectable)
        return Qt.ItemFlag.ItemIsEnabled

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False

        key = self.keys[index.row()]
        
        # Get type information from the product's display_attributes
        try:
            _, expected_type = self.product.display_attributes[key]
        except KeyError:
            return False

        # Perform type conversion based on product metadata
        try:
            if expected_type is bool:
                # Handle checkbox-like conversions
                value = str(value).lower() in ('true', '1', 'yes')
            else:
                value = expected_type(value)
        except (ValueError, TypeError):
            return False

        try:
            setattr(self.product, key.lower(), value)
        except (TypeError, ValueError) as e:
            # Handle validation errors
            return False

        self.data_dict[key] = value
        self.dataChanged.emit(index, index, [role])
        return True

    def refresh_model(self):
        self.data_dict = self.product.to_dict()
        self.layoutChanged.emit()
