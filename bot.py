import telebot
import requests
from config import TOKEN, CMC_API_KEY

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я SatoshiScannerBot. Следи за новыми монетами вместе со мной! Используй команду /newcoins для получения списка новых монет.")

@bot.message_handler(commands=['newcoins'])
def new_coins(message):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '10',
        'sort': 'date_added',
        'sort_dir': 'desc'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }

    response = requests.get(url, params=parameters, headers=headers)
    data = response.json()

    coins_list = ''
    for coin in data['data']:
        coins_list += f"{coin['name']} ({coin['symbol']}) - Цена: ${coin['quote']['USD']['price']:.4f}\n"

    bot.send_message(message.chat.id, f"Самые новые монеты на CoinMarketCap:\n\n{coins_list}")

if __name__ == '__main__':
    bot.infinity_polling()
