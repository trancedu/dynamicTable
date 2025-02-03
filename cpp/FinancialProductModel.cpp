#include "FinancialProductModel.h"
#include <QDateTime>
#include <QMetaType>
#include <QDebug>

FinancialProductModel::FinancialProductModel(FinancialProduct* product, QObject* parent)
    : QAbstractTableModel(parent), m_product(product)
{
    auto productAttrs = m_product->attributes();
    for(auto it = productAttrs.constBegin(); it != productAttrs.constEnd(); ++it) {
        const QVariantList& vals = it.value();
        m_attributes.insert(it.key(), {
            vals[0],
            vals[1].toInt(),
            vals[2],
            vals[3].value<std::function<void(QVariant)>>()
        });
    }
    m_keys = m_attributes.keys();
}

int FinancialProductModel::rowCount(const QModelIndex&) const
{
    return m_keys.size();
}

int FinancialProductModel::columnCount(const QModelIndex&) const
{
    return 4;
}

QVariant FinancialProductModel::data(const QModelIndex& index, int role) const
{
    if (!index.isValid())
        return QVariant();

    const QString& key = m_keys[index.row()];
    const AttributeData& attr = m_attributes[key];

    if (role == Qt::DisplayRole || role == Qt::EditRole) {
        switch (index.column()) {
            case 0: return key;
            case 1: return attr.value;
            case 2: return QMetaType(attr.type).name();
            case 3: return attr.defaultValue;
        }
    }
    return QVariant();
}

QVariant FinancialProductModel::headerData(int section, Qt::Orientation orientation, int role) const
{
    if (role != Qt::DisplayRole)
        return QVariant();

    if (orientation == Qt::Horizontal) {
        static const QStringList headers = {"Attribute", "Value", "Type", "Default"};
        return section < headers.size() ? headers[section] : QVariant();
    }
    return QVariant();
}

Qt::ItemFlags FinancialProductModel::flags(const QModelIndex& index) const
{
    auto flags = QAbstractTableModel::flags(index);
    if (index.column() == 1) {
        const QString key = m_keys[index.row()];
        if (key == "Total")
            return flags & ~Qt::ItemIsEditable;
        return flags | Qt::ItemIsEditable;
    }
    return flags & ~Qt::ItemIsEditable;
}

bool FinancialProductModel::setData(const QModelIndex& index, const QVariant& value, int role)
{
    if (index.column() != 1 || !index.isValid() || role != Qt::EditRole)
        return false;

    const QString key = m_keys[index.row()];
    AttributeData& attr = m_attributes[key];
    
    if (!attr.setter)
        return false;

    try {
        attr.setter(value);
        
        // Replace direct assignment with conversion logic
        auto productAttrs = m_product->attributes();
        m_attributes.clear();
        for(auto it = productAttrs.constBegin(); it != productAttrs.constEnd(); ++it) {
            const QVariantList& vals = it.value();
            m_attributes.insert(it.key(), {
                vals[0],
                vals[1].toInt(),
                vals[2],
                vals[3].value<std::function<void(QVariant)>>()
            });
        }
        
        emit dataChanged(index, index, {role});
        
        // Update dependent fields
        for (const auto& dependent : m_product->attributeDependencies().value(key)) {
            int depRow = m_keys.indexOf(dependent);
            if (depRow != -1) {
                QModelIndex depIndex = this->index(depRow, 1);
                emit dataChanged(depIndex, depIndex, {role});
            }
        }

        emit statusMessage(QString("[%1] ✓ Successfully updated %2 to %3")
                           .arg(getTimestamp(), key, value.toString()));
        return true;
    } catch (const std::exception& e) {
        emit statusMessage(QString("[%1] ✗ Error: %2")
                           .arg(getTimestamp(), e.what()));
        return false;
    }
}

void FinancialProductModel::refreshModel()
{
    beginResetModel();
    auto productAttrs = m_product->attributes();
    m_attributes.clear();
    
    // Convert QVariantList entries to AttributeData structs
    for(auto it = productAttrs.constBegin(); it != productAttrs.constEnd(); ++it) {
        const QVariantList& vals = it.value();
        m_attributes.insert(it.key(), {
            vals[0],  // Current value
            vals[1].toInt(),  // QMetaType ID as int
            vals[2],  // Default value
            vals[3].value<std::function<void(QVariant)>>()  // Setter
        });
    }
    
    m_keys = m_attributes.keys();
    endResetModel();
}

QString FinancialProductModel::getTimestamp() const
{
    return QDateTime::currentDateTime().toString("HH:mm:ss");
} 