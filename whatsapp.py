from twilio.rest import Client
from config import account_sid, auth_token,twilio_number,my_number

def whatsapp(mensaje):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=twilio_number,
        body=mensaje,
        to=my_number
    )

    print(f"Mensaje enviado con ID: {message.sid}")