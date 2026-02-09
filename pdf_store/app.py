import os
import smtplib
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import datetime
import time

# Import our checksum helper
try:
    from paytm_checksum import generate_checksum, verify_checksum
except ImportError:
    # If running from root directory
    from pdf_store.paytm_checksum import generate_checksum, verify_checksum

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production
serializer = URLSafeTimedSerializer(app.secret_key)

# --- Configuration ---
# Paytm Credentials (Placeholders - replace with actual values)
PAYTM_MID = "YOUR_MERCHANT_ID"
PAYTM_MERCHANT_KEY = "YOUR_MERCHANT_KEY_12345" # Must be 16-32 chars
PAYTM_WEBSITE = "WEBSTAGING"
PAYTM_CHANNEL_ID = "WEB"
PAYTM_INDUSTRY_TYPE_ID = "Retail"
PAYTM_TXN_URL = "https://securegw-stage.paytm.in/theia/processTransaction" # Staging URL
# PAYTM_TXN_URL = "https://securegw.paytm.in/theia/processTransaction" # Production URL

# App URL (for callback)
BASE_URL = "http://localhost:5000"

# Email Configuration (Placeholders)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"

# PDF Configuration
PDF_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs')

# Product Data
PRODUCTS = {
    "1": {"id": "1", "title": "Ultimate Guide to Python", "price": "100.00", "file": "guide1.pdf", "desc": "Master Python in 30 days."},
    "2": {"id": "2", "title": "Data Science Handbook", "price": "150.00", "file": "guide2.pdf", "desc": "Complete data science reference."},
    "3": {"id": "3", "title": "Web Development 101", "price": "120.00", "file": "guide3.pdf", "desc": "Build your first website."},
    "4": {"id": "4", "title": "Machine Learning Basics", "price": "200.00", "file": "guide4.pdf", "desc": "Intro to ML algorithms."}
}

def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/initiate_payment', methods=['POST'])
def initiate_payment():
    pdf_id = request.form.get('pdf_id')
    email = request.form.get('email')

    if not pdf_id or not email:
        flash("Invalid request.")
        return redirect(url_for('index'))

    product = PRODUCTS.get(pdf_id)
    if not product:
        flash("Product not found.")
        return redirect(url_for('index'))

    # Generate unique Order ID
    order_id = f"ORDER_{int(time.time())}_{pdf_id}"

    # Paytm Parameters
    param_dict = {
        'MID': PAYTM_MID,
        'ORDER_ID': order_id,
        'TXN_AMOUNT': product['price'],
        'CUST_ID': email,  # Using email as Cust ID for simplicity
        'INDUSTRY_TYPE_ID': PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': PAYTM_WEBSITE,
        'CHANNEL_ID': PAYTM_CHANNEL_ID,
        'CALLBACK_URL': f"{BASE_URL}/callback",
        'EMAIL': email,
    }

    try:
        checksum = generate_checksum(param_dict, PAYTM_MERCHANT_KEY)
        param_dict['CHECKSUMHASH'] = checksum
        return render_template('redirect_paytm.html', params=param_dict, txn_url=PAYTM_TXN_URL)
    except Exception as e:
        # In case of mock failure or key error
        print(f"Checksum generation error: {e}")
        flash(f"Error initiating payment: {e}")
        return redirect(url_for('index'))

@app.route('/callback', methods=['POST'])
def callback():
    form_data = request.form.to_dict()

    # Verify Checksum
    checksum = form_data.get('CHECKSUMHASH', '')
    if 'CHECKSUMHASH' in form_data:
        form_data.pop('CHECKSUMHASH')

    is_valid_checksum = False
    try:
        is_valid_checksum = verify_checksum(form_data, PAYTM_MERCHANT_KEY, checksum)
    except Exception as e:
        print(f"Checksum verification error: {e}")

    if is_valid_checksum and form_data.get('RESPCODE') == '01':
        # Payment Successful
        order_id = form_data.get('ORDERID')
        # Extract product ID from Order ID (ORDER_timestamp_pdfid)
        try:
            pdf_id = order_id.split('_')[-1]
            email = form_data.get('EMAIL') or "customer@example.com" # Fallback if not returned

            # Generate Download Token (valid for 24 hours)
            token = serializer.dumps({'pdf_id': pdf_id, 'email': email}, salt='file-download')
            download_link = url_for('download_file', token=token, _external=True)

            # Send Email
            email_body = f"""
            <h2>Thank you for your purchase!</h2>
            <p>You have successfully purchased: {PRODUCTS[pdf_id]['title']}</p>
            <p>Download your file here: <a href="{download_link}">Download PDF</a></p>
            <p>Link is valid for 24 hours.</p>
            """
            # We don't block on email sending in production, use a task queue. Here we just call it.
            # Only attempt if credentials are not placeholders
            if "your_email" not in SMTP_USERNAME:
                send_email(email, "Your PDF Download Link", email_body)

            return render_template('success.html', download_link=download_link, product=PRODUCTS[pdf_id])

        except Exception as e:
            return f"Error processing order: {e}"
    else:
        return "Payment Failed or Checksum Mismatch"

@app.route('/download/<token>')
def download_file(token):
    try:
        data = serializer.loads(token, salt='file-download', max_age=86400) # 24 hours
        pdf_id = data['pdf_id']
        product = PRODUCTS.get(pdf_id)

        if product:
            return send_from_directory(PDF_FOLDER, product['file'], as_attachment=True)
        else:
            return "File not found", 404

    except SignatureExpired:
        return "The download link has expired."
    except BadSignature:
        return "Invalid download link."
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
