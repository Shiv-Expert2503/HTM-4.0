import os

import pymongo
import requests
import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackContext, \
    ConversationHandler
from transformers import pipeline

from logger import logging

####################################################################################################


li = []
i = 1
all_topics = [['/start', '/help', '/translate'], ['/translate_voice', '/audio_to_text'],
              ['/languages_available']]
uri = "mongodb+srv://shivansh1:A5Jgkddd8*dhSSb@cluster0.yc3hy9y.mongodb.net/?retryWrites=true&w=majority"
db_name = "coders-magglu-keee"
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

Token = '6666820551:AAH4qD0_CXR1QacZkW6UXgzI0j5RvchCKhs'


# handling start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    author = update.message.from_user.first_name
    logging.info(f'Bot Started By user {author}')
    database[colletion_name].insert_one({author: "hello there"})

    reply = "Hi! 👋 {}😃\n\n I'am all-in-one bot. I can detect spam and gives the particular user warnings, if warning exceeds more than 3 then i'll kick thet particular user. Type /command to see all commands available. \n\n Features available \n\n 1. Offensive/Faul Language Detection \n\n 2. Text_Translation \n\n 3.Voice to Text(Custom languages available) \n\n 4. Audio to Text (Custom languages available) \n\n 5. Spam Detection (Links/Stickers) \n\n 6. Image Analysis".format(
        author)
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
        text="Can't help at this moment kindly contact Shivansh personally!")


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(all_topics)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Here are all the commands',
                                   reply_markup=ReplyKeyboardMarkup(keyboard=all_topics, one_time_keyboard=True))


async def languages_available(update: Update, context: ContextTypes.DEFAULT_TYPE):
    l1 = ['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque', 'belarusian', 'bengali',
          'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)',
          'corsican', 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 'finnish',
          'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hausa',
          'hawaiian', 'hebrew', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish',
          'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'korean', 'kurdish (kurmanji)', 'kyrgyz',
          'lao', 'latin', 'latvian', 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay', 'malayalam',
          'maltese', 'maori', 'marathi', 'mongolian', 'myanmar (burmese)', 'nepali', 'norwegian', 'odia', 'pashto',
          'persian', 'polish', 'portuguese', 'punjabi', 'romanian', 'russian', 'samoan', 'scots gaelic', 'serbian',
          'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili',
          'swedish', 'tajik', 'tamil', 'telugu', 'thai', 'turkish', 'ukrainian', 'urdu', 'uyghur', 'uzbek',
          'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=l1)


# Handling translate command
async def translate(update: Update, context: CallbackContext):
    await update.message.reply_text("Please enter the text:")
    return "GET_TEXT"


async def get_trans_lang(update: Update, context: CallbackContext):
    try:
        context.user_data['text'] = str(update.message.text)
        await update.message.reply_text(
            "Please enter the language you want it to get translated(Please see languages available and type their "
            "short forms) :")
        return "GET_LANG"
    except ValueError:
        await update.message.reply_text("Invalid Language")
        return "GET_TEXT"


async def get_text(update: Update, context: CallbackContext):
    try:
        logging.info("Get Text started")
        target_language = update.message.text
        translator = Translator()
        text_to_translate = context.user_data['text']
        detected_language = translator.detect(text_to_translate).lang

        translated_text = translator.translate(text_to_translate, dest=target_language)
        logging.info(f"Original Text: {text_to_translate} (Detected Language: {detected_language})")
        logging.info(f"Translation to {target_language}: {translated_text.text}")
        await update.message.reply_text(f"The translation is {translated_text.text}")
    except ValueError:
        logging.error("Error Occurred at translation of text ")
        await update.message.reply_text("Invalid inputs.")
    return ConversationHandler.END


async def translate_voice(update: Update, context: CallbackContext):
    author = update.message.from_user.first_name
    logging.info(f"Voice Translation activated by {author}")
    await update.message.reply_text("Please input your voice:")
    return "GET_VOICE"


async def get_trans_lang_voice(update: Update, context: CallbackContext):
    try:
        author = update.message.from_user.first_name
        file_id = update.message.voice.file_id
        voice_note_file = await context.bot.get_file(file_id)
        logging.info(voice_note_file.file_path)
        logging.info(f'Voice send by {author} voice file is {voice_note_file.file_path}')
        context.user_data['voice'] = voice_note_file.file_path
        await update.message.reply_text(
            "Please enter the language you want it to get translated(Please see languages available and type their "
            "short forms) :")
        return "GET_LANG"
    except ValueError:
        await update.message.reply_text("Invalid Language")
        return "GET_VOICE"


async def get_translated_voice(update: Update, context: CallbackContext):
    author = update.message.from_user.first_name
    try:
        logging.info("Voice_translation main process started")
        target_language = update.message.text
        audio_url = context.user_data['voice']
        logging.info(audio_url)
        response = requests.get(audio_url)

        # Fetching data from the url

        if response.status_code == 200:
            with open('voice_message.ogg', 'wb') as f:
                f.write(response.content)
            ogg_file = os.path.join(os.getcwd(), 'voice_message.ogg')
            wav_file = os.path.join(os.getcwd(), 'temp_voice.wav')

            oga_file = AudioSegment.from_file(ogg_file, format="ogg")

            # Export it as a .wav file
            oga_file.export(wav_file, format="wav")
            logging.info("Exported")
            recognizer = sr.Recognizer()
            audio_file = wav_file
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)

            reply = recognizer.recognize_google(audio_data)
            translator = Translator()
            text_to_translate = reply
            detected_language = translator.detect(text_to_translate).lang
            translated_text = translator.translate(text_to_translate, dest=target_language)
            logging.info(f"{author} Original Text: {text_to_translate} (Detected Language: {detected_language})")
            logging.info(f"{author} Translation to {target_language}: {translated_text.text}")
            await update.message.reply_text(f"The translation is {translated_text.text}")
            os.remove(ogg_file)
            os.remove(wav_file)
            logging.info("Removed")
    except Exception as e:
        await update.message.reply_text("Invalid inputs.")
        logging.error("Error while translating", exc_info=context.error)
    return ConversationHandler.END


