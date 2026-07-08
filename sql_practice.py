import sqlite3
conn = sqlite3.connect("fish_oil.db")
cursor = conn.cursor()

# 建表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY, name TEXT, city TEXT, type TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY, customer_id INTEGER, product TEXT,
        purity INTEGER, quantity_kg REAL, price_per_kg REAL, order_date TEXT
    )
""")

# 插数据
cursor.executemany("INSERT OR REPLACE INTO customers VALUES (?,?,?,?)", [
    (1, "杭州宠物食品", "杭州", "宠物品牌"),
    (2, "上海OEM工厂", "上海", "OEM"),
    (3, "广州贸易商", "广州", "贸易商"),
    (4, "宁波保健品", "宁波", "保健品"),
    (5, "深圳宠物科技", "深圳", "宠物品牌"),
])
cursor.executemany("INSERT OR REPLACE INTO orders VALUES (?,?,?,?,?,?,?)", [
    (1, 1, "EE型鱼油", 80, 1000, 85, "2026-06-01"),
    (2, 1, "EE型鱼油", 80, 500, 85, "2026-06-15"),
    (3, 2, "EE型鱼油", 60, 2000, 55, "2026-06-10"),
    (4, 3, "TG型鱼油", 70, 800, 72, "2026-06-20"),
    (5, 4, "EE型鱼油", 85, 300, 95, "2026-07-01"),
    (6, 2, "EE型鱼油", 60, 1500, 55, "2026-07-05"),
    (7, 5, "EE型鱼油", 80, 600, 85, "2026-07-08"),
])
conn.commit()

# === 查询1 ===
print("=== 订单+客户名（JOIN） ===")
cursor.execute("""
    SELECT orders.id, customers.name, orders.product, orders.quantity_kg
    FROM orders
    JOIN customers ON orders.customer_id = customers.id
""")
for row in cursor.fetchall():
    print(row)

# === 查询2 ===
print("\n=== 宠物品牌的订单 ===")
cursor.execute("""
    SELECT customers.name, orders.product, orders.quantity_kg, orders.order_date
    FROM orders
    JOIN customers ON orders.customer_id = customers.id
    WHERE customers.type = '宠物品牌'
""")
for row in cursor.fetchall():
    print(row)

# === 查询3 ===
print("\n=== 每个客户的总采购量（kg） ===")
cursor.execute("""
    SELECT customers.name, SUM(orders.quantity_kg) AS total_kg
    FROM orders
    JOIN customers ON orders.customer_id = customers.id
    GROUP BY customers.name
    ORDER BY total_kg DESC
""")
for row in cursor.fetchall():
    print(row)

conn.close()