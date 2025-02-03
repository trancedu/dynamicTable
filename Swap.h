#pragma once
#include "FinancialProduct.h"

class Swap : public FinancialProduct {
    Q_OBJECT
    Q_PROPERTY(double fixedRate READ fixedRate WRITE setFixedRate NOTIFY fixedRateChanged)
    Q_PROPERTY(double notional READ notional WRITE setNotional NOTIFY notionalChanged)

public:
    Swap(const QString& name, double price, int quantity, const QString& description,
        double fixedRate, double notional, QObject* parent = nullptr);

    double fixedRate() const;
    double notional() const;

    QHash<QString, QVariantList> attributes() const override;
    QHash<QString, QVector<QString>> attributeDependencies() const override;

public slots:
    void setFixedRate(double rate);
    void setNotional(double amount);

signals:
    void fixedRateChanged();
    void notionalChanged();

private:
    double m_fixedRate;
    double m_notional;
}; 