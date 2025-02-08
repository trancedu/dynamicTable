CREATE DATABASE IF NOT EXISTS financial_product_db;

USE financial_product_db;

drop table financial_products;

drop table options;

drop table swaps;

CREATE TABLE IF NOT EXISTS financial_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    financial_product_id INT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    strike_price DECIMAL(10, 2) NOT NULL,
    expiration DATE NOT NULL,
    volatility DECIMAL(5, 2) NOT NULL,
    quantity INT NOT NULL,
    description TEXT,
    FOREIGN KEY (financial_product_id) REFERENCES financial_products(id)
);

CREATE TABLE IF NOT EXISTS swaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    financial_product_id INT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    fixed_rate DECIMAL(5, 2) NOT NULL,
    notional DECIMAL(15, 2) NOT NULL,
    quantity INT NOT NULL,
    description TEXT,
    FOREIGN KEY (financial_product_id) REFERENCES financial_products(id)
);
