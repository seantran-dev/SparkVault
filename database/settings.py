# settings
from .db import get_connection
import os
from getpass import getpass
from database.users import *
from authentication.login import *
from argon2 import PasswordHasher
from encryption.decrypt import *
from database.credentials import *

def draw_settings_header(current_tab, user = None):
    clear_screen()
    line_length = 45
    
    print(f" SecureDB > Settings", end ="")
    
    if user == None:
        print("")
    else:
        name = user[1]
        print(" " * (line_length - 26 - len(name)), end = "")
        print(f"User: {name}")
    print("-" * line_length, end = "\n")
    if current_tab == "security":  
        print(" [Security]    Credentials     User Account")
    elif current_tab == "credentials":  
        print("  Security    [Credentials]    User Account")
    elif current_tab == "accounts":
        print("  Security     Credentials    [User Account]")
    print("-" * line_length, end = "\n")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_user_settings(user_id):
    conn = get_connection() 
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM user_settings
        WHERE user_id = %s;
        """,
        (user_id,)
    )

    settings = cur.fetchone()

    cur.close()
    conn.close()

    return settings

def update_setting(user_id, setting, value):
        conn = get_connection() 
        cur = conn.cursor()

        # no SQL injections on my watch...
        allowed = {
        "hide_passwords",
        "clipboard_timeout",
        "auto_lock_timeout",
        "default_sort",
        }

        if setting not in allowed:
            raise ValueError("Invalid setting")
        
        cur.execute(
            f"""
            UPDATE user_settings
            SET {setting} = %s
            WHERE user_id = %s;
            """,
            (value, user_id)
        )

        conn.commit()

        cur.close()
        conn.close()

# Toggle hide password
def toggle_hide_passwords(user_id, setting, current_value):
    value_error = False
    value = ""
    while True:
        clear_screen()
        draw_settings_header("security")
        print(" Enabling this will hide all user/credential password entries and displays.\n")

        if value_error is True:
            print("Please enter a valid option.\n")
            value_error = False

        print("  1. Yes")
        print("  2. No")
        print()
        choice = input("> ")
        if choice == "1":
            value = "True"
            update_setting(user_id, setting, True)
            break
        elif choice == "2":
            value = "False"
            update_setting(user_id, setting, False)
            break
        elif choice == "":
            return None
        else: 
            value_error = True
            continue

    return value

# Clipboard timeout
def set_clipboard_timeout(user_id, setting, current_value):
    value_error = False
    value_negative = False
    while True:
        try:
            clear_screen()
            draw_settings_header("security")
            print(" Set the amount of time after copying a password until it is cleared from the clipboard.")
            print(f"\n Input '0' to disable this function. Current Value: {current_value}")

            if value_error is True:
                print("\nPlease enter a valid number.")
                value_error = False
            elif value_negative == True:
                print("\nPlease enter a number greater than 0, or input '0' to disable.")
                value_negative = False
            print()
            value = input("New Value:  ")
            if value == "":
                return None
            value = int(value)
            if value < 0:
                value_negative = True
                continue
            break
        except ValueError:
            value_error = True
    if value == current_value:
        print("No changes made.")
    else:
        update_setting(user_id, setting, value)

    return value

#
def set_auto_lock_timeout(user_id, setting, current_value):
    value_error = False
    value_negative = False
    while True:
        try:
            clear_screen()
            draw_settings_header("security")
            print(" Set the amount of time after log-in until the user is automatically logged out.")
            print(f"\n Input '0' to disable this function. Current Value: {current_value}")

            if value_error is True:
                print("\nPlease enter a valid number.")
                value_error = False
            elif value_negative == True:
                print("\nPlease enter a number greater than 0, or input '0' to disable.")
                value_negative = False
            print()
            value = input("New Value:  ")
            if value == "":
                return None
            value = int(value)
            if value < 0:
                value_negative = True
                continue
            break
        except ValueError:
            value_error = True
    if value == current_value:
        print("No changes made.")
    else:
        update_setting(user_id, setting, value)
        
    return value

def set_default_sort(user_id, setting, current_value):

    value_error = False
    while True:
        clear_screen()
        draw_settings_header("credentials")
        print(" Set how the credentials list is displayed by:\n")
        print("  1. Service name (A-Z)")
        print("  2. Date of creation (Newest)")
        print("  3. Last updated (Newest)")
        print()
        print("  0: Flip the display order of selections")
        print("    (Ex. A-Z becomes Z-A, Newest becomes Oldest)")
        print()
        if value_error == True:
            print("//ERROR - Invalid selection. Please try again.")
            value_error = False
        choice = input("> ")
        if current_value[-10:] == "(inversed)":
            suffix = " (inversed)"
        else:
            suffix = ""
        match choice:
            case "1":
                sort = f"service{suffix}"
                sort_type = "Service name"
            case "2":
                sort = f"created_at{suffix}"
                sort_type = "Date of first entry"
            case "3":
                sort = f"updated_at{suffix}"
                sort_type = "Most recently updated"
            case "0":
                if current_value[-10:] == "(inversed)":
                    sort = current_value[:-11]
                else:
                    sort = f"{current_value} (inversed)"
            case "":
                return None
            case _:
                value_error = True
        if value_error == False:
            update_setting(user_id, setting, sort)
            break
        
    return sort


def change_username_setting(user, current_username):
    draw_settings_header("accounts")
    password = getpass("Enter password to continue: ")
    if password == "":
        return 1, None # cancel
    user = authenticate(current_username, password)
    
    if user == None:
        return 0, None # failed
    username_taken = False
    while True:
        draw_settings_header("accounts")
        if username_taken is True:
            print(f"Username '{new_username}' is already in use.\n")
            username_taken = False
        print(f" Current Username: {current_username}\n")
        new_username = input(f"     New Username: ")
        if get_user(new_username) is not None:
            username_taken = True
            continue
        elif new_username.strip() == "" or new_username.lower() == current_username.lower():
            return 1, None # cancel
        else:
            update_user(user[0], "username", new_username)
            break
        
    return 2, new_username # success

def change_email_setting(user, current_email):
    draw_settings_header("accounts")
    password = getpass("Enter password to continue: ")
    if password == "":
        return 1, None # cancel
    user = authenticate(user[1], password)
    
    if user == None:
        return 0, None # failed
    while True:
        draw_settings_header("accounts")
        print(f" Current E-mail: {current_email}\n")
        new_email = input(f"     New E-mail: ")
        if new_email.strip() == "" or new_email == current_email:
            return 1, None # cancel
        else:
            update_user(user[0], "email", new_email)
            break
        
    return 2, new_email # success

# 1. verify user's current password
# 2. request new password
# 3. generate new key from new password
# 4. decrypt credential ciphertexts with current key
# 5. encrypt ciphertexts with new key
# 6. hash new password and update user

def change_master_password(user):
    draw_settings_header("accounts")
    password = getpass(" Enter current password to continue: ")
    if password == "":
        return 1, None
    user = authenticate(user[1], password)
    if user == None:
        return 0, None # failed

    user, current_key = login(user[1], password)

    new_password = getpass(" Enter new password: ")
    if new_password == "":
        return 1, None
    confirm = getpass(" Confirm new password: ")
    if new_password != confirm:
        return -1, None # failed
    
    new_kdf_salt = os.urandom(16)
    new_key = derive_key(new_password, new_kdf_salt)

    credentials_list = get_credentials(user)
    user_id = user[0]

    ph = PasswordHasher()
    password_hash = ph.hash(new_password)

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
                    ciphertext = %s, 
                    nonce = %s
                WHERE credential_id = %s
                AND user_id = %s
                """,
                (ciphertext, nonce, credential[0], user_id)
            )

        cur.execute(
            """
            UPDATE users
            SET
                password_hash = %s,
                kdf_salt = %s
            WHERE user_id = %s
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

    return 2, new_key

