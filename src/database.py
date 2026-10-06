import psycopg


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "customer_support_db",
    "user": "postgres",
    "password": "NewPassword123"
}


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = psycopg.connect(
        **DB_CONFIG
    )

    return connection


# ============================================================
# TEST CONNECTION
# ============================================================

if __name__ == "__main__":

    try:

        connection = get_connection()

        print(
            "PostgreSQL connection successful!"
        )

        connection.close()

    except Exception as e:

        print(
            "Database connection failed:"
        )

        print(e)