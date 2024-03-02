import logging

from faker import Faker
import random
import psycopg2
from psycopg2 import DatabaseError

fake = Faker()

# Підключення до бази даних
conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="123098")
cur = conn.cursor()

# Додавання користувачів
for _ in range(10):
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fake.name(), fake.email(),))

# Додавання задач
for status_id in range(1, 4):
    for _ in range(30):
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", (fake.sentence(), fake.text(), status_id, random.randint(1, 10)))

try:
    # Збереження змін
    conn.commit()
except DatabaseError as e:
    logging.error(e)
    conn.rollback()
finally:
    # Закриття підключення
    cur.close()
    conn.close()