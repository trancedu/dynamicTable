import sys
from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow, QPushButton, QVBoxLayout, QWidget
from financial_product import FinancialProduct, Option, Swap
from financial_product_model import FinancialProductModel
from product_list_model import ProductListModel
from database_operations import load_products, save_products_to_db

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.products = []  # This will be loaded from the database

        # Setup UI
        self.table_view = QTableView()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_products)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Financial Products List")
        self.resize(600, 300)

        # Show list view initially
        self.show_product_list()
        
        # Connect double click
        self.table_view.doubleClicked.connect(self.show_product_details)

    def show_product_list(self):
        """Show the list of products with name and price"""
        self.products = load_products()  # Assuming load_products is the function to fetch products
        
        # Pass products to ProductListModel
        self.list_model = ProductListModel(self.products)
        self.table_view.setModel(self.list_model)
        self.table_view.setColumnWidth(0, 200)
        self.table_view.setColumnWidth(1, 100)

    def show_product_details(self, index):
        """Show detailed view in a new window when a row is double-clicked"""
        selected_product = self.products[index.row()]
        self.detail_window = ProductDetailWindow(selected_product)
        self.detail_window.show()

    def save_products(self):
        save_products_to_db(self.products)

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
        
        # Add save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_product)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        layout.addWidget(self.save_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Connect error signal to status bar
        self.model.status_message.connect(self.statusBar().showMessage)

    def save_product(self):
        success, message = save_products_to_db([self.product])
        if success:
            self.statusBar().showMessage("Product saved successfully.")
        else:
            self.statusBar().showMessage(f"Error saving product: {message}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
