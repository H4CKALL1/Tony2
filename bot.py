import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot token from Telegram
BOT_TOKEN = '7490099653:AAFwf-ePtVaIsODfFWZQSwfvxDjntdidDYs'

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id

    # Send welcome message (this will remain visible)
    welcome_message = await update.message.reply_text(f'Welcome {user.first_name}! Please select your language:')
    
    # Inline buttons for language selection (this will remain visible)
    keyboard = [
        [InlineKeyboardButton("English", callback_data='lang_en')],
        [InlineKeyboardButton("Hindi", callback_data='lang_hi')],
        [InlineKeyboardButton("Gujarati", callback_data='lang_gu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with inline buttons (this will remain visible)
    language_message = await update.message.reply_text('Choose a language:', reply_markup=reply_markup)

    # Save these message IDs so they don't get deleted
    context.user_data['persistent_messages'] = [welcome_message.message_id, language_message.message_id]

# Language selection handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_id = user.id

    # Delete previous messages (but keep welcome and language selection messages)
    if 'temp_message_ids' in context.user_data:
        for msg_id in context.user_data['temp_message_ids']:
            try:
                await context.bot.delete_message(chat_id=query.message.chat_id, message_id=msg_id)
            except:
                pass

    # Show a loading message
    loading_message = await query.message.reply_text("Loading... Please wait")

    # Simulate a short delay for loading (e.g., 2 seconds)
    time.sleep(2)

    # Delete the loading message
    await context.bot.delete_message(chat_id=query.message.chat_id, message_id=loading_message.message_id)

    # Message to show after language selection
    if query.data == 'lang_en':
        text = "In English: All users create a new account and register. After registration you have to deposit ₹100, ₹200 as shown in the photo below and send your hack photo and GoaGame photo to the below id then you And then you will be given the key 🔐"
    elif query.data == 'lang_hi':
        text = "हिंदी में: सभी उपयोगकर्ता एक नया खाता बनाएं और पंजीकरण करें। रजिस्ट्रेशन के बाद आपको नीचे फोटो में दिखाए अनुसार ₹100, ₹200 जमा करने होंगे और अपनी हैक फोटो और GoaGame फोटो नीचे दी गई आईडी पर भेजनी होगी फिर आपको hack key 🔐 दिया जायगा ।"
    elif query.data == 'lang_gu':
        text = "ગુજરાતીમાં: બધા યુઝર નવું એકાઉન્ટ બનાવી લો અને રજીસ્ટર કરી લેજો. રજિસ્ટર કરિયા બાદ નીચે  ફોટો માં બતાવ્યાં મુજબ ₹100, ₹200 ડિપોઝિટ કરીને તમારા hack નો ફોટો અને GoaGame  નો ફોટો નીચે આપેલી id પર મોકલવો પડશે પછી તમને હેક ની key 🔐 આપવા માં આવશે"

    # Send the translated message
    new_message = await context.bot.send_message(chat_id=query.message.chat_id, text=text)

    # Send the same image to all users regardless of the language
    with open('image.jpg', 'rb') as image:
        new_image_message = await context.bot.send_photo(chat_id=query.message.chat_id, photo=image)

    # Send the clickable ID link
    id_link_message = await query.message.reply_text("Click the link below to visit the ID:", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Go to ID", url="http://t.me/Goa_Game_Hackerr")]  # Replace with actual ID URL
    ]))

    # Save the new message IDs (these will be deleted upon the next language selection)
    context.user_data['temp_message_ids'] = [new_message.message_id, new_image_message.message_id, id_link_message.message_id]

# Main function to start the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers for different bot commands and actions
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    # Run the bot until manually stopped
    app.run_polling()