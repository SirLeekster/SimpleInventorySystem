CREATE DATABASE IF NOT EXISTS simpleinventorysystem;

USE simpleinventorysystem;

CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    organization_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS organizations (
    organization_id INT AUTO_INCREMENT PRIMARY KEY,
    organization_name VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
        ON DELETE SET NULL
);

ALTER TABLE users
ADD FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
    ON DELETE CASCADE;

CREATE TABLE IF NOT EXISTS user_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    action TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    product_name TEXT NOT NULL,
    description TEXT DEFAULT NULL,
    category VARCHAR(50) DEFAULT 'General',
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

CREATE TABLE IF NOT EXISTS inventory_skus (
    sku_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    inventory_id INTEGER NOT NULL,
    sku_code VARCHAR(100) NOT NULL UNIQUE,
    serial_number VARCHAR(100) DEFAULT NULL,
    status VARCHAR(50) DEFAULT 'in_stock', -- e.g., in_stock, sold, damaged, etc.
    expiration_date DATE DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (inventory_id) REFERENCES inventory(id)
        ON DELETE CASCADE
);





CREATE INDEX idx_inventory_org ON inventory (organization_id);
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_inventory_creator ON inventory(created_by);
CREATE INDEX idx_inventory_skus_item ON inventory_skus (inventory_id);

