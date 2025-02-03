import sys
from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow
from financial_product import FinancialProduct
from financial_product_model import FinancialProductModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.product = FinancialProduct("Bond", 100.0, 1000, "Corporate bond")
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
