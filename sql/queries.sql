-- 1. Список товаров
SELECT id, name, price FROM products ORDER BY name;

-- 2. Фильтрация товаров дороже 10 000 рублей
SELECT id, name, price FROM products WHERE price >= 10000 ORDER BY price;

-- 3. Полная информация о заказах
SELECT o.id, o.order_date, p.name AS product_name, s.name AS supplier_name
FROM orders o JOIN products p ON o.product_id = p.id
JOIN suppliers s ON o.supplier_id = s.id WHERE o.is_cancelled = 0;

-- 4. Количество активных заказов
SELECT COUNT(*) AS orders_count FROM orders WHERE is_cancelled = 0;

-- 5. Число заказов по поставщикам
SELECT s.name AS supplier_name, COUNT(o.id) AS orders_count
FROM suppliers s LEFT JOIN orders o ON s.id = o.supplier_id AND o.is_cancelled = 0
GROUP BY s.id, s.name ORDER BY orders_count DESC;

-- 6. Товары без активных заказов
SELECT p.id, p.name FROM products p
WHERE p.id NOT IN (SELECT o.product_id FROM orders o WHERE o.is_cancelled = 0);

-- 7. Заявки по статусам
SELECT status, COUNT(*) AS requests_count FROM requests GROUP BY status;

-- 8. Средняя цена товара
SELECT AVG(price) AS average_price FROM products;

-- 9. Самый дорогой товар
SELECT id, name, price FROM products WHERE price = (SELECT MAX(price) FROM products);

-- 10. Заказы за период
SELECT id, order_date, status FROM orders WHERE order_date BETWEEN '2026-01-01' AND '2026-12-31' ORDER BY order_date;

-- 11. Заявки и связанный заказ
SELECT r.id, r.requester, r.status, r.order_id FROM requests r ORDER BY r.id;

-- 12. Количество товаров у каждого поставщика
SELECT s.name, COUNT(o.id) AS line_count FROM suppliers s
LEFT JOIN orders o ON s.id = o.supplier_id GROUP BY s.id, s.name;
