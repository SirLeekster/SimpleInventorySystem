-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS simpleinventorysystem;

-- Use the newly created or existing database
USE simpleinventorysystem;

-- Create the 'users' table if it doesn't already exist
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each user
    username VARCHAR(25) UNIQUE NOT NULL,       -- Unique username (max 25 characters)
    email VARCHAR(255) UNIQUE NOT NULL,         -- Unique email for each user
    password_hash VARCHAR(255) NOT NULL,        -- Hashed password for security
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- Timestamp of account creation
);

-- Retrieve all user records (for testing and verification)
SELECT * FROM users;

-- Uncomment the following line if you need to drop the table (for reset purposes)
-- DROP TABLE users;
-- ========================
-- Inventory Table
-- ========================

CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================
-- Sample Inventory Data
-- ========================

INSERT INTO inventory (product_name, quantity, price) VALUES
('Laptop', 10, 899.99),
('Mouse', 20, 19.99),
('Keyboard', 15, 49.99);
