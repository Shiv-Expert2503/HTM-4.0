import logging
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters
import os
import pandas as pd
import re

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialising Everything

logger=logging.getLogger(__name__)


Token='6644344026:AAHmKqa6mubIGELIZ-7zlFWnjrf6NhCw1nw'

all_topics=[['World', 'Nation', 'Entertainment'], ['Sports', 'Science', 'Health'],['Business', 'Technology']]


li=[]



#handeling start command
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    author=update.message.from_user.first_name
    reply="Hi! 👋 {}\n\n This is Testing phase one😃".format(author)
    await context.bot.send_message(chat_id=update.effective_chat.id,text=reply)
    # li=[]
    li.append(author)
    print(author)


#handeling help command
async def help(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text="Can't help at this moment kindley contact Shivansh personally!")



#echoing message
async def reply_text(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text=update.message.text)

#echoing stickers
async def echo_sticker(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_sticker(chat_id=update.effective_chat.id,sticker=update.message.sticker.file_id)


#echoing audio
async def echo_audio(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_audio(chat_id=update.effective_chat.id,audio=update.message.audio)

#echoing video
async def echo_video(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_video(chat_id=update.effective_chat.id,video=update.message.video.file_id)

#echoing voice
async def echo_voice(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_voice(chat_id=update.effective_chat.id,voice=update.message.voice.file_id)

#echoing photo
async def echo_photo(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id,photo=update.message.photo[-1])

#echoing video note
async def echo_video_note(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_video_note(chat_id=update.effective_chat.id,video_note=update.message.video_note.file_id)

#For unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# Error handler

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) :
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)


# def error(update:Update,context : ContextTypes.DEFAULT_TYPE):
#     logger.error("Update caused error ")

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
    #Making audio handler 
    application.add_handler(MessageHandler(filters.AUDIO,echo_audio))
    #Making video handler
    application.add_handler(MessageHandler(filters.VIDEO,echo_video))
    #Making voice handler
    application.add_handler(MessageHandler(filters.VOICE,echo_voice))
    #Making photo handler
    application.add_handler(MessageHandler(filters.PHOTO,echo_photo))
    #Making video note handler
    application.add_handler(MessageHandler(filters.VIDEO_NOTE,echo_video_note))

    #unknown command handler
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # application.add_error_handler(error)
    application.add_error_handler(error_handler)
    
    application.run_polling()


if __name__ == '__main__':
    main()

