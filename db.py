import sqlite3
from datetime import datetime

DB_NAME = "gastos.db"

def conectar():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            celular TEXT,
            supermercado TEXT,
            monto REAL,
            fecha TEXT
        );
    """)
    return conn

def insertar_gasto(celular, supermercado, monto):
    conn = conectar()
    fecha = datetime.now().strftime("%Y-%m-%d")
    conn.execute("INSERT INTO gastos (celular, supermercado, monto, fecha) VALUES (?, ?, ?, ?)",
                 (celular, supermercado, monto, fecha))
    conn.commit()
    conn.close()
