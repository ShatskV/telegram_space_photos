import telegram
bot = telegram.Bot(token='5533522910:AAG98OXvC0pmkVUDmswTnM7EvdL3KY5kHqY')

print(bot.get_me())
bot.send_message(chat_id='@devman_bot_channel', text="I'm sorry Dave I'm afraid I can't do that.")