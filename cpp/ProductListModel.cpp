#include "ProductListModel.h"
#include <QString>

ProductListModel::ProductListModel(const QVector<FinancialProduct*>& products, QObject* parent)
    : QAbstractTableModel(parent), m_products(products)
{
}

int ProductListModel::rowCount(const QModelIndex&) const
{
    return m_products.size();
}

int ProductListModel::columnCount(const QModelIndex&) const
{
    return 2;
}

QVariant ProductListModel::data(const QModelIndex& index, int role) const
{
    if (!index.isValid())
        return QVariant();

    FinancialProduct* product = m_products[index.row()];
    
    if (role == Qt::DisplayRole || role == Qt::EditRole) {
        switch (index.column()) {
            case 0: return product->name();
            case 1: return QString::number(product->price(), 'f', 2);
        }
    }
    return QVariant();
}

QVariant ProductListModel::headerData(int section, Qt::Orientation orientation, int role) const
{
    if (role == Qt::DisplayRole && orientation == Qt::Horizontal) {
        static const QStringList headers = {"Product Name", "Current Price"};
        return section < headers.size() ? headers[section] : QVariant();
    }
    return QVariant();
}

Qt::ItemFlags ProductListModel::flags(const QModelIndex& index) const
{
    Qt::ItemFlags flags = QAbstractTableModel::flags(index);
    if (index.isValid()) {
        flags |= Qt::ItemIsEnabled | Qt::ItemIsSelectable;
    }
    return flags;
} 