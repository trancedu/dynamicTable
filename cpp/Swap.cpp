#include "Swap.h"
#include <stdexcept>
#include <QMetaType>
#include <QVariant>

Swap::Swap(const QString& name, double price, int quantity, const QString& description,
         double fixedRate, double notional, QObject* parent)
    : FinancialProduct(name, price, quantity, description, parent),
      m_fixedRate(fixedRate),
      m_notional(notional)
{
}

double Swap::fixedRate() const { return m_fixedRate; }
double Swap::notional() const { return m_notional; }

void Swap::setFixedRate(double rate) {
    if(rate < 0) throw std::invalid_argument("Fixed rate cannot be negative");
    if(m_fixedRate != rate) {
        m_fixedRate = rate;
        emit fixedRateChanged();
    }
}

void Swap::setNotional(double amount) {
    if(amount < 0) throw std::invalid_argument("Notional cannot be negative");
    if(m_notional != amount) {
        m_notional = amount;
        emit notionalChanged();
    }
}

QHash<QString, QVariantList> Swap::attributes() const {
    auto base = FinancialProduct::attributes();
    
    base.insert("fixedRate", QVariantList{
        m_fixedRate,
        QVariant::fromValue(QMetaType::Double),
        0.0
    });
    
    base.insert("notional", QVariantList{
        m_notional,
        QVariant::fromValue(QMetaType::Double),
        0.0
    });
    
    return base;
}

QHash<QString, QVector<QString>> Swap::attributeDependencies() const {
    auto base = FinancialProduct::attributeDependencies();
    base.insert("fixedRate", {"Total"});
    base.insert("notional", {"Total"});
    return base;
} 