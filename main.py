from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database credentials (change these with yours)
db_config = {
    'host': 'your-mysql-host',
    'user': 'your-mysql-username',
    'password': 'your-mysql-password',
    'database': 'your-database-name'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                message = f"✅ Welcome {username}!"
            else:
                message = "❌ Invalid credentials"

        except mysql.connector.Error as err:
            message = f"❌ Database error: {err}"

    return render_template('login.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
