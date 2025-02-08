INSERT INTO financial_products (name, price) VALUES
('Put Option', 50.00),
('Interest Rate Swap', 0.05);

INSERT INTO options (financial_product_id, name, price, strike_price, expiration, volatility, quantity, description)
VALUES (LAST_INSERT_ID(), 'Option Name', 50.00, 120.00, '2024-12-31', 0.30, 10, 'Option Description');

INSERT INTO swaps (financial_product_id, name, price, fixed_rate, notional, quantity, description)
VALUES (LAST_INSERT_ID(), 'Swap Name', 0.05, 0.05, 1000000.00, 5, 'Swap Description');