-- Personal Expense Tracking and Analysis System
CREATE DATABASE IF NOT EXISTS expense_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE expense_tracker;

CREATE TABLE IF NOT EXISTS categories (
    category_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS expenses (
    expense_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    category_id INT UNSIGNED NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    description VARCHAR(240) NOT NULL,
    payment_method ENUM('Cash','Debit card','Credit card','Bank transfer','UPI','Other') NOT NULL DEFAULT 'Other',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_expense_amount_positive CHECK (amount > 0),
    CONSTRAINT fk_expense_category FOREIGN KEY (category_id) REFERENCES categories(category_id),
    INDEX idx_expense_date (expense_date),
    INDEX idx_expense_category_date (category_id, expense_date)
);

INSERT IGNORE INTO categories(category_name) VALUES
('Food & dining'), ('Transport'), ('Housing'), ('Utilities'),
('Shopping'), ('Health'), ('Education'), ('Entertainment'), ('Other');
