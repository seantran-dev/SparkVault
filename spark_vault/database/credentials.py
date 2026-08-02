from .db import get_connection
from getpass import getpass
from datetime import datetime
from argon2 import PasswordHasher

from spark_vault.encryption.modes import encrypt_CTR, decrypt_CTR

import os

def get_credentials(user):
    conn = get_connection()
    cur = conn.cursor()

    user_id = user[0]
    cur.execute("""
        SELECT credential_id, user_id, service, login_username, ciphertext, nonce, created_at, updated_at, website
        FROM credentials
        WHERE user_id = ?
    """, (user_id,))

    credentials = cur.fetchall()

    cur.close()
    conn.close()

    if not credentials:
        return None

    return credentials

def delete_credential(user_id, cred_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM credentials
        WHERE credential_id = ?
        AND user_id = ?
    """, (cred_id, user_id))

    conn.commit()
    cur.close()
    conn.close()

def add_credentials(user, service, login_username, password, website, aes_key):
    conn = get_connection()
    cur = conn.cursor()
    user_id = user[0]

    password_bytes = password.encode("utf-8")

    nonce, ciphertext = encrypt_CTR(password_bytes, aes_key)


    cur.execute(
        """
        INSERT INTO credentials (user_id, service, login_username, ciphertext, nonce, website)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, service, login_username, ciphertext, nonce, website)    
    )
    conn.commit()

    cur.close()
    conn.close()

# credential[] : credential_id, user_id, service, login_username, ciphertext, nonce, website
def edit_credentials(user, aes_key, cred_id, service, username, password, website):
    conn = get_connection()
    cur = conn.cursor()

    user_id = user[0]

    password_bytes = password.encode("utf-8")
    nonce, ciphertext = encrypt_CTR(password_bytes, aes_key)

    cur.execute(
        """
        UPDATE credentials
        SET
            service = ?,
            login_username = ?,
            ciphertext = ?, 
            nonce = ?,
            website = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE credential_id = ?
        AND user_id = ?
        """,
        (service, username, ciphertext, nonce, website, cred_id, user_id)
    )
    conn.commit()

    cur.close()
    conn.close()


def update_credential_key_change(user_id, credential_id, ciphertext, nonce):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
            """
            UPDATE credentials
            SET
                ciphertext = ?, 
                nonce = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE credential_id = ?
            AND user_id = ?
            """,
            (ciphertext, nonce, credential_id, user_id)
        )
    
    conn.commit()

    cur.close()
    conn.close()

def re_encrypt_credentials(user, current_key, new_password):
    from spark_vault.authentication.login import derive_key
    from spark_vault.encryption.decrypt import decrypt_secret
    from spark_vault.encryption.modes import encrypt_CTR
    from spark_vault.database.users import get_user

    ph = PasswordHasher()
    password_hash = ph.hash(new_password)
    new_kdf_salt = os.urandom(16)
    new_key = derive_key(new_password, new_kdf_salt)

    
    user_id = user[0]
    username = user[1]
    credentials_list = get_credentials(user)

    conn = get_connection()
    cur = conn.cursor()
    try:
        for credential in credentials_list:

            credential_password = decrypt_secret(current_key, credential)
            password_bytes = credential_password.encode("utf-8")
            nonce, ciphertext = encrypt_CTR(password_bytes, new_key)
            
            cur.execute(
                """
                UPDATE credentials
                SET
                    ciphertext = ?, 
                    nonce = ?
                WHERE credential_id = ?
                AND user_id = ?
                """,
                (ciphertext, nonce, credential[0], user_id)
            )

        cur.execute(
            """
            UPDATE users
            SET
                password_hash = ?,
                kdf_salt = ?
            WHERE user_id = ?
            """,
            (password_hash, new_kdf_salt, user_id)
        )

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

    new_user = get_user(username)
    
    return new_user, new_key

