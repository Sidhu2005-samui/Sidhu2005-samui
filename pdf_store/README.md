# Digital PDF Store with Paytm Integration

A simple, one-page website to sell digital PDFs using Paytm as the payment gateway.

## Features
- **One-page Storefront**: Lists products with descriptions and prices.
- **Paytm Integration**: Secure payment processing.
- **Instant Delivery**: Download link generated upon successful payment.
- **Secure Downloads**: Links are signed and expire after 24 hours.
- **Email Receipts**: Sends an email with the download link.
- **No Database**: Uses a simple in-memory configuration (easy to extend to a database).

## Prerequisites
- Python 3.7+
- A Paytm Merchant Account (for credentials)
- An Email Account (for sending receipts via SMTP, e.g., Gmail)

## Installation

1.  **Clone the repository** (if you haven't already).

2.  **Install Dependencies**:
    Navigate to the project directory and install the required packages:
    ```bash
    pip install flask paytmchecksum requests pycryptodome
    ```

3.  **Project Structure**:
    Ensure the following structure exists:
    ```
    pdf_store/
    ├── app.py                 # Main application logic
    ├── paytm_checksum.py      # Checksum helper
    ├── pdfs/                  # Store your PDF files here
    ├── static/
    │   └── style.css          # Styling
    └── templates/
        ├── index.html         # Storefront
        ├── redirect_paytm.html # Redirection page
        └── success.html       # Success page
    ```

## Configuration

Open `app.py` and update the following configuration sections:

### 1. Paytm Credentials
Replace the placeholders with your actual Paytm Merchant details obtained from the [Paytm Dashboard](https://dashboard.paytm.com/).
```python
PAYTM_MID = "YOUR_MERCHANT_ID"
PAYTM_MERCHANT_KEY = "YOUR_MERCHANT_KEY"
PAYTM_WEBSITE = "WEBSTAGING"  # Use "DEFAULT" for production
PAYTM_CHANNEL_ID = "WEB"
PAYTM_INDUSTRY_TYPE_ID = "Retail"
PAYTM_TXN_URL = "https://securegw-stage.paytm.in/theia/processTransaction" # Staging
# For Production use: https://securegw.paytm.in/theia/processTransaction
```

### 2. Email Settings
Configure your SMTP server to send receipt emails. For Gmail, you may need an [App Password](https://support.google.com/accounts/answer/185833).
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"
```

### 3. Products
Update the `PRODUCTS` dictionary in `app.py` with your actual PDF details.
```python
PRODUCTS = {
    "1": {"id": "1", "title": "My Ebook", "price": "99.00", "file": "ebook.pdf", "desc": "Description..."},
    # ...
}
```
*Note: Place your PDF files in the `pdfs/` folder.*

## Running the Application

1.  Start the Flask server:
    ```bash
    python app.py
    ```

2.  Open your browser and navigate to:
    `http://localhost:5000`

## Hosting Guide

You can host this application on any platform that supports Python (e.g., PythonAnywhere, Heroku, AWS, DigitalOcean).

### PythonAnywhere (Recommended for beginners)
1.  Sign up at [PythonAnywhere](https://www.pythonanywhere.com/).
2.  Upload the `pdf_store` files.
3.  Open a Bash console and install dependencies (`pip install flask paytmchecksum ...`).
4.  Go to the "Web" tab, add a new web app, and select "Flask".
5.  Point the WSGI configuration file to your `app.py`.
6.  Reload the web app.

### Deployment Notes
- **Security**: In production, change the `app.secret_key` in `app.py` to a random, secure string.
- **HTTPS**: Ensure your site is served over HTTPS for secure payments.
- **Production Server**: Use a production WSGI server like Gunicorn instead of the built-in Flask server.
  ```bash
  pip install gunicorn
  gunicorn app:app
  ```

## How It Works
1.  User selects a product and enters their email.
2.  App generates a unique Order ID and a Paytm Checksum.
3.  User is redirected to Paytm to complete the payment.
4.  Upon success, Paytm redirects back to `/callback`.
5.  App verifies the checksum and payment status.
6.  App generates a signed, time-limited download link.
7.  App sends an email receipt and displays the download link.
