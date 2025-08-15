#!/usr/bin/env python3
import stripe
from fastapi.responses import RedirectResponse

from nicegui import app, ui

stripe.api_key = 'not-set'  # TODO: set your Stripe API key here


@ui.page('/')
def index():
    ui.label('Buy a Product')
    ui.button('Checkout', on_click=lambda: ui.navigate.to('/checkout'))


@app.get('/checkout')
def checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': 2000,  # $20 in cents
                'product_data': {'name': 'Example Product'},
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8080/success',
        cancel_url='http://localhost:8080/cancel',
    )
    return RedirectResponse(session.url, status_code=303)


@ui.page('/success')
def success():
    ui.label('✅ Payment successful! Thank you.')


@ui.page('/cancel')
def cancel():
    ui.label('❌ Payment canceled.')


ui.run()
