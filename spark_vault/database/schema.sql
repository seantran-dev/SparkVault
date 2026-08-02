CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1,
    kdf_salt BLOB NOT NULL
);

CREATE TABLE credentials (
    credential_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    service TEXT NOT NULL,
    login_username TEXT,
    ciphertext BLOB NOT NULL,
    nonce BLOB NOT NULL,
    website TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE user_settings (
    user_id INTEGER PRIMARY KEY,

    hide_passwords INTEGER NOT NULL DEFAULT 1,
    clipboard_timeout INTEGER NOT NULL DEFAULT 60,
    auto_lock_timeout INTEGER NOT NULL DEFAULT 15,
    default_sort TEXT NOT NULL DEFAULT 'UPDATED_DESC',

    FOREIGN KEY(user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);