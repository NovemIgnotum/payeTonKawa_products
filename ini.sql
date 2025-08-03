create table products(
id SERIAL PRIMARY KEY,
name VARCHAR(127) NOT NULL,
price DOUBLE,
stock_quantity INT NOT NULL,
created_at TIMESTAMP,
updated_at TIMESTAMP
)