INSERT INTO financial_products (name, price) VALUES
('Put Option', 50.00),
('Interest Rate Swap', 0.05);

CREATE TABLE IF NOT EXISTS options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    strike_price DECIMAL(10, 2) NOT NULL,
    expiration DATE NOT NULL,
    volatility DECIMAL(5, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS swaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    fixed_rate DECIMAL(5, 2) NOT NULL,
    notional DECIMAL(15, 2) NOT NULL
);

INSERT INTO options (name, price, strike_price, expiration, volatility) VALUES
('Put Option', 50.00, 120.00, '2024-12-31', 0.30);

INSERT INTO swaps (name, price, fixed_rate, notional) VALUES
('Interest Rate Swap', 0.05, 0.05, 1000000.00);