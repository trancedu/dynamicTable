CREATE DATABASE IF NOT EXISTS financial_product_db;

USE financial_product_db;

CREATE TABLE IF NOT EXISTS financial_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
