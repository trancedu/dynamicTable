import sys
from PyQt6.QtWidgets import QApplication, QTableView
from financial_product import FinancialProduct
from financial_product_model import FinancialProductModel

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create an instance of your financial product.
    product = FinancialProduct("Bond", 100.0, 1000, "Corporate bond")

    # Create the model and pass the product to it.
    model = FinancialProductModel(product)

    # Create a QTableView and set its model.
    table_view = QTableView()
    table_view.setModel(model)
    table_view.setWindowTitle("Financial Product Editor")
    table_view.resize(400, 200)
    table_view.show()

    sys.exit(app.exec())
