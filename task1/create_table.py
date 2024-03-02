import psycopg2

db_config = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "123098",
}

create_table_queries = [
    """
    drop table if exists tasks;
    drop table if exists status;
    drop table if exists users;
    """,
    """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE
    )
    """,
    """
    CREATE TABLE status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
    """,
    """
    CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(175) NOT NULL,
        description text,
        status_id INTEGER  REFERENCES status(id)
        on delete cascade,
        user_id INTEGER  REFERENCES users(id)
        on delete cascade
    );
    """,
]


def create_tables():
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        for query in create_table_queries:
            cur.execute(query)

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    create_tables()