async def translate_audio(update: Update, context: CallbackContext):
    author = update.message.from_user.first_name
    logging.info(f"Audio translation started by {author}")
    await update.message.reply_text("Please input audio: ")
    return "GET_AUDIO"


async def get_trans_lang_audio(update: Update, context: CallbackContext):
    author = update.message.from_user.first_name
    try:
        file_id = update.message.audio.file_id
        audio_note_file = await context.bot.get_file(file_id)
        logging.info(audio_note_file.file_path)
        logging.info(f'Audio send by {author} audio file is {audio_note_file.file_path}')
        audio_url = audio_note_file.file_path
        context.user_data['audio'] = audio_url
        await update.message.reply_text(
            "Please enter the language you want it to get translated(Please see languages available and type their "
            "short forms) :")
        return "GET_LANG"
    except ValueError:
        logging.info("User didn't entered the right language")
        await update.message.reply_text("Invalid Language")
        return "GET_AUDIO"


async def get_translated_audio(update: Update, context: CallbackContext):
    author = update.message.from_user.first_name
    try:
        logging.info("Main Translation Started")
        target_language = update.message.text
        audio_url = context.user_data['audio']
        logging.info(audio_url)
        response = requests.get(audio_url)
        # Fetching data from the url
        if response.status_code == 200:
            with open('audio_message.mp3', 'wb') as f:
                f.write(response.content)
            mp3_file_path = os.path.join(os.getcwd(), 'audio_message.mp3')
            wav_file = os.path.join(os.getcwd(), 'temp_audio.wav')

            mp3_file = AudioSegment.from_file(mp3_file_path, format="mp3")
            mp3_file.export(wav_file, format="wav")
            logging.info("Exported")
            recognizer = sr.Recognizer()
            audio_file = wav_file
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
            reply = recognizer.recognize_google(audio_data)
            translator = Translator()
            text_to_translate = reply
            detected_language = translator.detect(text_to_translate).lang
            # print(target_language)
            translated_text = translator.translate(text_to_translate, dest=target_language)
            logging.info(f"{author} Original Text: {text_to_translate} (Detected Language: {detected_language})")
            logging.info(f"{author} Translation to {target_language}: {translated_text.text}")
            await update.message.reply_text(f"The translation is {translated_text.text}")
            try:
                os.remove(mp3_file_path)
                os.remove(wav_file)
                logging.info("Removed")
            except Exception as e:
                logging.info("Error While Removing directary")

    except Exception as e:
        await update.message.reply_text("Invalid inputs.")
        logging.error("Error while translating", exc_info=context.error)
    return ConversationHandler.END


