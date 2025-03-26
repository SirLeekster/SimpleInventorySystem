-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS simpleinventorysystem;

-- Use the newly created or existing database
USE simpleinventorysystem;

-- Create the 'users' table
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,       -- Unique ID for each user
    username VARCHAR(25) UNIQUE NOT NULL,            -- Unique username
    email VARCHAR(255) UNIQUE NOT NULL,              -- Unique email
    password_hash CHAR(60) NOT NULL,                 -- Bcrypt-hashed password
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP    -- Account creation timestamp
);

-- Create a table to log user actions (optional, for activity tracking)
CREATE TABLE IF NOT EXISTS user_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    action TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create the 'inventory' table
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    product_name TEXT NOT NULL,
    description TEXT DEFAULT NULL,                   -- Optional item description
    category VARCHAR(50) DEFAULT 'General',          -- Optional item category
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,                  -- For soft deletes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Record creation
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create helpful indexes for performance
CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_product_name ON inventory(product_name);

-- Sample Users
INSERT INTO users (username, email, password_hash) VALUES
('admin', 'admin@example.com', 'sample_hash_1'),
('testuser', 'test@example.com', 'sample_hash_2');

-- Sample Inventory Data
INSERT INTO inventory (product_name, description, category, quantity, price) VALUES
('Laptop', '15-inch, 16GB RAM', 'Electronics', 10, 899.99),
('Mouse', 'Wireless USB Mouse', 'Accessories', 20, 19.99);
