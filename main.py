import os
import requests
import telegram
import pdfkit
import openai
from flask import Flask, request, jsonify


# Initialize Flask app
app = Flask(__name__)

# Load environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN') or "6114848997:AAHqgjaMqMzFwszB36IiEPrvSZruNh0ktBM"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or "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"

# Initialize Telegram bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Set the webhook for the Telegram bot
def set_webhook():
    url = "https://api.telegram.org/bot{}/setWebhook".format(TELEGRAM_TOKEN)
    webhook_url = "https://telegram-pdf.onrender.com/{}".format(TELEGRAM_TOKEN)
    response = requests.post(url, data={"url": webhook_url})
    print(response.text)

if __name__ == '__main__':
    set_webhook()

# Define the Flask route for handling Telegram webhook events
@app.route('/{}'.format(TELEGRAM_TOKEN), methods=['POST'])
def respond():
    # Parse the incoming message from Telegram
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # Get the user ID and message text
    user_id = update.message.chat.id
    message_text = update.message.text

    # Call ChatGPT to generate a response
    prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. User: {}\nAI:".format(message_text)
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=1024, n=1,stop=None,temperature=0.5).choices[0].text.strip()

    # Generate a PDF file with the response text
    pdfkit.from_string(response, '{}.pdf'.format(user_id))

    # Send the PDF file back to the user
    with open('{}.pdf'.format(user_id), 'rb') as f:
        bot.send_document(chat_id=user_id, document=f)

    return 'OK'

if __name__ == '__main__':
    app.run()