async def report(update: Update, context: CallbackContext):
    author = update.message.from_user.first_name
    logging.info(f"Report command started by {author}")
    await update.message.reply_text("Enter the username: ")
    return "GET_USERNAME"


async def make_report(update: Update, context: CallbackContext):
    author = update.message.from_user.first_name
    try:
        logging.info("Main Report started")
        username = update.message.text
        chat = await context.bot.get_chat(username)
        user_id = chat.id
        await update.message.reply_text(f"User is {user_id}")
        user_data = database[colletion_name].find_one(
            {"user_id": update.message.from_user.id})
        if not user_data:
            user_data = {"user_id": update.message.from_user.id, "user_name": author, "warnings": 0}
            database[colletion_name].insert_one(user_data)
        warnings = user_data["warnings"]
        database[colletion_name].update_one(
            {"user_id": update.message.from_user.id},
            {"$set": {
                "warnings": warnings + 1
            }})
        # print(warnings)
    except ValueError:
        logging.error(f"Error occurred while reporting done by {author}", exc_info=context.error)
        await update.message.reply_text("Invalid inputs.")
    return ConversationHandler.END


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
            # Translating the text
            translator = Translator()
            text_to_translate = update.message.text
            detected_language = translator.detect(text_to_translate).lang

            target_language = 'hi'
            if detected_language != 'en':
                translated_text = translator.translate(text_to_translate, dest=target_language)
                logging.info(f"Original Text: {text_to_translate} (Detected Language: {detected_language})")
                logging.info(f"Translation to {target_language}: {translated_text.text}")
                # Use a pipeline as a high-level helper
                # Converting hindi translated text to english for its checking via transformer
                pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")
                logging.info(pipe(translated_text.text))

                # Passing translated english text to toxic checking
                pipe = pipeline("text-classification", model="unitary/toxic-bert")
                logging.info(f'{pipe(translated_text.text)[0]} by {author}')
                if pipe(translated_text.text)[0]['score'] > 0.85:
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
            else:
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
        logging.info(f"Voice processing initiated by {author}")
        file_id = update.message.voice.file_id
        voice_note_file = await context.bot.get_file(file_id)
        logging.info(voice_note_file.file_path)
        logging.info(f'Voice send by {author} voice file is {voice_note_file.file_path}')

        audio_url = voice_note_file.file_path
        response = requests.get(audio_url)

        # Fetching data from the url

        if response.status_code == 200:
            with open('voice_message.ogg', 'wb') as f:
                f.write(response.content)
            ogg_file = os.path.join(os.getcwd(), 'voice_message.ogg')
            wav_file = os.path.join(os.getcwd(), 'temp_voice.wav')
            oga_file = AudioSegment.from_file(ogg_file, format="ogg")

            # Export it as a .wav file
            oga_file.export(wav_file, format="wav")
            logging.info("Exported")
            recognizer = sr.Recognizer()
            audio_file = wav_file
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)

            # Trying audio analysis
            try:
                reply = recognizer.recognize_google(audio_data)
                try:
                    pipe = pipeline("text-classification", model="unitary/toxic-bert")
                    logging.info(f'{pipe(reply)[0]} by {author}')
                    if pipe(reply)[0]['score'] > 0.85:
                        reply = "This is warning.  {} you used--> {} words which are offencive!".format(author, reply)
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text=reply)
                    else:
                        reply = "You said --> {}".format(reply)
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text=reply)
                except Exception as e:
                    logging.error(f'Error occurred while handling the text by user {author}', exc_info=context.error)
            except sr.UnknownValueError:
                logging.info("Google Web Speech Recognition could not understand voice")

            os.remove(ogg_file)
            os.remove(wav_file)
        else:
            logging.info(f"Failed to download the audio. Status code: {response.status_code}")

    except Exception as e:
        logging.error(f'Error while handling voice by {author} {e}', exc_info=context.error)


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    author = update.message.from_user.first_name
    try:
        logging.info(f"Image processing initiated by {author}")
        pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
        logging.info(update.message.photo[-1])
        image_id = update.message.photo[-1].file_id
        image_file = await context.bot.get_file(image_id)
        image_data = pipe(image_file.file_path)[0]['generated_text']

        pipe2 = pipeline("text-classification", model="unitary/toxic-bert")
        logging.info(f'{pipe2(image_data)[0]} by {author}')
        if pipe2(image_data)[0]['score'] > 0.85:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Your image implies to {image_data} which is toxic!")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your image implies to {image_data}")

    except Exception as e:
        logging.error(f"Error occurred while analysing photo{e}", exc_info=context.error)


