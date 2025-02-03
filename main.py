import sys
from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow
from financial_product import FinancialProduct, Option, Swap
from financial_product_model import FinancialProductModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create multiple products
        self.products = [
            Option(
                "Put Option", 50.0, 100, "Equity option", 
                _strike_price=120.0, _expiration="2024-12-31", _volatility=0.3
            ),
            Swap(
                "Interest Rate Swap", 0.05, 1_000_000, "Fixed vs floating rate",
                _fixed_rate=0.05, _notional=1_000_000
            )
        ]
        
        # Setup UI
        self.table_view = QTableView()
        self.setCentralWidget(self.table_view)
        self.setWindowTitle("Financial Products List")
        self.resize(600, 300)
        
        # Show list view initially
        self.show_product_list()
        
        # Connect double click
        self.table_view.doubleClicked.connect(self.show_product_details)

    def show_product_list(self):
        """Show the list of products with name and price"""
        from product_list_model import ProductListModel  # Local import to avoid circular dependency
        self.list_model = ProductListModel(self.products)
        self.table_view.setModel(self.list_model)
        self.table_view.setColumnWidth(0, 200)
        self.table_view.setColumnWidth(1, 100)

    def show_product_details(self, index):
        """Show detailed view in a new window when a row is double-clicked"""
        selected_product = self.products[index.row()]
        self.detail_window = ProductDetailWindow(selected_product)
        self.detail_window.show()

class ProductDetailWindow(QMainWindow):
    def __init__(self, product):
        super().__init__()
        self.product = product
        self.model = FinancialProductModel(self.product)
        
        # Setup UI
        self.table_view = QTableView()
        self.setCentralWidget(self.table_view)
        self.table_view.setModel(self.model)
        self.setWindowTitle(f"Product Details - {self.product.name}")
        self.resize(600, 300)
        
        # Connect error signal to status bar
        self.model.status_message.connect(self.statusBar().showMessage)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
