#pragma once
#include "FinancialProduct.h"

class Option : public FinancialProduct {
    Q_OBJECT
    Q_PROPERTY(double strikePrice READ strikePrice WRITE setStrikePrice NOTIFY strikePriceChanged)
    Q_PROPERTY(QString expiration READ expiration WRITE setExpiration NOTIFY expirationChanged)
    Q_PROPERTY(double volatility READ volatility WRITE setVolatility NOTIFY volatilityChanged)

public:
    Option(const QString& name, double price, int quantity, const QString& description,
          double strikePrice, const QString& expiration, double volatility, QObject* parent = nullptr);

    double strikePrice() const;
    QString expiration() const;
    double volatility() const;

    QHash<QString, QVariantList> attributes() const override;
    QHash<QString, QVector<QString>> attributeDependencies() const override;

public slots:
    void setStrikePrice(double price);
    void setExpiration(const QString& expiration);
    void setVolatility(double volatility);

signals:
    void strikePriceChanged();
    void expirationChanged();
    void volatilityChanged();

private:
    double m_strikePrice;
    QString m_expiration;
    double m_volatility;
}; 