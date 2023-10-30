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

    sleep(1) # Wait for a second to simulate a redaction ...

    await  context.bot.send_message (
        chat_id = update.effective_chat.id,
        text = f"Salut *{username}* 👋, \nJe suis **@GitBasicsBot** créer par **@th3fr3dy**.\nJe vais t'aider à réviser ce que tu as appris sur : https://th3fr3dy.me/gitbasics",
        parse_mode = "Markdown"
    )

    await context.bot.send_chat_action (
        chat_id = update.effective_chat.id,
        action = "typing"
    )

    sleep(1) # Wait for a second to simulate a redaction ...

    await  context.bot.send_message (
        chat_id = update.effective_chat.id,
        text = f"Je vais vous poser une question et il vous faudrat donc trouver la solution pour avoir la question suivante. \n\n*Exemple :*\n*Question :* Comment afficher l'historique des versions pour la branche courante dans Git ?\n*Réponse attendue :* _git log_",
        reply_markup=letgoButton,
        parse_mode = "Markdown"

    )
# c_q_id === current_question_id
c_q_id = 0

async def askQuestion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global c_q_id, Questions
    question = f"*Question : * {Questions[0][0]}"

    await context.bot.send_message (
        chat_id = update.effective_chat.id,
        text=  question,
        parse_mode = "Markdown"
    )


async def getResponse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global c_q_id, Questions

    if update.message is not None and update.message.text is not None:  # Add that verification for check if update object is available for this intance 😕
        answer = update.message.text.lower()
        correct_answer = Questions[c_q_id][1].lower()

        if correct_answer == answer:
            c_q_id = (c_q_id + 1) % len(Questions)
            await context.bot.send_message (
                chat_id=update.effective_chat.id,
                text=f"Reponse juste 👌, Passons à la Suivante.",
                parse_mode="Markdown"
            )
            # Sleep for 2s
            sleep(2)
            await askQuestion(update=update, context=context)

        else:
            await context.bot.send_message (
                chat_id=update.effective_chat.id,
                text=f"Mauvaise réponse 🚨",
                parse_mode="Markdown"
            )
    else:
        await context.bot.send_message (
            chat_id=update.effective_chat.id,
            text=f"Un problème est survenu lors du traitement de vote requete🚨"
        )
        logging.warning("L'objet 'update' ou 'update.message' est None ou 'update.message.text' est None.")


        # F-A-Q : For Ask Question

async def letgoButtonOpenFAQ (update: Update, context: ContextTypes.DEFAULT_TYPE):

    getQuery = update.callback_query

    if getQuery.data == "send_message":
       await askQuestion (update=update, context=context)


if __name__ == "__main__":

    gitbot = ApplicationBuilder().token(TOKEN_BOT).build()

    startHandler = CommandHandler("start", start)
    letgoHandler = CallbackQueryHandler(letgoButtonOpenFAQ)
    getResponseHandler = MessageHandler(filters.TEXT & (~filters.COMMAND), getResponse)


    gitbot.add_handler(startHandler)
    gitbot.add_handler(letgoHandler)
    gitbot.add_handler(getResponseHandler)


    gitbot.run_polling()
