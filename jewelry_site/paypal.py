# STANDARD MODULES
import base64
import requests
import json

# LOCAL MODULES
from config.settings import CLIENT_ID, CLIENT_SECRET
from .models import Address


class PayPalClient:
    def __init__(self, user):
        self.user = user
        self.addresses = Address.objects.filter(user=self.user)
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.to_base64()

    def to_base64(self):
        message = self.client_id + ':' + self.client_secret
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        self.base64_message = base64_bytes.decode('ascii')

    # SEND REQUEST TO PAYPAL API TO CREATE AN ORDER
    def create_order(self, items):
        purchase_units = [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": str(self.get_total(items)),
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": str(self.get_total(items)),
                        }
                    }
                },
                "items": [],
                "shipping": {
                    "address": {
                        "address_line_1": str(self.addresses[0].address_line_1),
                        "address_line_2": str(self.addresses[0].address_line_2),
                        "admin_area_2": str(self.addresses[0].admin_area_2),
                        "admin_area_1": str(self.addresses[0].admin_area_1),
                        "postal_code": str(self.addresses[0].postal_code),
                        "country_code": str(self.addresses[0].country.code)
                    }
                }
            }
        ]

        for item in items:
            purchase_units[0]['items'].append({
                "name": str(item.jewelry.name),
                "quantity": str(item.order_quantity),
                "unit_amount": {
                    "currency_code": "USD",
                    "value": str(item.jewelry.price)}
            })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + self.base64_message,
            # 'Paypal-Request-Id': str(self.user.id)
        }

        data = json.dumps({"intent": "CAPTURE", "purchase_units": purchase_units})

        response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders',
                                 headers=headers, data=data)
        response_json = response.json()
        print('CREATE ORDER: ', response_json)
        return response_json

    # SEND REQUEST TO PAYPAL API TO GET ORDER DETAILS
    def get_order_details(self, order_id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + self.base64_message
        }

        response = requests.get('https://api-m.sandbox.paypal.com/v2/checkout/orders/' + str(order_id), headers=headers)
        response_json = response.json()
        return response_json

    # SEND REQUEST TO PAYPAL API TO CONFIRM ORDER
    def confirm_order(self, order_id):
        order = self.get_order_details(order_id)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + self.base64_message
        }

        data = json.dumps({"payment_source": order['payment_source']})

        response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders/' +
                                 str(order_id) + '/confirm-payment-source', headers=headers, data=data)
        response_json = response.json()
        return response_json

    def authorize_payment_order(self, order_id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + self.base64_message,
        }

        response = requests.post(
            'https://api-m.sandbox.paypal.com/v2/checkout/orders/' + str(order_id) + '/authorize', headers=headers)
        response_json = response.json()
        return response_json

    def capture_payment_order(self, order_id):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + self.base64_message,
        }

        response = requests.post(
            'https://api-m.sandbox.paypal.com/v2/checkout/orders/' + str(order_id) + '/capture', headers=headers)
        response_json = response.json()
        print('CAPTURE ORDER: ', response_json)
        return response_json

    def get_total(self, items):
        total = 0
        if items.count() > 0:
            for item in items:
                total = total + self.get_subtotal(item)
        return total

    def get_subtotal(self, item):
        subtotal = item.jewelry.price * item.order_quantity
        return subtotal
