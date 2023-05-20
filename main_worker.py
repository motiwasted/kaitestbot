import os
import telebot

# Get the bot token from the Heroku environment variable
bot_token = os.environ.get('6046559810:AAEFIo-pbGa9zgwR9X8nLlM5lluWfyiHE8I')

# Create a bot instance
bot = telebot.TeleBot(bot_token)

# Handle the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    response = "Hello! This is a simple Telegram bot."
    bot.send_message(message.chat.id, response)

# Handle incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = "You said: " + message.text
    bot.send_message(message.chat.id, response)

# Start the bot
bot.polling()