# Audio  //Same as voice but the difference is here its .mp3 not .ogg
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    author = update.message.from_user.first_name
    try:
        logging.info(f"Audio processing initiated by {author}")
        file_id = update.message.audio.file_id
        audio_note_file = await context.bot.get_file(file_id)
        logging.info(f'Audio send by {author} audio file is {audio_note_file.file_path}')
        audio_url = audio_note_file.file_path
        response = requests.get(audio_url, stream=True)

        if response.status_code == 200:
            with open('audio_message.mp3', 'wb') as f:
                f.write(response.content)
            mp3_file_path = os.path.join(os.getcwd(), 'audio_message.mp3')
            wav_file = os.path.join(os.getcwd(), 'temp_audio.wav')
            mp3_file = AudioSegment.from_file(mp3_file_path, format="mp3")
            mp3_file.export(wav_file, format="wav")
            logging.info("Exported")
            recognizer = sr.Recognizer()
            audio_file = wav_file
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)

            try:
                reply = recognizer.recognize_google(audio_data)
                logging.info(reply)
                try:
                    pipe = pipeline("text-classification", model="unitary/toxic-bert")
                    logging.info(f'{pipe(reply)[0]} by {author}')

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
                logging.info("Google Web Speech Recognition could not understand audio")
            os.remove(mp3_file)
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

    application.add_handler(CommandHandler('command', command))

    application.add_handler(CommandHandler('languages_available', languages_available))

    # Making command handler for translate
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('translate', translate)],
        states={
            "GET_TEXT": [MessageHandler(filters.TEXT & ~filters.COMMAND, get_trans_lang)],
            "GET_LANG": [MessageHandler(filters.TEXT & ~filters.COMMAND, get_text)]
        },
        fallbacks=[],
    )

    application.add_handler(conversation_handler)

    report_handler = ConversationHandler(
        entry_points=[CommandHandler('report', report)],
        states={
            "GET_USERNAME": [MessageHandler(filters.TEXT & ~filters.COMMAND, make_report)],
        },
        fallbacks=[],
    )
    # To be completed by VARDAAN<=============================================================================
    application.add_handler(report_handler)

    conversation_handler_voice = ConversationHandler(
        entry_points=[CommandHandler('translate_voice', translate_voice)],
        states={
            "GET_VOICE": [MessageHandler(filters.VOICE & ~filters.COMMAND, get_trans_lang_voice)],
            "GET_LANG": [MessageHandler(filters.TEXT & ~filters.COMMAND, get_translated_voice)]
        },
        fallbacks=[],
    )

    application.add_handler(conversation_handler_voice)

    conversation_handler_audio = ConversationHandler(
        entry_points=[CommandHandler('audio_to_text', translate_audio)],
        states={
            "GET_AUDIO": [MessageHandler(filters.AUDIO & ~filters.COMMAND, get_trans_lang_audio)],
            "GET_LANG": [MessageHandler(filters.TEXT & ~filters.COMMAND, get_translated_audio)]
        },
        fallbacks=[],
    )

    application.add_handler(conversation_handler_audio)

    # Making message handler
    application.add_handler(MessageHandler(filters.TEXT, reply_text))
    # Making sticker handler
    application.add_handler(MessageHandler(filters.Sticker.ALL, echo_sticker))
    application.add_handler(MessageHandler(filters.PHOTO, photo))
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
