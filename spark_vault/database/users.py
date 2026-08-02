from .db import get_connection


def create_user(username, email, password_hash, salt):
    conn = get_connection() # opening phone call
    cur = conn.cursor() # conversation

    cur.execute(
        """
        INSERT INTO users (username, email, password_hash, kdf_salt)
        VALUES (?, ?, ?, ?)
        """,
        (username, email, password_hash, salt)    
    )

    user_id = cur.lastrowid

    cur.execute(
         """
         INSERT INTO user_settings (user_id)
         VALUES (?);
         """,
         (user_id,)
    )

    conn.commit()

    cur.close()
    conn.close()

def get_user(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user

def set_username(user_id, username):
    conn = get_connection() 
    cur = conn.cursor() 

    cur.execute(
        """
        UPDATE users
        SET username = ?
        WHERE user_id = ?
        """,
        (username, user_id)    
    )

    conn.commit()

    cur.close()
    conn.close()

def update_user(user_id, setting, value):
    conn = get_connection() 
    cur = conn.cursor() 

    allowed = {
         "username",
         "email"
    }
    
    if setting not in allowed:
            raise ValueError("//SQL - Invalid setting.")
        
    cur.execute(
        f"""
        UPDATE users
        SET {setting} = ?
        WHERE user_id = ?;
        """,
        (value, user_id)
    )
    conn.commit()

    cur.close()
    conn.close()

def delete_user(user_id):
    conn = get_connection() 
    cur = conn.cursor() 

    cur.execute(
         f"""
         DELETE FROM users
         WHERE user_id = ?;
         """,
         (user_id,)
    )

    conn.commit()
    
    cur.close()
    conn.close()


def update_username(user, current_password, new_username):
    from spark_vault.authentication.login import authenticate

    if get_user(new_username) is not None:
        return False, "Username is already taken."

    username = user[1]

    if new_username == username:
        return False, "Username is unchanged."
    user = authenticate(username, current_password)

    if user is None:
        return False, "Incorrect password."
    
    user_id = user[0]

    conn = get_connection() 
    cur = conn.cursor() 

    cur.execute(
        """
        UPDATE users
        SET username = ?
        WHERE user_id = ?
        """,
        (new_username, user_id)    
    )

    conn.commit()
    
    cur.close()
    conn.close()

    return True, ""


def update_user_password(user, current_key, current_password, new_password):
    from spark_vault.authentication.login import authenticate
    from spark_vault.database.credentials import get_credentials, re_encrypt_credentials
    from argon2 import PasswordHasher
    
    new_key = current_key
    username = user[1]
    user = authenticate(username, current_password)
    if user is None: 
        return False, "Incorrect password.", user, current_key


    new_user, new_key = re_encrypt_credentials(user, current_key, new_password)

    return True, "Password updated.", new_user, new_key