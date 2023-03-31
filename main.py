import os
import telegram
import openai
import PyPDF2
import telegram.ext


# Set up Telegram bot and OpenAI API credentials
bot = telegram.Bot(token='6114848997:AAHqgjaMqMzFwszB36IiEPrvSZruNh0ktBM')
openai.api_key = "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"

# Define function to generate text from ChatGPT
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

# Define function to convert text to PDF
def convert_to_pdf(text):
    pdf_writer = PyPDF2.PdfFileWriter()
    pdf_writer.addPage(PyPDF2.pdf.PageObject.createFromString(text))
    with open('output.pdf', 'wb') as output:
        pdf_writer.write(output)

# Define function to handle incoming messages
def handle_message(update, context):
    # Get the message text
    message_text = update.message.text

    # Generate response from ChatGPT
    response_text = generate_text(message_text)

    # Convert response to PDF
    convert_to_pdf(response_text)

    # Send the PDF file back to the user
    with open('output.pdf', 'rb') as f:
        bot.send_document(chat_id=update.effective_chat.id, document=f)

    # Print success message
    print("PDF file sent successfully!")

# Set up the Telegram message handler
updater = telegram.ext.Updater(token='6114848997:AAHqgjaMqMzFwszB36IiEPrvSZruNh0ktBM', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

# Start the bot
updater.start_polling()
