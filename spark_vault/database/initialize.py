from pathlib import Path
import sys
from spark_vault.database.db import get_connection

def initialize_database():
    if Path("sparkvault.db").exists():
        return

    conn = get_connection()

    schema_path = resource_path("spark_vault/database/schema.sql")
    with open(schema_path) as f:
        conn.executescript(f.read())

    conn.close()

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path