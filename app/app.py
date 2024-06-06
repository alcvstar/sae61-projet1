import re
from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

def is_valid_username(username):
    return re.fullmatch(r'[a-z]{6,8}', username) is not None

def is_valid_password(password):
    return (
        6 <= len(password) <= 15 and
        re.search(r'[0-9]', password) and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[ #%{}@]', password)
    )

def is_valid_email(email):
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not is_valid_username(username):
        return jsonify({"error": "Identifiant invalide : L'identifiant doit faire entre 6 & 10 caractères en minuscules (caractères ASCII uniquement)"}), 400
    if not is_valid_password(password):
        return jsonify({"error": "Mot de passe invalide : le mot de passe doit faire entre 6 et 15 caractères, et doit contenir au moins une majuscule, une minuscule, un chiffre et un carctère spécial parmis #%{}@"}), 400
    if not is_valid_email(email):
        return jsonify({"error": "Email invalide"}), 400

    try:
        conn = psycopg2.connect(
            dbname="your_db_name",
            user="your_db_user",
            password="your_db_password",
            host="db"
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (username, password, email)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "L'utilisateur a été enregistré avec succès"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
