#include <QApplication>
#include <QMainWindow>
#include <QTableView>
#include <QStatusBar>
#include "FinancialProductModel.h"
#include "ProductListModel.h"
#include "Option.h"
#include "Swap.h"

class ProductDetailWindow : public QMainWindow {
public:
    ProductDetailWindow(FinancialProduct* product, QWidget* parent = nullptr)
        : QMainWindow(parent), m_product(product) 
    {
        m_model = new FinancialProductModel(m_product, this);
        m_tableView = new QTableView(this);
        setCentralWidget(m_tableView);
        m_tableView->setModel(m_model);
        setWindowTitle(QString("Product Details - %1").arg(m_product->name()));
        resize(600, 300);
        
        connect(m_model, &FinancialProductModel::statusMessage, 
                statusBar(), [sb = statusBar()](const QString& msg) {
            sb->showMessage(msg, 0);
        });
    }

private:
    FinancialProduct* m_product;
    FinancialProductModel* m_model;
    QTableView* m_tableView;
};

class MainWindow : public QMainWindow {
public:
    MainWindow(QWidget* parent = nullptr) : QMainWindow(parent) {
        // Create products
        m_products = {
            new Option("Put Option", 50.0, 100, "Equity option", 
                      120.0, "2024-12-31", 0.3, this),
            new Swap("Interest Rate Swap", 0.05, 1000000, 
                    "Fixed vs floating rate", 0.05, 1000000, this)
        };

        // Setup UI
        m_tableView = new QTableView(this);
        setCentralWidget(m_tableView);
        setWindowTitle("Financial Products List");
        resize(600, 300);
        
        showProductList();
        connect(m_tableView, &QTableView::doubleClicked, 
                this, &MainWindow::showProductDetails);
    }

private:
    void showProductList() {
        m_listModel = new ProductListModel(m_products, this);
        m_tableView->setModel(m_listModel);
        m_tableView->setColumnWidth(0, 200);
        m_tableView->setColumnWidth(1, 100);
    }

    void showProductDetails(const QModelIndex& index) {
        auto detailWindow = new ProductDetailWindow(m_products[index.row()]);
        detailWindow->show();
    }

    QVector<FinancialProduct*> m_products;
    QTableView* m_tableView;
    ProductListModel* m_listModel;
};

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    
    MainWindow mainWindow;
    mainWindow.show();
    
    return app.exec();
} 