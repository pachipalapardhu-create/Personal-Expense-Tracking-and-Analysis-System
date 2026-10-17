-- Fictional sample expenses for a demonstration. Run schema.sql first.
USE expense_tracker;
INSERT INTO expenses(expense_date, category_id, amount, description, payment_method)
SELECT '2026-09-02', category_id, 280.00, 'Sample groceries', 'UPI' FROM categories WHERE category_name='Food & dining';
INSERT INTO expenses(expense_date, category_id, amount, description, payment_method)
SELECT '2026-09-05', category_id, 120.00, 'Sample metro trip', 'Debit card' FROM categories WHERE category_name='Transport';
INSERT INTO expenses(expense_date, category_id, amount, description, payment_method)
SELECT '2026-09-11', category_id, 950.00, 'Sample utility bill', 'Bank transfer' FROM categories WHERE category_name='Utilities';
INSERT INTO expenses(expense_date, category_id, amount, description, payment_method)
SELECT '2026-10-01', category_id, 340.00, 'Sample lunch', 'UPI' FROM categories WHERE category_name='Food & dining';
INSERT INTO expenses(expense_date, category_id, amount, description, payment_method)
SELECT '2026-10-03', category_id, 160.00, 'Sample bus pass top-up', 'Cash' FROM categories WHERE category_name='Transport';
INSERT INTO expenses(expense_date, category_id, amount, description, payment_method)
SELECT '2026-10-07', category_id, 1250.00, 'Sample course book', 'Credit card' FROM categories WHERE category_name='Education';
INSERT INTO expenses(expense_date, category_id, amount, description, payment_method)
SELECT '2026-10-09', category_id, 420.00, 'Sample pharmacy purchase', 'Debit card' FROM categories WHERE category_name='Health';
INSERT INTO expenses(expense_date, category_id, amount, description, payment_method)
SELECT '2026-10-12', category_id, 500.00, 'Sample dinner', 'UPI' FROM categories WHERE category_name='Food & dining';
