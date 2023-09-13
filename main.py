import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from newsapi import NewsApiClient

# Set your Telegram Bot API token and News API key here
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
NEWS_API_KEY = 'YOUR_NEWS_API_KEY'

# Initialize the NewsApiClient
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Initialize the updater and dispatcher
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Enable logging (optional)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Command handler for the /start command
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello {user.mention_html()}! I'm here to provide you with news headlines. Just type /news to get started!")

# Command handler for the /news command
def get_news(update: Update, context: CallbackContext):
    headlines = newsapi.get_top_headlines(sources='YOUR_NEWS_SOURCE')  # Replace with your desired news source
    if headlines and 'articles' in headlines:
        articles = headlines['articles']
        for article in articles:
            title = article['title']
            url = article['url']
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"<a href='{url}'>{title}</a>", parse_mode='HTML')

# Add handlers to the dispatcher
start_handler = CommandHandler('start', start)
news_handler = CommandHandler('news', get_news)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(news_handler)

# Start the bot
if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
