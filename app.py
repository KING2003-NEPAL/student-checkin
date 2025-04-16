from flask import Flask, render_template, request
import pandas as pd
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)
csv_file = 'attendance.csv'

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        student_number = request.form['number']
        bi_number = request.form['bi']

        try:
            df = pd.read_csv(csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Name', 'Student Number', 'BI Number'])

        if (bi_number in df['BI Number'].values) or (student_number in df['Student Number'].values):
            message = "You have already checked in."
            qr_code_image = None
        else:
            new_entry = pd.DataFrame({
                'Name': [name],
                'Student Number': [student_number],
                'BI Number': [bi_number]
            })
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(csv_file, index=False)

            qr_data = f"Name: {name}\nStudent Number: {student_number}\nBI: {bi_number}"
            qr_code_image = generate_qr(qr_data)
            message = "Check-in successful!"

        return render_template('form.html', message=message, qr_code_image=qr_code_image)

    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('form.html', message="An error occurred. Please try again.")

@app.route('/dashboard')
def dashboard():
    try:
        df = pd.read_csv(csv_file)
        records = df.to_dict(orient='records')
    except FileNotFoundError:
        records = []

    return render_template('dashboard.html', records=records)

def generate_qr(data):
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=True)

