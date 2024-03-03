from faker import Faker
import random
import psycopg2

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


# Додавання користувачів
def add_users(count_users):
    users_data = [(fake.name(), fake.unique.email()) for _ in range(count_users)]
    return users_data


# Додавання статусів
def add_status(status_list):
    status_data = [(status,) for status in status_list]
    return status_data


# Додавання задач
def add_tasks(status_list, count_users, count_tasks):
    tasks_data = [
        (
            fake.sentence(),
            fake.text(),
            random.randint(1, len(status_list)),
            random.randint(1, count_users),
        )
        for _ in range(count_tasks)
    ]
    return tasks_data


def main():
    # Підключення до бази даних
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        # Додавання користувачів
        cur.executemany(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)",
            add_users(count_users),
        )

        # Додавання статусів
        cur.executemany(
            "INSERT INTO status (name) VALUES (%s)", add_status(status_list)
        )

        # Додавання задач
        cur.executemany(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            add_tasks(status_list, count_users, count_tasks),
        )

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
