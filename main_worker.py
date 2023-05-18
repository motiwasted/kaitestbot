import time
import telebot

# Create a bot instance
bot = telebot.TeleBot('6046559810:AAEFIo-pbGa9zgwR9X8nLlM5lluWfyiHE8I')

# Handle incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Check if the message text is "Деплой прошел успешно"
    if message.text.lower() == "123":
        response_text = "Поздравляю ты залил бота на heroku!"
        bot.send_message(message.chat.id, response_text)

# Start the bot
print("Bot was started \n " , time.strftime("%H:%M:%S", time.localtime()))
bot.polling()