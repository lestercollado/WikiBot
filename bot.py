import os
import wikipedia
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, ParseMode

INPUT_TEXT = 0

wikipedia.set_lang("es")

def start(update, context):
    update.message.reply_text(
        text = "👋 Bienvenido al bot para buscar en la Wikipedia."
    )

def help(update, context):
    update.message.reply_text(
        text = "<b>Ayuda del Bot.</b>\n🟡 El bot mostrará un resumen si encuentra el término buscado. \n🔵 Siempre retornará sugerencias de búsquedas que puedes utilizar para continuar tu búsqueda",
        parse_mode=ParseMode.HTML
    )

def search_command_handler(update,context):
    update.message.reply_text('Envíame lo que deseas buscar 🔎')

    return INPUT_TEXT

def input_text(update, context):
    text = update.message.text

    chat = update.message.chat

    search_wikipedia(text,chat)

    return ConversationHandler.END


def search_wikipedia(text,chat):
    chat.send_action(
        action = ChatAction.TYPING,
        timeout = None
    )

    text_result = "<b>Sugerencias para "+text+":</b> \n"

    busqueda = wikipedia.search(text, results=10, suggestion=False)

    try:
        resumen = wikipedia.summary(text, sentences=5)
        chat.send_message("<b>Resumen:</b>\n"+resumen,parse_mode=ParseMode.HTML)
        for sug in busqueda:
            text_result = text_result +"➖ "+sug+"\n"
        chat.send_message(text_result,parse_mode=ParseMode.HTML)   
    except Exception as e:
        if not busqueda:
            chat.send_message("No se encontraron resultados, ni sugerencias")
        else:
            for sug in busqueda:
                text_result = text_result +"➖ "+sug+"\n"
            chat.send_message(text_result,parse_mode=ParseMode.HTML)  

def random_wikipedia(update, context):
    chat = update.message.chat
    chat.send_action(
        action = ChatAction.TYPING,
        timeout = None
    )
    rand = wikipedia.random(1)
    chat.send_message("<b>Título: </b>"+wikipedia.WikipediaPage(rand).title+"\n"+wikipedia.WikipediaPage(rand).summary+"\n"+"🌐 Ver más: "+wikipedia.WikipediaPage(rand).url,parse_mode=ParseMode.HTML)  

if __name__ == '__main__':    
    updater = Updater(token='1790924272:AAGxVDIseRQhA9DXX6z6PBfix7I3f9cOmh0', use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('iniciar',start))
    dp.add_handler(CommandHandler('ayuda',help))
    dp.add_handler(CommandHandler('aleatoria',random_wikipedia))
    dp.add_handler(ConversationHandler(
        entry_points = [
            CommandHandler('buscar', search_command_handler)
        ],

        states = {
            INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
        },
        
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()