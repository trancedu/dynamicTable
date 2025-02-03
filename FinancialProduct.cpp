#include "FinancialProduct.h"
#include <stdexcept>
#include <QVariant>

FinancialProduct::FinancialProduct(QObject* parent) : QObject(parent), 
    m_name(""), m_price(0.0), m_quantity(0), m_description("") {}

FinancialProduct::FinancialProduct(const QString& name, double price, int quantity, 
                                 const QString& description, QObject* parent)
    : QObject(parent), m_name(name), m_price(price), 
      m_quantity(quantity), m_description(description) {}

QString FinancialProduct::name() const { return m_name; }
double FinancialProduct::price() const { return m_price; }
int FinancialProduct::quantity() const { return m_quantity; }
QString FinancialProduct::description() const { return m_description; }
double FinancialProduct::total() const { return m_price * m_quantity; }

void FinancialProduct::setName(const QString& name) { 
    if (m_name != name) {
        m_name = name;
        emit nameChanged();
    }
}

void FinancialProduct::setPrice(double price) {
    if (price < 0) throw std::invalid_argument("Price cannot be negative");
    if (m_price != price) {
        m_price = price;
        emit priceChanged();
    }
}

void FinancialProduct::setQuantity(int quantity) {
    if (quantity < 0) throw std::invalid_argument("Quantity cannot be negative");
    if (m_quantity != quantity) {
        m_quantity = quantity;
        emit quantityChanged();
    }
}

void FinancialProduct::setDescription(const QString& description) {
    if (m_description != description) {
        m_description = description;
        emit descriptionChanged();
    }
}

QHash<QString, QVariantList> FinancialProduct::attributes() const {
    QHash<QString, QVariantList> attrs;
    
    attrs.insert("Name", QVariantList{
        m_name,
        QVariant::fromValue(QMetaType(QMetaType::QString)),
        "",
        QVariant::fromValue(std::function<void(QVariant)>([this](const QVariant& v) mutable { 
            const_cast<FinancialProduct*>(this)->setName(v.toString()); 
        }))
    });
    
    attrs.insert("Price", QVariantList{
        m_price,
        QVariant::fromValue(QMetaType(QMetaType::Double)),
        0.0,
        QVariant::fromValue(std::function<void(QVariant)>([this](const QVariant& v) mutable { 
            const_cast<FinancialProduct*>(this)->setPrice(v.toDouble()); 
        }))
    });
    
    attrs.insert("Quantity", QVariantList{
        m_quantity,
        QVariant::fromValue(QMetaType(QMetaType::Int)),
        0,
        QVariant::fromValue(std::function<void(QVariant)>([this](const QVariant& v) mutable { 
            const_cast<FinancialProduct*>(this)->setQuantity(v.toInt()); 
        }))
    });
    
    attrs.insert("Description", QVariantList{
        m_description,
        QVariant::fromValue(QMetaType(QMetaType::QString)),
        "",
        QVariant::fromValue(std::function<void(QVariant)>([this](const QVariant& v) mutable { 
            const_cast<FinancialProduct*>(this)->setDescription(v.toString()); 
        }))
    });
    
    attrs.insert("Total", QVariantList{
        total(),
        QVariant::fromValue(QMetaType(QMetaType::Double)),
        0.0,
        QVariant::fromValue(std::function<void(QVariant)>())  // Empty function
    });
    
    return attrs;
}

QHash<QString, QVector<QString>> FinancialProduct::attributeDependencies() const {
    return {
        {"Price", {"Total"}},
        {"Quantity", {"Total"}}
    };
} 