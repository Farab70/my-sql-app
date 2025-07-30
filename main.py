from flask import Flask, request, render_template
import mysql.connector
import os

app = Flask(__name__)

# Read DB config from environment variables
db_config = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return "✅ Login Successful!"
        else:
            return "❌ Invalid username or password!"

    except Exception as e:
        return f"❗ Database Error: {str(e)}"
