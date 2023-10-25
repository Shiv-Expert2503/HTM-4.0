from transformers import pipeline
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters
# import pandas as pd

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialising Everything

logger = logging.getLogger(__name__)


Token='6644344026:AAHmKqa6mubIGELIZ-7zlFWnjrf6NhCw1nw'


li=[]
i=1


#handeling start command
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    author=update.message.from_user.first_name
    reply="Hi! 👋 {}\n\n Testing phase 2😃".format(author)
    await context.bot.send_message(chat_id=update.effective_chat.id,text=reply)
    li.append(author)
    print(author)

#handeling help command
async def help(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text="Can't help at this moment kindley contact Shivansh personally!")



# message
async def reply_text(update:Update,context : ContextTypes.DEFAULT_TYPE ):
    global i
    author=update.message.from_user.first_name
    if len(update.message.entities):
        
        for entity in update.message.entities:
            if entity['type'] == 'url':
                reply = "This is warning {}.  {} Sending links are not allowed".format(i,author)
                if i == 3:
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
                    await context.bot.send_message(chat_id=update.effective_chat.id,text="You voilated our rules")
                    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=update.message.from_user.id)
                else:
                    i = i+1
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
                    await context.bot.send_message(chat_id=update.effective_chat.id,text=reply)
    else:
        # Use a pipeline as a high-level helper
        pipe = pipeline("text-classification", model="unitary/toxic-bert")
        print(pipe(update.message.text))
        print(type(pipe(update.message.text)))
        print(pipe(update.message.text)[0])
        print(type(pipe(update.message.text)[0]))
        if pipe(update.message.text)[0]['score']>0.9:
            reply = "This is warning {}.  {} please donot use abusive words!".format(i,author)
            if i == 3:
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
                    await context.bot.send_message(chat_id=update.effective_chat.id,text="You voilated our rules")
                    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=update.message.from_user.id)
            else:
                i = i+1
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
                await context.bot.send_message(chat_id=update.effective_chat.id,text=reply)


# stickers
async def echo_sticker(update:Update,context : ContextTypes.DEFAULT_TYPE):
    global i
    author=update.message.from_user.first_name
    reply="This is warning {}.  {} Sending stickers are not allowed".format(i,author)
    if i==3:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        await context.bot.send_message(chat_id=update.effective_chat.id,text="You voilated our rules")
        await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=update.message.from_user.id)
    else:
        i=i+1
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        await context.bot.send_message(chat_id=update.effective_chat.id,text=reply)

#For unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This command doesnot exist. Please try with valid commands")

# Error handler

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) :
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)


#Main Function
def main():

    application = ApplicationBuilder().token(Token).build()
    
    #Making command handler for start
    application.add_handler(CommandHandler('start', start))
    #Making command handler for help
    application.add_handler(CommandHandler('help',help))


    #Making message handler
    application.add_handler(MessageHandler(filters.TEXT ,reply_text))
    #Making sticker handler 
    application.add_handler(MessageHandler(filters.Sticker.ALL,echo_sticker))
    #unknown command handler
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # application.add_error_handler(error)
    application.add_error_handler(error_handler)
    
    application.run_polling()


if __name__ == '__main__':
    main()

