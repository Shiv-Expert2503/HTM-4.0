from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import pymongo
from logger import logging
import os
import requests
from transformers import pipeline
from pydub import AudioSegment
import speech_recognition as sr

####################################################################################################


li = []
i = 1

uri = "mongodb+srv://shivansh1:A5Jgkddd8*dhSSb@cluster0.yc3hy9y.mongodb.net/?retryWrites=true&w=majority"
db_name = "coders-magloo-ke"
# Create a new client and connect to the server
client = pymongo.MongoClient(uri)
database = client[db_name]
colletion_name = "harry-puttar"

try:
    client.admin.command('ping')
    logging.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    logging.info("Error Occurred while setting the connection")

#################################################################################################

# Initialising Everything

Token = '6644344026:AAHmKqa6mubIGELIZ-7zlFWnjrf6NhCw1nw'


async def reply_custom_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text):
    author = update.message.from_user.first_name
    try:
        pipe = pipeline("text-classification", model="unitary/toxic-bert")
        logging.info(f'{pipe(text)[0]} by {author}')
        print(pipe(text)[0])
        if pipe(text)[0]['score'] > 0.85:
            reply = "This is warning.  {} please don't use abusive words!".format(author)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=reply)
    except Exception as e:
        logging.error(f'Error occurred while handling the text by user {author}', exc_info=context.error)


# handeling start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    author = update.message.from_user.first_name
    logging.info(f'Bot Started By user {author}')
    database[colletion_name].insert_one({author: "hello there"})

    reply = "Hi! 👋 {}\n\n Testing phase 2😃".format(author)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=reply)
    li.append(author)
    logging.info(f"DM by {author}")


# handling help command
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    author = update.message.from_user.first_name
    logging.info(f"Help command activated by user {author}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Can't help at this moment kindley contact Shivansh personally!")


# message
async def reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    author = update.message.from_user.first_name
    try:
        logging.info(f'Text by user {author}, text is {update.message.text}')
        # Check if the user exists in the database, if not add the user
        user_data = database[colletion_name].find_one(
            {"user_id": update.message.from_user.id})
        if not user_data:
            user_data = {"user_id": update.message.from_user.id, "user_name": author, "warnings": 0}
            database[colletion_name].insert_one(user_data)

        warnings = user_data["warnings"]

        # code for handling links and abusive words...
        if len(update.message.entities):
            for entity in update.message.entities:
                if entity['type'] == 'url':
                    logging.info(f"{author} has send a link {update.message.text}")
                    reply = "This is warning {}.  {} Sending links are not allowed".format(
                        warnings, author)
                    if warnings > 2:
                        await context.bot.delete_message(
                            chat_id=update.effective_chat.id,
                            message_id=update.message.message_id)
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text="You violated our rules")
                        try:
                            await context.bot.ban_chat_member(
                                chat_id=update.effective_chat.id,
                                user_id=update.message.from_user.id)
                            logging.info(f"Removed {author}")
                        except Exception as e:
                            logging.error(f'Error removing {author}', exc_info=context.error)
                    else:
                        warnings += 1
                        await context.bot.delete_message(
                            chat_id=update.effective_chat.id,
                            message_id=update.message.message_id)
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text=reply)
        else:
            # Use a pipeline as a high-level helper
            pipe = pipeline("text-classification", model="unitary/toxic-bert")
            logging.info(f'{pipe(update.message.text)[0]} by {author}')
            if pipe(update.message.text)[0]['score'] > 0.85:
                reply = "This is warning {}.  {} please don't use abusive words!".format(
                    warnings + 1, author)
                database[colletion_name].update_one(
                    {"user_id": update.message.from_user.id},
                    {"$set": {
                        "warnings": warnings + 1
                    }})
                if warnings > 2:
                    try:
                        await context.bot.delete_message(chat_id=update.effective_chat.id,
                                                         message_id=update.message.message_id)
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text="You violated our rules")
                        logging.info(f"Removed {author}")
                        await context.bot.ban_chat_member(chat_id=update.effective_chat.id,
                                                          user_id=update.message.from_user.id)
                        database[colletion_name].delete_one({"user_id": update.message.from_user.id})
                    except Exception as e:
                        logging.error(f'Error removing {author}', exc_info=context.error)
                else:
                    await context.bot.delete_message(chat_id=update.effective_chat.id,
                                                     message_id=update.message.message_id)
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text=reply)
    except Exception as e:
        logging.error(f'Error occurred while handling the text by user {author}', exc_info=context.error)


# stickers
async def echo_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    author = update.message.from_user.first_name
    try:

        # Check if the user exists in the database, if not add the user
        user_data = database[colletion_name].find_one(
            {"user_id": update.message.from_user.id})
        if not user_data:
            user_data = {"user_id": update.message.from_user.id, "user_name": author, "warnings": 0}
            database[colletion_name].insert_one(user_data)

        warnings = user_data["warnings"]

        # Your existing code for handling stickers...
        reply = "This is warning {}.  {} Sending stickers are not allowed".format(
            warnings + 1, author)
        if warnings > 2:
            try:
                await context.bot.delete_message(chat_id=update.effective_chat.id,
                                                 message_id=update.message.message_id)
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="You violated our rules")
                await context.bot.ban_chat_member(chat_id=update.effective_chat.id,
                                                  user_id=update.message.from_user.id)
                logging.info(f"Removed {author}")
                database[colletion_name].delete_one({"user_id": update.message.from_user.id})
            except Exception as e:
                logging.error(f'Error removing {author}', exc_info=context.error)
        else:
            await context.bot.delete_message(chat_id=update.effective_chat.id,
                                             message_id=update.message.message_id)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=reply)

        # Update the warning counter for the user
        database[colletion_name].update_one({"user_id": update.message.from_user.id},
                                            {"$set": {
                                                "warnings": warnings + 1
                                            }})
    except Exception as e:
        logging.error(f'Error occurred while handling sticker by user {author}', exc_info=context.error)


