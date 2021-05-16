import telegram


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
