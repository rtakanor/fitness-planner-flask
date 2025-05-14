from flask import Flask, request, jsonify, redirect, session, render_template
from fitness import UserProfile, calcular_bmr, calcular_tmr, rutinas
from db import init_db, guardar_registro
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave-super-secreta'
init_db()

@app.route('/')
def home():
    if 'username' not in session:
        return redirect('/login')
    return render_template('index.html', username=session['username'])

@app.route('/api/bmr', methods=['POST'])
def bmr():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    data = request.json
    user = UserProfile(data['edad'], data['peso'], data['altura'], data['genero'])
    return jsonify({'bmr': calcular_bmr(user)})

@app.route('/api/tmr', methods=['POST'])
def tmr():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    data = request.json
    user = UserProfile(data['edad'], data['peso'], data['altura'], data['genero'])
    objetivo = data['objetivo'].lower()
    actividad = int(data['actividad'])

    resultado = calcular_tmr(user, actividad)
    rutina = rutinas.get(objetivo)

    if not rutina:
        return jsonify({'error': 'Objetivo inválido'}), 400

    guardar_registro(
        session['username'],
        data['edad'], data['peso'], data['altura'],
        data['genero'], actividad, objetivo,
        resultado
    )

    return jsonify({
        'tmr': resultado,
        'rutina': [
            {"dia": dia, "actividad": act}
            for dia, act in zip(rutinas['dias'], rutina)
        ]
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verificar_usuario(username, password):
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error="Credenciales inválidas")
    return render_template('login.html', error=None)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    try:
        crear_usuario(username, password)
        session['username'] = username
        return redirect('/')
    except sqlite3.IntegrityError:
        return render_template('login.html', error="Ese usuario ya existe. Intenta otro nombre.")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

def crear_usuario(username, password):
    conn = sqlite3.connect('usuarios.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def verificar_usuario(username, password):
    conn = sqlite3.connect('usuarios.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cur.fetchone()
    conn.close()
    return result is not None

if __name__ == '__main__':
    app.run(debug=True)
