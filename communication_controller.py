import telegram
import smtplib
from email.message import EmailMessage


class CommunicationController:

    @staticmethod
    def send_telegram_message(message_text, config, silent=False):
        bot = telegram.Bot(token=config["telegram_token"])
        for chat_id in config["telegram_chat_ids"]:
            try:
                if not silent:
                    bot.send_message(chat_id=chat_id, text=message_text)
                else:
                    bot.send_message(chat_id=chat_id, text=message_text, disable_notification=True)
            except Exception as e:
                print(f"Fehler beim Versenden der Telegram-Nachricht an {chat_id}: {e}")
        return

    @staticmethod
    def send_email(notification_emails, body, config, subject="Impftermin gefunden"):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = "Impftermin-Checker <" + config["smtp_user"] + ">"
        msg['To'] = ','.join(notification_emails)

        server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
        server.starttls()
        server.login(config["smtp_user"], config["smtp_password"])
        server.send_message(msg)
        server.quit()
        return
