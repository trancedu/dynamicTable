#include "Option.h"
#include <stdexcept>
#include <QMetaType>
#include <QVariant>

Option::Option(const QString& name, double price, int quantity, const QString& description,
             double strikePrice, const QString& expiration, double volatility, QObject* parent)
    : FinancialProduct(name, price, quantity, description, parent),
      m_strikePrice(strikePrice),
      m_expiration(expiration),
      m_volatility(volatility)
{
}

double Option::strikePrice() const { return m_strikePrice; }
QString Option::expiration() const { return m_expiration; }
double Option::volatility() const { return m_volatility; }

void Option::setStrikePrice(double price) {
    if(price < 0) throw std::invalid_argument("Strike price cannot be negative");
    if(m_strikePrice != price) {
        m_strikePrice = price;
        emit strikePriceChanged();
    }
}

void Option::setExpiration(const QString& expiration) {
    if(expiration.isEmpty()) throw std::invalid_argument("Expiration date cannot be empty");
    if(m_expiration != expiration) {
        m_expiration = expiration;
        emit expirationChanged();
    }
}

void Option::setVolatility(double volatility) {
    if(volatility < 0) throw std::invalid_argument("Volatility cannot be negative");
    if(m_volatility != volatility) {
        m_volatility = volatility;
        emit volatilityChanged();
    }
}

QHash<QString, QVariantList> Option::attributes() const {
    auto base = FinancialProduct::attributes();
    
    base.insert("strikePrice", QVariantList{
        m_strikePrice,
        QVariant::fromValue(QMetaType::Double),
        0.0
    });
    
    base.insert("expiration", QVariantList{
        m_expiration,
        QVariant::fromValue(QMetaType::QString),
        ""
    });
    
    base.insert("volatility", QVariantList{
        m_volatility,
        QVariant::fromValue(QMetaType::Double),
        0.2
    });
    
    return base;
}

QHash<QString, QVector<QString>> Option::attributeDependencies() const {
    auto base = FinancialProduct::attributeDependencies();
    base.insert("strikePrice", {"Total"});
    base.insert("volatility", {"Total"});
    return base;
} 