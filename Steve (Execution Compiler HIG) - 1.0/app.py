from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from cryptography.fernet import Fernet

app = Flask(__name__)

# Encryption Key (generate and store securely)
ENCRYPTION_KEY = "TqUA8ph-BvlC-TMu_vZAv3neRWTYlBx5hSB4rtnaSvE="
cipher = Fernet(ENCRYPTION_KEY)

# Database Setup
def init_db():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

@app.route('/')
def index():
    # Retrieve all passwords from the database
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT service, password FROM passwords')
    passwords_data = cursor.fetchall()
    conn.close()

    decrypted_passwords = {service: decrypt_password(pwd) for service, pwd in passwords_data}
    return render_template('index.html', passwords=decrypted_passwords)

@app.route('/add', methods=['GET', 'POST'])
def add_password():
    if request.method == 'POST':
        service = request.form['service']
        password = request.form['password']
        if service and password:
            encrypted_password = encrypt_password(password)
            
            # Insert the password into the database
            conn = sqlite3.connect('passwords.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO passwords (service, password) VALUES (?, ?)', (service, encrypted_password))
            conn.commit()
            conn.close()

        return redirect(url_for('index'))
    return render_template('add_password.html')

@app.route('/delete/<service>')
def delete_password(service):
    # Delete the password from the database
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE service = ?', (service,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
