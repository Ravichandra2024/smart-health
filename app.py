from flask import Flask, jsonify,render_template
import serial
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
sender_email = "balakrishnareddya800@gmail.com"
sender_password = "stzbmgzbzabbhcgt"
receiver_email = "9921004836@klu.ac.in"
app = Flask(__name__)
ser = serial.serial_for_url('/dev/cu.usbserial-110', baudrate=9600)
subject = "Emergency alert"
body = "The patient need a urgent medicine"
@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/heart_rate', methods=['GET'])
def get_heart_rate():
    data = ser.readline().decode().strip()  
    if data.startswith('HR:'):
        heart_rate = int(data[3:]) 
        response = jsonify({'heart_rate': heart_rate})
        return response, 200
    else:
        return jsonify({'error': 'Invalid data'}), 400  

@app.route("/mail", methods=["GET"])
def fun():
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        response = {"success": True, "message": "Email sent successfully."}
    except Exception as e:
        response = {"success": False, "message": f"An error occurred: {str(e)}"}
    return jsonify(response)
@app.route("/req", methods=["GET"])
def req():
    try:
        with serial.Serial('/dev/cu.usbserial-10', 9600, timeout=1) as ser:
            ser.write("buzz".encode())
            time.sleep(1)
        response = {"success": True, "message": response} 
    except Exception as e:
        response = {"success": False, "message": f"An error occurred: {str(e)}"}
    return jsonify(response)

if __name__ == '__main__':
    ser.flushInput()
    app.run()
