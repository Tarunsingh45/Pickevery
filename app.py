import os
from flask import Flask, render_template, request, jsonify
from pyairtable import Table
from datetime import datetime

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = 'app6yjy1Xxc0ChJkR'  # Replace this
CONTACT_TABLE = 'contacts'              # Name of your contact table
WAITLIST_TABLE = 'waiting list'             # Name of your waitlist table

def save_contact_to_airtable(name, email, message):
    table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, CONTACT_TABLE)
    table.create({
        "Name": name,
        "Email": email,
        "Message": message,
    })

def save_waitlist_to_airtable(email):
    table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, WAITLIST_TABLE)
    table.create({
        "Email": email,
    })


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
        save_contact_to_airtable(name, email, message)
    except Exception as e:
        print("Airtable Error:", e)  # 👈 Add this if it’s not already here
        return jsonify({'status': 'error', 'message': 'Failed to save to Airtable.'}), 500


    return jsonify({'status': 'success', 'message': 'Message received!'})


# Waitlist form handler
@app.route('/waitlist', methods=['POST'])
def handle_waitlist():
    email = request.form.get('email')

    if not email:
        return jsonify({'status': 'error', 'message': 'Email is required.'}), 400

    try:
        save_waitlist_to_airtable(email)
    except Exception as e:
        print("Airtable Error:", e)
        return jsonify({'status': 'error', 'message': 'Failed to save to Airtable.'}), 500

    return jsonify({'status': 'success', 'message': 'You’ve been added to the waitlist!'})


# Privacy Policy page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Terms & Conditions page
@app.route('/terms')
def terms():
    return render_template('terms.html')

# Refund & Cancellation Policy page
@app.route('/refund')
def refund():
    return render_template('refund.html')

# Run locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





