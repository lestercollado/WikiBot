import os
import wikipedia
import pyshorteners
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, ParseMode

INPUT_TEXT = 0

wikipedia.set_lang("es")

def start(update, context):
    update.message.reply_text(
        text = "👋 Hola, soy un bot para realizar búsquedas en la Wikipedia.\n ⁉️ Consulta la /ayuda para que aprendas como utilizarme"
    )

def about(update, context):
    update.message.reply_text(
        text = "❗️ Desarrollado por Lester Collado Rolo.\n Telegram: @retsel2020"
    )

def help(update, context):
    update.message.reply_text(
        text = "<b>Ayuda del Bot.</b>\n🟡 El bot mostrará un resumen si encuentra el término buscado. \n🔵 Siempre retornará sugerencias de búsquedas que puedes utilizar para continuar tu búsqueda.\n <b>Comandos: </b>\n/aleatoria puedes obtener un resumen de una página aleatoria\n/buscar realizar búsquedas",
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

    busqueda = wikipedia.search(text, results=7, suggestion=False)

    try:
        resumen = wikipedia.summary(text, sentences=5)
        chat.send_message("<b>Resumen:</b>\n"+resumen,parse_mode=ParseMode.HTML)
        for sug in busqueda:
            url = wikipedia.WikipediaPage(sug).url
            text_result = text_result +"➖ "+sug+" ["+short_url(url)+"]"+"\n"
        chat.send_message(text_result,parse_mode=ParseMode.HTML)   
    except Exception as e:
        if not busqueda:
            chat.send_message("No se encontraron resultados, ni sugerencias")
        else:
            for sug in busqueda:
                url = wikipedia.WikipediaPage(sug).url
                text_result = text_result +"➖ "+sug+" ["+short_url(url)+"]"+"\n"
            chat.send_message(text_result,parse_mode=ParseMode.HTML)  

def random_wikipedia(update, context):
    chat = update.message.chat
    chat.send_action(
        action = ChatAction.TYPING,
        timeout = None
    )
    rand = wikipedia.random(1)
    url = wikipedia.WikipediaPage(rand).url
    chat.send_message("<b>Título: </b>"+wikipedia.WikipediaPage(rand).title+"\n"+wikipedia.WikipediaPage(rand).summary+"\n"+"🌐 Ver más: "+short_url(url),parse_mode=ParseMode.HTML)  

def short_url(url):
    s = pyshorteners.Shortener()
    short_u = s.clckru.short(url)
    return short_u

if __name__ == '__main__':    
    updater = Updater(token='1790924272:AAHc_OvukFpvDLLYSeUCeJ7mt7RznEiuQd0', use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('iniciar',start))
    dp.add_handler(CommandHandler('info',about))
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('ayuda',help))
    dp.add_handler(CommandHandler('help',help))
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
