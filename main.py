import sys
from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow
from financial_product import FinancialProduct, Option, Swap
from financial_product_model import FinancialProductModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.product = Option(
            "Put Option", 50.0, 100, "Equity option", 
            _strike_price=120.0, _expiration="2024-12-31", _volatility=0.3
        )
        self.model = FinancialProductModel(self.product)
        
        # Setup UI
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.setCentralWidget(self.table_view)
        self.setWindowTitle("Financial Product Editor")
        self.resize(600, 300)  # Wider to accommodate new columns
        
        # Connect error signal to status bar
        self.model.status_message.connect(self.statusBar().showMessage)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
