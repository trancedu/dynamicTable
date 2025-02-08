#pragma once
#include <QObject>
#include <QHash>
#include <QVector>
#include <functional>

class FinancialProduct : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int id READ id WRITE setId NOTIFY idChanged)
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)
    Q_PROPERTY(double price READ price WRITE setPrice NOTIFY priceChanged)
    Q_PROPERTY(int quantity READ quantity WRITE setQuantity NOTIFY quantityChanged)
    Q_PROPERTY(QString description READ description WRITE setDescription NOTIFY descriptionChanged)

public:
    explicit FinancialProduct(QObject* parent = nullptr);
    FinancialProduct(const QString& name, double price, int quantity, const QString& description, QObject* parent = nullptr);

    // Property accessors
    QString name() const;
    double price() const;
    int quantity() const;
    QString description() const;
    double total() const;
    int id() const;

    // Virtual methods for attributes
    virtual QHash<QString, QVariantList> attributes() const;
    virtual QHash<QString, QVector<QString>> attributeDependencies() const;

public slots:
    void setName(const QString& name);
    void setPrice(double price);
    void setQuantity(int quantity);
    void setDescription(const QString& description);
    void setId(int id);

signals:
    void nameChanged();
    void priceChanged();
    void quantityChanged();
    void descriptionChanged();
    void idChanged();

protected:
    QString m_name;
    double m_price;
    int m_quantity;
    QString m_description;
    int m_id = 0;
}; 