#pragma once
#include <QAbstractTableModel>
#include <QVector>
#include "FinancialProduct.h"

class ProductListModel : public QAbstractTableModel
{
    Q_OBJECT

public:
    explicit ProductListModel(const QVector<FinancialProduct*>& products, QObject* parent = nullptr);
    
    // QAbstractTableModel interface
    int rowCount(const QModelIndex& parent = QModelIndex()) const override;
    int columnCount(const QModelIndex& parent = QModelIndex()) const override;
    QVariant data(const QModelIndex& index, int role) const override;
    QVariant headerData(int section, Qt::Orientation orientation, int role) const override;
    Qt::ItemFlags flags(const QModelIndex& index) const override;

private:
    QVector<FinancialProduct*> m_products;
}; 