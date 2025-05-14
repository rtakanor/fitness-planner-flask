import sqlite3

def init_db():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            edad INTEGER,
            peso REAL,
            altura REAL,
            genero TEXT,
            actividad INTEGER,
            objetivo TEXT,
            tmr REAL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def guardar_registro(username, edad, peso, altura, genero, actividad, objetivo, tmr):
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO registros (username, edad, peso, altura, genero, actividad, objetivo, tmr)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, edad, peso, altura, genero, actividad, objetivo, tmr))
    conn.commit()
    conn.close()
