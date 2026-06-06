import smtplib
from email.mime.text import MIMEText

EMAIL = "hsybmalik96@gmail.com"        
APP_PASSWORD = "tdjlvtklgmkpszct"   

def send_alert(message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = "🚨 IDS Alert!"
        msg['From'] = EMAIL
        msg['To'] = EMAIL

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL, APP_PASSWORD)
            server.sendmail(EMAIL, EMAIL, msg.as_string())
            print("✅ Alert email sent!")
    except Exception as e:
        print(f"❌ Email error: {e}")
