import sqlite3

connection = sqlite3.connect("players.db")

print("Database connected successfully!")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT,
    wins INTEGER,
    losses INTEGER,
    kills INTEGER
)
""")

cursor.execute("""
INSERT INTO players (name, wins, losses, kills)
VALUES ('Dragon99', 25, 10, 100)
""")

cursor.execute("SELECT * FROM players")

result = cursor.fetchall()

print(result)

connection.commit()
connection.close()

print("Players table created successfully!")