# Voice
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    author = update.message.from_user.first_name
    try:
        file_id = update.message.voice.file_id
        voice_note_file = await context.bot.get_file(file_id)
        # voice_note_file.download(os.path.join(os.getcwd(),'voice_message.ogg'))
        print(voice_note_file.file_path)
        logging.info(f'Voice send by {author} voice file is {voice_note_file.file_path}')

        audio_url = voice_note_file.file_path
        response = requests.get(audio_url)

        if response.status_code == 200:
            with open('voice_message.ogg', 'wb') as f:
                f.write(response.content)
            ogg_file = os.path.join(os.getcwd(), 'voice_message.ogg')
            wav_file = os.path.join(os.getcwd(), 'temp_voice.wav')
            print(ogg_file)
            print(wav_file)
            oga_file = AudioSegment.from_file(ogg_file, format="ogg")

            # Export it as a .wav file
            oga_file.export(wav_file, format="wav")
            # audio_data, sample_rate = librosa.load('temp_audio.mp3', sr=None)

            print("Exported")
            # np.save('audio_array.npy', audio_data)
            recognizer = sr.Recognizer()
            audio_file = wav_file
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)

            try:
                reply = recognizer.recognize_google(audio_data)  # Use Google Web Speech API
                print(reply)
                try:
                    pipe = pipeline("text-classification", model="unitary/toxic-bert")
                    logging.info(f'{pipe(reply)[0]} by {author}')
                    print(pipe(reply)[0])
                    if pipe(reply)[0]['score'] > 0.85:
                        reply = "This is warning.  {} you used--> {} words which are offencive!".format(author, reply)
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text=reply)
                    else:
                        reply = "You said --> {}".format( reply)
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text=reply)
                except Exception as e:
                    logging.error(f'Error occurred while handling the text by user {author}', exc_info=context.error)
            except sr.UnknownValueError:
                print("Google Web Speech Recognition could not understand voice")

            os.remove(ogg_file)
            os.remove(wav_file)
        else:
            logging.info(f"Failed to download the audio. Status code: {response.status_code}")

    except Exception as e:
        logging.error(f'Error while handling voice by {author} {e}', exc_info=context.error)


# Audio
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    author = update.message.from_user.first_name
    try:
        file_id = update.message.audio.file_id
        audio_note_file = await context.bot.get_file(file_id)
        print(audio_note_file.file_path)
        logging.info(f'Audio send by {author} audio file is {audio_note_file.file_path}')
        audio_url = audio_note_file.file_path
        response = requests.get(audio_url, stream=True)

        if response.status_code == 200:
            with open('audio_message.mp3', 'wb') as f:
                f.write(response.content)
            mp3_file_path = os.path.join(os.getcwd(), 'audio_message.mp3')
            wav_file = os.path.join(os.getcwd(), 'temp_audio.wav')
            print(mp3_file_path)
            print(wav_file)
            mp3_file = AudioSegment.from_file(mp3_file_path, format="mp3")
            mp3_file.export(wav_file, format="wav")
            print("Exported")
            recognizer = sr.Recognizer()
            audio_file = wav_file
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)

            try:
                reply = recognizer.recognize_google(audio_data)  # Use Google Web Speech API
                print(reply)
                try:
                    pipe = pipeline("text-classification", model="unitary/toxic-bert")
                    logging.info(f'{pipe(reply)[0]} by {author}')
                    print(pipe(reply)[0])
                    if pipe(reply)[0]['score'] > 0.85:
                        reply = "This is warning.  {} you used --> {} words which are offencive!".format(author, reply)
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text=reply)
                    else:
                        reply = "You said --> {}".format(reply)
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text=reply)
                except Exception as e:
                    logging.error(f'Error occurred while handling the text by user {author}', exc_info=context.error)
            except sr.UnknownValueError:
                print("Google Web Speech Recognition could not understand audio")
            os.remove(mp3_file_path)
            os.remove(wav_file)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Your audio is {reply}")
        else:
            logging.info(f"Failed to download the audio. Status code: {response.status_code}")


    except Exception as e:
        logging.error(f'Error while handling audio by {author} {e}', exc_info=context.error)


# For unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="This command doesn't exist. Please try with valid commands")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Exception while handling an update:", exc_info=context.error)


# Main Function
def main():
    application = ApplicationBuilder().token(Token).build()

    # Making command handler for start
    application.add_handler(CommandHandler('start', start))
    # Making command handler for help
    application.add_handler(CommandHandler('help', help))
    # Making report handler for report
    # application.add_handler(CommandHandler('report', report))

    # Making message handler
    application.add_handler(MessageHandler(filters.TEXT, reply_text))
    # Making sticker handler
    application.add_handler(MessageHandler(filters.Sticker.ALL, echo_sticker))
    # Making voice handler
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    # Making voice handler
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    # application.add_error_handler(error)
    application.add_error_handler(error_handler)
    # unknown command handler
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    print('Application Started')
    application.run_polling()


if __name__ == '__main__':
    main()
