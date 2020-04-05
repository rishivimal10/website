import smtplib
import csv
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, send_file
from string import Template
from pathlib import Path
app = Flask(__name__)

@app.route('/')
def my_home():
    return render_template("index.html")

@app.route('/<page_name>')
def page(page_name):
    return render_template(page_name)

def send_email(data):

    html = Template(Path('templates/send_email.html').read_text())
    address = data["email"]
    subject = data["subject"]
    message = data["message"]


    email= EmailMessage()
    email['from'] = address
    email['to'] = 'rvimalen@uwaterloo.ca'
    email['subject'] = "Website Message: " + subject

    email.set_content(html.substitute({'add': address, 'mess': message}), 'html')

    with smtplib.SMTP(host='smtp.gmail.com', port= 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('rishivimal10@gmail.com', 'Infatu8d!Person')
        smtp.send_message(email)

def write_to_csv (data):
    with open ('database.csv', newline='', mode='a') as database:
        address = data["email"]
        subject = data["subject"]
        message = data["message"]

        csv_writer = csv.writer(database, delimiter=',', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([address,subject, message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        send_email(data)
        write_to_csv(data)
        return redirect("/thank_you.html")
    else:
        return "could not send message"

@app.route('/resume_download/')
def resume():
    return send_file("static/assets/Resume_Rishi.pdf")