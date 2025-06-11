import os
from flask import Flask, render_template, request, jsonify

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Contact form handler
@app.route('/contact', methods=['POST'])
def handle_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        return jsonify({'status': 'error', 'message': 'All fields are required.'}), 400

    try:
        with open('messages.txt', 'a', encoding='utf-8') as f:
            f.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n---\n")
    except Exception:
        return jsonify({'status': 'error', 'message': 'Failed to save message.'}), 500

    return jsonify({'status': 'success', 'message': 'Thank you for your message! We\'ll get back to you soon.'})

# Waitlist form handler
@app.route('/waitlist', methods=['POST'])
def handle_waitlist():
    email = request.form.get('email')

    if not email:
        return jsonify({'status': 'error', 'message': 'Email is required.'}), 400

    try:
        with open('waitlist.txt', 'a', encoding='utf-8') as f:
            f.write(f"{email}\n")
    except Exception:
        return jsonify({'status': 'error', 'message': 'Failed to save email.'}), 500

    return jsonify({'status': 'success', 'message': 'Thank you for joining our waitlist!'})

# Run locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
