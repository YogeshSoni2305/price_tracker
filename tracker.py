import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_flipkart_price(product_url):
    """
    Scrape the current price from a Flipkart product page.
    Returns the price as a float or None if extraction fails.
    """
    # Headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        # Send GET request
        response = requests.get(product_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try to find price in the specified div
        price_div = soup.find('div', class_='Nx9bqj CxhGGd')
        if price_div:
            price_text = price_div.text.strip()
            # Clean and convert price to float
            price = float(price_text.replace('₹', '').replace(',', ''))
            return price

        # Fallback to regex
        price_pattern = r'₹[0-9,]+'
        price_match = re.search(price_pattern, response.text)
        if price_match:
            price_text = price_match.group(0)
            price = float(price_text.replace('₹', '').replace(',', ''))
            return price

        return None

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except (ValueError, AttributeError) as e:
        print(f"Error parsing price: {e}")
        return None

def send_email(product_url, current_price, target_price, recipient_email):
    """
    Send an email notification when the price drops below the target.
    """
    try:
        # Email configuration
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_PASSWORD')

        # Create email message
        subject = "Flipkart Price Alert: Price Dropped!"
        body = (
            f"The price of the product has dropped to ₹{current_price:.2f}, "
            f"which is below your target price of ₹{target_price:.2f}.\n\n"
            f"Product URL: {product_url}\n\n"
            "Check it out now!"
        )
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)

        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
