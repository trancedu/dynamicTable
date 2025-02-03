#pragma once
#include <QAbstractTableModel>
#include <QVector>
#include <QHash>
#include "FinancialProduct.h"

class FinancialProductModel : public QAbstractTableModel
{
    Q_OBJECT

public:
    explicit FinancialProductModel(FinancialProduct* product, QObject* parent = nullptr);
    
    // QAbstractTableModel interface
    int rowCount(const QModelIndex& parent = QModelIndex()) const override;
    int columnCount(const QModelIndex& parent = QModelIndex()) const override;
    QVariant data(const QModelIndex& index, int role) const override;
    QVariant headerData(int section, Qt::Orientation orientation, int role) const override;
    Qt::ItemFlags flags(const QModelIndex& index) const override;
    bool setData(const QModelIndex& index, const QVariant& value, int role = Qt::EditRole) override;

    void refreshModel();

signals:
    void statusMessage(const QString& message);

private:
    struct AttributeData {
        QVariant value;
        int type;  // Store QMetaType ID as int
        QVariant defaultValue;
    };

    FinancialProduct* m_product;
    QHash<QString, AttributeData> m_attributes;
    QVector<QString> m_keys;

    QString getTimestamp() const;
}; 