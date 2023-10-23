import logging
from time import sleep
from credential import TOKEN_BOT
from questions import Questions
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler, filters


logging.basicConfig (
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start (update: Update, context: ContextTypes.DEFAULT_TYPE):

    username = update.effective_user.name
    letgo = InlineKeyboardButton("Commencer 🚀", callback_data="send_message")
    letgoButton = InlineKeyboardMarkup([
        [letgo]
    ])

    await context.bot.send_chat_action (
        chat_id = update.effective_chat.id,
        action = "typing"
    )

    sleep(1) #Attends pendant une seconde pour simmuler une redaction...

    await  context.bot.send_message (
        chat_id = update.effective_chat.id,
        text = f"Salut *{username}* 👋, \nJe suis **@GitBasicsBot** créer par **@th3fr3dy**.\nJe vais t'aider à réviser ce que tu as appris sur : https://th3fr3dy.me/gitbasics",
        parse_mode = "Markdown"
    )

    await context.bot.send_chat_action (
        chat_id = update.effective_chat.id,
        action = "typing"
    )

    sleep(1) #Attends pendant une seconde pour simmuler une redaction...

    await  context.bot.send_message (
        chat_id = update.effective_chat.id,
        text = f"Je vais vous poser une question et il vous faudrat donc trouver la solution pour avoir la question suivante. \n\n*Exemple :*\n*Question :* Comment afficher l'historique des versions pour la branche courante dans Git ?\n*Réponse attendue :* _git log_",
        reply_markup=letgoButton,
        parse_mode = "Markdown"
    )

async def letgoButtonOpen (update: Update, context: ContextTypes.DEFAULT_TYPE):

    getQuery = update.callback_query

    if getQuery.data == "send_message":
            await context.bot.send_message (
                        chat_id= update.effective_chat.id,
                        text=f"*Question : * {Questions[0][0]}",
                        parse_mode= "Markdown"
                    )
            


async def getresponse(update: Update, context: ContextTypes.DEFAULT_TYPE, answer: str):
    if update.message.text.strip() == answer:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Reponse juste 👌",
            parse_mode="Markdown"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Mauvaise réponse 🚨",
            parse_mode="Markdown"
        )

if __name__ == "__main__":

    gitbot = ApplicationBuilder().token(TOKEN_BOT).build()

    startHandler = CommandHandler("start", start)
    letgoHandler = CallbackQueryHandler(letgoButtonOpen)
    getResponseHandler = MessageHandler(filters.TEXT & (~filters.COMMAND), getresponse)


    gitbot.add_handler(startHandler)
    gitbot.add_handler(letgoHandler)
    gitbot.add_handler(getResponseHandler)


    gitbot.run_polling()