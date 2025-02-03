from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, pyqtSignal
from financial_product import FinancialProduct
from datetime import datetime  # Add datetime import

class FinancialProductModel(QAbstractTableModel):
    status_message = pyqtSignal(str)  # Renamed signal

    def __init__(self, product: FinancialProduct, parent=None):
        super().__init__(parent)
        self.product = product
        self.attributes = self.product.attributes
        self.keys = list(self.attributes.keys())

    def rowCount(self, parent=QModelIndex()):
        return len(self.keys)

    def columnCount(self, parent=QModelIndex()):
        # Now four columns: Attribute, Value, Type, Default
        return 4

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        key = self.keys[index.row()]
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            col = index.column()
            attr_data = self.attributes[key]
            
            if col == 0:  # Attribute name
                return key
            elif col == 1:  # Current value
                return str(attr_data[0])
            elif col == 2:  # Value type
                return attr_data[1].__name__
            elif col == 3:  # Default value
                return str(attr_data[2])
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            headers = ["Attribute", "Value", "Type", "Default"]
            return headers[section] if section < len(headers) else None
        return None

    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 1:
            # Make Total field non-editable
            key = self.keys[index.row()]
            if key == "Total":
                return flags & ~Qt.ItemFlag.ItemIsEditable
            return flags | Qt.ItemFlag.ItemIsEditable
        return flags & ~Qt.ItemFlag.ItemIsEditable

    def _get_timestamp(self):
        """Helper method to format current timestamp"""
        return f"[{datetime.now().strftime('%H:%M:%S')}]"

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if index.column() != 1 or not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False

        key = self.keys[index.row()]
        _, expected_type, default = self.attributes[key]

        try:
            converted_value = expected_type(value)
            setattr(self.product, key.lower(), converted_value)
            self.attributes = self.product.attributes
            
            # Emit data change for current field
            self.dataChanged.emit(index, index, [role])
            
            # If Price or Quantity changed, also update Total
            if key in ("Price", "Quantity"):
                total_row = self.keys.index("Total")
                total_index = self.index(total_row, 1)
                self.dataChanged.emit(total_index, total_index, [role])

            self.status_message.emit(
                f"{self._get_timestamp()} ✓ Successfully updated {key} to {converted_value}"
            )
            return True
        except (ValueError, TypeError) as e:
            self.status_message.emit(
                f"{self._get_timestamp()} ✗ Validation error: {str(e)}"
            )
            return False
        except Exception as e:
            self.status_message.emit(
                f"{self._get_timestamp()} ✗ Unexpected error: {str(e)}"
            )
            return False

    def refresh_model(self):
        self.attributes = self.product.attributes
        self.layoutChanged.emit()
