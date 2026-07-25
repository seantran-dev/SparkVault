from .db import get_connection

def create_user(username, email, password_hash, salt):
    conn = get_connection() # opening phone call
    cur = conn.cursor() # conversation

    cur.execute(
        """
        INSERT INTO users (username, email, password_hash, kdf_salt)
        VALUES (%s, %s, %s, %s)
        """,
        (username, email, password_hash, salt)    
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
        WHERE username = %s
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
        SET username = %s
        WHERE user_id = %s
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
         "email",
         "password_hash",
         "kdf_salt"
    }
    
    if setting not in allowed:
            raise ValueError("//SQL - Invalid setting.")
        
    cur.execute(
        f"""
        UPDATE users
        SET {setting} = %s
        WHERE user_id = %s;
        """,
        (value, user_id)
    )
    conn.commit()

    cur.close()
    conn.close()
