import random
import psycopg2
from psycopg2 import Error

db_config = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "123098",
}
count_users = 10
count_tasks = 30

try:
    # Підключення до бази даних
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    # Отримати завдання конкретного користувача за його user_id
    user_id = random.randint(1, count_users)
    select_tasks_for_user = f"SELECT * FROM tasks WHERE user_id = {user_id};"
    cursor.execute(select_tasks_for_user)
    tasks_records = cursor.fetchall()
    if tasks_records:
        print(f"Завдання користувача {user_id}:")
        for task in tasks_records:
            print(task)
    else:
        print("Завдань для цього користувача не знайдено.")

    # Вибрати завдання за певним статусом (наприклад, 'new')
    select_tasks_by_status_query = "SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'New');"
    cursor.execute(select_tasks_by_status_query)
    tasks_by_status_records = cursor.fetchall()
    print("Завдання зі статусом 'New':")
    for task in tasks_by_status_records:
        print(task)

    # Оновити статус конкретного завдання (наприклад, змінити на 'in progress')
    task_id_to_update = random.randint(1, count_tasks)
    update_task_status_query = "UPDATE tasks SET status_id = 2 WHERE id = %s;"
    cursor.execute(update_task_status_query, (task_id_to_update,))
    connection.commit()
    print(f"Статус завдання {task_id_to_update} оновлено успішно.")

    # Отримати список користувачів, які не мають жодного завдання
    select_users_without_tasks_query = (
        "SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);"
    )
    cursor.execute(select_users_without_tasks_query)
    users_without_tasks_query = cursor.fetchall()
    print("Користувачі, які не мають жодного завдання:")
    for user in users_without_tasks_query:
        print(user)

    # Додати нове завдання для конкретного користувача
    user_id_to_add_task = random.randint(1, count_users)
    insert_task_query = "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);"
    cursor.execute(
        insert_task_query, ("New task", "Description", 1, user_id_to_add_task)
    )
    connection.commit()
    print(f"Нове завдання для користувача {user_id_to_add_task} додано успішно.")

    # Отримати всі завдання, які ще не завершено
    select_tasks_not_done_query = "SELECT * FROM tasks WHERE status_id != 3;"
    cursor.execute(select_tasks_not_done_query)
    tasks_not_done_query = cursor.fetchall()
    print("Завдання, які ще не завершено:")
    for task in tasks_not_done_query:
        print(task)

    # Видалити конкретне завдання
    task_id_to_delete = random.randint(1, count_tasks)
    delete_task_query = "DELETE FROM tasks WHERE id = %s;"
    cursor.execute(delete_task_query, (task_id_to_delete,))
    connection.commit()
    print(f"Завдання {task_id_to_delete} видалено успішно.")

    # Знайти користувачів з певною електронною поштою.
    select_users_by_email_query = (
        "SELECT * FROM users WHERE email LIKE '%@example.com';"
    )
    cursor.execute(select_users_by_email_query)
    users_by_email_query = cursor.fetchall()
    print("Користувачі з електронною поштою @example.com:")
    for user in users_by_email_query:
        print(user)

    # Оновити ім'я користувача.
    user_id_to_update = random.randint(1, count_users)
    update_user_name_query = "UPDATE users SET fullname = 'Updated Name' WHERE id = %s;"
    cursor.execute(update_user_name_query, (user_id_to_update,))
    connection.commit()
    print(f"Ім'я користувача {user_id_to_update} оновлено успішно.")

    # Отримати кількість завдань для кожного статусу.
    select_tasks_count_query = (
        "SELECT status.name, COUNT(tasks.id) AS task_count FROM status "
        "LEFT JOIN tasks ON status.id = tasks.status_id GROUP BY status.name;"
    )
    cursor.execute(select_tasks_count_query)
    tasks_count_query = cursor.fetchall()
    print("Кількість завдань для кожного статусу:")
    for task in tasks_count_query:
        print(task)

    # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
    user_id = random.randint(1, count_users)
    select_tasks_by_domain_query = (
        f"SELECT * FROM tasks JOIN users ON tasks.user_id = users.id "
        f"WHERE users.email LIKE '%@example.com';"
    )
    cursor.execute(select_tasks_by_domain_query)
    tasks_by_domain_query = cursor.fetchall()
    print("Завдання, які призначені користувачам з доменною частиною @example.com:")
    for task in tasks_by_domain_query:
        print(task)

    # Отримати список завдань, що не мають опису
    select_tasks_without_description_query = (
        "SELECT * FROM tasks WHERE description IS NULL OR description = '';"
    )
    cursor.execute(select_tasks_without_description_query)
    tasks_without_description_query = cursor.fetchall()
    print("Завдання, що не мають опису:")
    for task in tasks_without_description_query:
        print(task)

    # Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
    select_tasks_in_progress_query = (
        "SELECT users.fullname, tasks.title FROM users "
        "INNER JOIN tasks ON users.id = tasks.user_id "
        "WHERE tasks.status_id = 2;"
    )
    cursor.execute(select_tasks_in_progress_query)
    tasks_in_progress_query = cursor.fetchall()
    print("Користувачі та їх завдання, які є у статусі 'in progress':")
    for task in tasks_in_progress_query:
        print(task)

    # Отримати користувачів та кількість їхніх завдань
    select_users_and_tasks_query = (
        "SELECT users.fullname, COUNT(tasks.id) AS task_count FROM users "
        "LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.fullname;"
    )
    cursor.execute(select_users_and_tasks_query)
    users_and_tasks_query = cursor.fetchall()
    print("Користувачі та кількість їх завдань:")
    for user in users_and_tasks_query:
        print(user)

except (Exception, Error) as error:
    print("Помилка при роботі з PostgreSQL", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("З'єднання з базою даних закрите.")
