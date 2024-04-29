import socket
import threading
import sqlite3
import bcrypt

conn = sqlite3.connect('chat-app.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT)''')
conn.commit()

def handle_client(client_socket, addr):
    print(f"Connected client: {addr}")

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if message.lower() == 'quit':
            break
        else:
            # Parse the message to check credentials
            command, username, password = message.split()
            if command == 'CHECK_CREDENTIALS':
                if check_credentials(username, password):
                    client_socket.send("VALID_CREDENTIALS".encode('utf-8'))
                else:
                    client_socket.send("INVALID_CREDENTIALS".encode('utf-8'))

    print(f"Client {addr} disconnected")
    client_socket.close()

def check_credentials(username, password):
    # Fetch hashed password from the database for the given username
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result:
        hashed_password = result[0]
        # Verify the password using bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    else:
        return False

def register_user(username, password):
    hashed_obj = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_obj.decode('utf-8')))
    conn.commit()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen(5)

while True:
    client, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client, addr))
    client_handler.start()