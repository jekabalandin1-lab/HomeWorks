import sqlite3

conn = sqlite3.connect("FruitBasket.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Fruits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    color TEXT NOT NULL
)
"""
)

fruits_data = [("Яблуко", "Червоне"), ("Банан", "Жовтий"), ("Апельсин", "Помаранчевий")]

cursor.execute("SELECT COUNT(*) FROM Fruits")
if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO Fruits (name, color) VALUES (?, ?)", fruits_data
    )
    conn.commit()

cursor.execute("UPDATE Fruits SET color = 'Зелене' WHERE name = 'Яблуко'")
conn.commit()

cursor.execute("SELECT * FROM Fruits WHERE color = 'Жовтий'")
yellow_fruits = cursor.fetchall()
for row in yellow_fruits:
    print(row)

cursor.execute("SELECT * FROM Fruits")
all_fruits = cursor.fetchall()
for row in all_fruits:
    print(row)

conn.close()