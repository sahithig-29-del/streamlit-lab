
import bcrypt
from db import get_connection


def signup(username, email, password):
    conn = get_connection()
    cur = conn.cursor()

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (username, email, password_hash)
        )
        conn.commit()
        return True, "Signup successful!"

    except Exception:
        conn.rollback()
        return False, "Username or email already exists, or signup failed."

    finally:
        cur.close()
        conn.close()


def login(username, password):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT id, password_hash, role, failed_attempts, is_locked
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        user = cur.fetchone()

        if not user:
            return False, "Invalid username or password."

        user_id, password_hash, role, failed_attempts, is_locked = user

        if is_locked:
            return False, "Account locked after 3 failed attempts."

        if bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8")
        ):
            cur.execute(
                "UPDATE users SET failed_attempts = 0 WHERE id = %s",
                (user_id,)
            )
            conn.commit()

            return True, {
                "id": user_id,
                "username": username,
                "role": role
            }

        failed_attempts += 1

        if failed_attempts >= 3:
            cur.execute(
                """
                UPDATE users
                SET failed_attempts = %s, is_locked = TRUE
                WHERE id = %s
                """,
                (failed_attempts, user_id)
            )
            conn.commit()
            return False, "Account locked after 3 failed attempts."

        cur.execute(
            "UPDATE users SET failed_attempts = %s WHERE id = %s",
            (failed_attempts, user_id)
        )
        conn.commit()

        return False, f"Invalid password. Attempts remaining: {3 - failed_attempts}"

    finally:
        cur.close()
        conn.close()


def reset_password(username, email, new_password):
    conn = get_connection()
    cur = conn.cursor()

    try:
        password_hash = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cur.execute(
            """
            UPDATE users
            SET password_hash = %s,
                failed_attempts = 0,
                is_locked = FALSE
            WHERE username = %s AND email = %s
            """,
            (password_hash, username, email)
        )

        conn.commit()
        return cur.rowcount > 0

    finally:
        cur.close()
        conn.close()
