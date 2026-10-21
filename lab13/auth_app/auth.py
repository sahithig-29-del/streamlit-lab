
import bcrypt
from db import get_connection


def signup(username, password):
    conn = get_connection()
    cur = conn.cursor()

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        cur.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (%s, %s)
            """,
            (username, password_hash)
        )
        conn.commit()
        return True, "Signup successful!"

    except Exception:
        conn.rollback()
        return False, "Username already exists or signup failed."

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

        password_matches = bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8")
        )

        if password_matches:
            cur.execute(
                """
                UPDATE users
                SET failed_attempts = 0
                WHERE id = %s
                """,
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
                SET failed_attempts = %s,
                    is_locked = TRUE
                WHERE id = %s
                """,
                (failed_attempts, user_id)
            )
            conn.commit()

            return False, "Account locked after 3 failed attempts."

        cur.execute(
            """
            UPDATE users
            SET failed_attempts = %s
            WHERE id = %s
            """,
            (failed_attempts, user_id)
        )
        conn.commit()

        remaining = 3 - failed_attempts

        return False, (
            f"Invalid password. Attempts remaining: {remaining}"
        )

    finally:
        cur.close()
        conn.close()


def reset_password(username, new_password):
    conn = get_connection()
    cur = conn.cursor()

    password_hash = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        cur.execute(
            """
            UPDATE users
            SET password_hash = %s,
                failed_attempts = 0,
                is_locked = FALSE
            WHERE username = %s
            """,
            (password_hash, username)
        )

        conn.commit()
        return cur.rowcount > 0

    finally:
        cur.close()
        conn.close()
