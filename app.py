from flask import Flask, request, jsonify, render_template_string
import random
import string

app = Flask(__name__)

# Set up characters and shuffled key for substitution cipher
chars = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)
key = chars.copy()
random.shuffle(key)

# Encryption Function
def encrypt(plain_text):
    cipher_text = ""
    for letter in plain_text:
        if letter in chars:
            index = chars.index(letter)
            cipher_text += key[index]
        else:
            cipher_text += letter
    return cipher_text

# Decryption Function
def decrypt(cipher_text):
    plain_text = ""
    for letter in cipher_text:
        if letter in key:
            index = key.index(letter)
            plain_text += chars[index]
        else:
            plain_text += letter
    return plain_text

# Route for main page with HTML and CSS embedded
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Text Encryption & Decryption</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #fbc2eb, #a6c1ee);
            }
            .container {
                width: 400px;
                padding: 40px;
                background-color: #ffffff;
                border-radius: 12px;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
                text-align: center;
            }
            h2 {
                color: #333;
                margin-bottom: 20px;
                font-size: 24px;
            }
            textarea {
                width: 100%;
                height: 120px;
                padding: 12px;
                margin-top: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                resize: none;
                font-size: 16px;
                transition: box-shadow 0.3s ease;
            }
            textarea:focus {
                outline: none;
                border-color: #4CAF50;
                box-shadow: 0 0 8px rgba(76, 175, 80, 0.4);
            }
            .button-container {
                margin-top: 20px;
            }
            button {
                width: 120px;
                padding: 12px;
                margin: 5px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                color: white;
                background-color: #4CAF50;
                transition: all 0.3s ease;
            }
            button:hover {
                background-color: #45a049;
                transform: translateY(-2px);
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            }
            .output {
                margin-top: 25px;
                color: #333;
                font-weight: bold;
                padding: 12px;
                background-color: #f9f9f9;
                border-radius: 8px;
                word-break: break-word;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Text Encryption & Decryption</h2>
            <textarea id="message" placeholder="Enter your message here..."></textarea>
            <div class="button-container">
                <button onclick="encryptMessage()">Encrypt</button>
                <button onclick="decryptMessage()">Decrypt</button>
            </div>
            <div id="output" class="output"></div>
        </div>

        <script>
            function encryptMessage() {
                const message = document.getElementById("message").value;
                fetch('/encrypt', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("output").innerText = "Encrypted: " + data.encrypted_message;
                });
            }

            function decryptMessage() {
                const message = document.getElementById("message").value;
                fetch('/decrypt', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("output").innerText = "Decrypted: " + data.decrypted_message;
                });
            }
        </script>
    </body>
    </html>
    ''')

# Route for encryption
@app.route('/encrypt', methods=['POST'])
def encrypt_message():
    data = request.json
    message = data['message']
    encrypted_message = encrypt(message)
    return jsonify({"encrypted_message": encrypted_message})

# Route for decryption
@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    data = request.json
    message = data['message']
    decrypted_message = decrypt(message)
    return jsonify({"decrypted_message": decrypted_message})

if __name__ == '__main__':
    app.run(debug=True)
