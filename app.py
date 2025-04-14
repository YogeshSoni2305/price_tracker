from flask import Flask, render_template, request
from tracker import get_flipkart_price, send_email

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    error = None

    if request.method == 'POST':
        product_url = request.form.get('product_url')
        try:
            target_price = float(request.form.get('target_price'))
            email = request.form.get('email')  # Optional: collect email from form

            if not product_url or not target_price:
                error = "Please provide both a product URL and a target price."
            else:
                # Get current price
                current_price = get_flipkart_price(product_url)

                if current_price is None:
                    error = "Could not retrieve the product price. Please check the URL and try again."
                else:
                    # Compare prices
                    if current_price <= target_price:
                        # Send email notification
                        if send_email(product_url, current_price, target_price, email or 'recipient@example.com'):
                            message = (
                                f"Success! The current price (₹{current_price:.2f}) is at or below your target "
                                f"(₹{target_price:.2f}). An email notification has been sent."
                            )
                        else:
                            error = (
                                f"The current price (₹{current_price:.2f}) is at or below your target "
                                f"(₹{target_price:.2f}), but there was an error sending the email."
                            )
                    else:
                        message = (
                            f"The current price (₹{current_price:.2f}) is higher than your target "
                            f"price (₹{target_price:.2f})."
                        )

        except ValueError:
            error = "Please enter a valid number for the target price."

    return render_template('index.html', message=message, error=error)

if __name__ == '__main__':
    app.run(debug=True)
