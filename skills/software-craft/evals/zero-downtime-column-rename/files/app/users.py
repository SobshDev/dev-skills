def create_user(conn, email, name):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO users (email, name) VALUES (%s, %s) RETURNING id", (email, name))
        return cur.fetchone()[0]


def find_by_email(conn, email):
    with conn.cursor() as cur:
        cur.execute("SELECT id, email, name FROM users WHERE email = %s", (email,))
        return cur.fetchone()


def update_email(conn, user_id, email):
    with conn.cursor() as cur:
        cur.execute("UPDATE users SET email = %s WHERE id = %s", (email, user_id))
