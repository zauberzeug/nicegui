from nicegui import ui, app
import stripe
import os
from fastapi.responses import RedirectResponse
import dotenv
# Load environment variables from .env file
dotenv.load_dotenv()


# 1. Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', None)  # your secret key

@app.get('/checkout')
async def checkout():
    # Create a checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': 2000,  # $20 in cents
                'product_data': {
                    'name': 'Example Product',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8080/success',
        cancel_url='http://localhost:8080/cancel',
    )
    # Redirect user directly to Stripe-hosted checkout
    return RedirectResponse(session.url, status_code=303)

@ui.page('/')
def index():
    ui.label('Buy a Product')
    # Simply navigate to the /checkout endpoint
    ui.button('Checkout', on_click=lambda: ui.navigate.to('/checkout'))

@ui.page('/success')
def success():
    ui.label('✅ Payment successful! Thank you.')

@ui.page('/cancel')
def cancel():
    ui.label('❌ Payment canceled.')

ui.run()
