from flask import render_template ,jsonify, request
from app.pay import bp
import paypalrestsdk


@bp.route('/')
def index():
    return render_template('shopp/payment.html')


paypalrestsdk.configure({
"mode": "sandbox", # sandbox or live
"client_id": "AQJ2oK52oyl_wEM6x9vNxlUqJFMQiT9Z36YEG4qjbBMIF6wvNFFPyZhLThSYNMNCi7D-NIv4qhipuCg9",
"client_secret": "EBMk7nMkjPN1HF9hAR2rIOiibAk8zA3xdnOvJ7sFMKANPZsoEggzwqchc7hAmNLjb81JS2EtGhl8HZgS" })


@bp.route('/payment', methods=['POST'])
def payment():
    payment = paypalrestsdk.Payment(
{
"intent": "sale",
"payer": {
    "payment_method": "paypal"
},
"redirect_urls": {
    "return_url": "http://www.example.com/return_url",
    "cancel_url": "http://www.example.com.br/cancel"
},
"transactions": [
    {
        "amount": {
            "currency": "USD",
            "total": "200.00",
            "details": {
                "shipping": "10.00",
                "subtotal": "190.00"
            }
        },
        "item_list": {
            "items": [
                {
                    "name": "Foto 1",
                    "currency": "USD",
                    "sku": "123",
                    "quantity": "1",
                    "price": "190.00"
                }
            ]
        },
        "description": "Payment description"
    }
]
})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@bp.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})
