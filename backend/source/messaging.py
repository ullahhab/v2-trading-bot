import smtplib
from email.mime.text import MIMEText
import requests
import config

mail = {"mint": "mailmymobile.net", "regular": "gmail.com"}
def send_sms(to_number, message, gmail_user, gmail_app_password, connection):
    """Use this for email instead"""
    to_email = f"{to_number}@{mail[connection]}"
    print(f"email={to_email}")
    msg = MIMEText(message)
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"]= ""

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server: 
        server.login(gmail_user, gmail_app_password)
        server.send_message(msg)
send_sms("hammadullahris", "hello from Hamad", "johnchanged@gmail.com", "wjjt glul ihww osda", "regular")

def sendWhatsAppMessage(message):
    url = f"https://graph.facebook.com/v18.0/{config.META_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {config.META_ACCESS_TOKEN}",
        "Content-Type" : "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": config.TO_NUMBER,
        "type" : "text",
        "text": {"body": message}
    }
    try: 
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if response.status_code == 200:
            print(f"[Meta] sent | ID: {data['messages'][0]['id']}")
            return True
        else:
            print(f"[Meta] Failed | Error: {data}")
            return False
    except Exception as e:
        print(f"[Meta] Failed | Error: {e}")
        return False




