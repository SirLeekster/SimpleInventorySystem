-- create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS simpleinventorysystem;

-- select the database to use
USE simpleinventorysystem;

-- create users table
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    username VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    organization_id INT,
    role VARCHAR(20) NOT NULL DEFAULT 'readonly',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- create organizations table
CREATE TABLE IF NOT EXISTS organizations (
    organization_id INT AUTO_INCREMENT PRIMARY KEY,
    organization_name VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
        ON DELETE SET NULL
);

-- add foreign key from users to organizations
ALTER TABLE users
ADD FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
    ON DELETE CASCADE;

-- create user logs table
CREATE TABLE IF NOT EXISTS user_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    action TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- create inventory table
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    product_name TEXT NOT NULL,
    description TEXT DEFAULT NULL,
    category VARCHAR(50) DEFAULT 'general',
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    image_path TEXT DEFAULT NULL,
    created_by BIGINT,
    organization_id INT,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id) ON DELETE CASCADE
);

-- create inventory skus table
CREATE TABLE IF NOT EXISTS inventory_skus (
    sku_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    inventory_id INTEGER NOT NULL,
    sku_code VARCHAR(100) NOT NULL UNIQUE,
    serial_number VARCHAR(100) DEFAULT NULL,
    status VARCHAR(50) DEFAULT 'in_stock',
    expiration_date DATE DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (inventory_id) REFERENCES inventory(id)
        ON DELETE CASCADE
);

-- create sales table
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    inventory_id INTEGER NOT NULL,
    sku_id BIGINT NOT NULL,
    organization_id INTEGER NOT NULL,
    price REAL NOT NULL,
    sold_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (inventory_id) REFERENCES inventory(id),
    FOREIGN KEY (sku_id) REFERENCES inventory_skus(sku_id)
        ON DELETE CASCADE
);

-- create suppliers table
CREATE TABLE IF NOT EXISTS suppliers  (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    address VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- create inventory orders table
CREATE TABLE IF NOT EXISTS inventory_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    supplier_id INT,
    quantity INT NOT NULL,
    status ENUM('pending', 'fulfilled', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- create indexes for faster lookups
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_org_id ON users(organization_id);

CREATE INDEX idx_organizations_creator ON organizations(created_by);

CREATE INDEX idx_user_logs_user_id ON user_logs(user_id);
CREATE INDEX idx_user_logs_timestamp ON user_logs(timestamp);

CREATE INDEX idx_inventory_org ON inventory(organization_id);
CREATE INDEX idx_inventory_creator ON inventory(created_by);
CREATE INDEX idx_inventory_category ON inventory(category);
CREATE INDEX idx_inventory_name ON inventory(product_name(100));

CREATE INDEX idx_inventory_skus_item ON inventory_skus(inventory_id);
CREATE INDEX idx_inventory_skus_status ON inventory_skus(status);
CREATE INDEX idx_inventory_skus_expiration ON inventory_skus(expiration_date);
