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
    created_by BIGINT,
    organization_id INT,

    FOREIGN KEY (created_by) REFERENCES users(user_id)
        ON DELETE SET NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_inventory_org ON inventory (organization_id);
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_inventory_creator ON inventory(created_by);


-- Insert initial organization(s)
INSERT INTO organizations (organization_name) VALUES
('Default Org');

-- Insert users (using organization_id from above insert)
INSERT INTO users (username, email, password_hash, organization_id) VALUES
('admin', 'admin@example.com', 'sample_hash_1', 1),
('testuser', 'test@example.com', 'sample_hash_2', 1);

-- Insert sample inventory data
INSERT INTO inventory (product_name, description, category, quantity, price, created_by, organization_id) VALUES
('Laptop', '15-inch, 16GB RAM', 'Electronics', 10, 899.99, 1, 1),
('Mouse', 'Wireless USB Mouse', 'Accessories', 20, 19.99, 2, 1);

