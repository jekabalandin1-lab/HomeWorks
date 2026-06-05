import sqlite3

conn = sqlite3.connect("AnimalKingdom.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Animals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL
)
"""
)

animals_data = [
    ("Лев", "Ссавець"),
    ("Крокодил", "Плазун"),
    ("Орел", "Птах"),
    ("Морська черепаха", "Плазун"),
    ("Мавпа", "Ссавець"),
]

cursor.execute("SELECT COUNT(*) FROM Animals")
if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO Animals (name, type) VALUES (?, ?)", animals_data
    )
    conn.commit()

cursor.execute("UPDATE Animals SET name = 'Сокіл' WHERE name = 'Орел'")
conn.commit()

cursor.execute("SELECT * FROM Animals WHERE type = 'Ссавець'")
mammals = cursor.fetchall()
for row in mammals:
    print(row)

cursor.execute("SELECT * FROM Animals")
all_animals = cursor.fetchall()
for row in all_animals:
    print(row)

conn.close()