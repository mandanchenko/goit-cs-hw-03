import logging

from faker import Faker
import random
import psycopg2
from psycopg2 import DatabaseError

fake = Faker()

db_config = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "123098",
}

# Кількість користуваічів
count_users = 10
# Кількість задач
count_tasks = 30
# Перелік статусів
status_list = ["New", "In progress", "Done"]


# Підключення до бази даних
conn = psycopg2.connect(**db_config)
cur = conn.cursor()


# Додавання користувачів
def add_users(count_users):
    for _ in range(count_users):
        cur.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)",
            (
                fake.name(),
                fake.unique.email(),
            ),
        )


# Додавання статусів
def add_status(status_list):
    for status in status_list:
        cur.execute("INSERT INTO status (name) VALUES (%s)", (status,))


# Додавання задач
def add_tasks(status_list, count_users, count_tasks):
    for _ in range(count_tasks):
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (
                fake.sentence(),
                fake.text(),
                random.randint(1, len(status_list)),
                random.randint(1, count_users),
            ),
        )


try:
    add_users(count_users)
    add_status(status_list)
    add_tasks(status_list, count_users, count_tasks)
    conn.commit()
except DatabaseError as e:
    logging.error(e)
    conn.rollback()
finally:
    cur.close()
    conn.close()
