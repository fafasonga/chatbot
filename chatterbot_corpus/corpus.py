import os
import io
import glob
import yaml
from gtts import gTTS
import time, datetime
from time import ctime
from langdetect import detect
from datetime import datetime
from chatterbot import ChatBot
import speech_recognition as sr
from subprocess import Popen, PIPE, STDOUT
from chatterbot.trainers import ListTrainer


DIALOG_MAXIMUM_CHARACTER_LENGTH = 400
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATA_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'data/english/')

bot = ChatBot('Bot')
bot.set_trainer(ListTrainer)


class CorpusObject(list):
    """
    This is a proxy object that allow additional
    attributes to be added to the collections of
    data that get returned by the corpus reader.
    """

    def __init__(self, *args, **kwargs):
        """
        Imitate a list by allowing a value to be passed in.
        """
        if args:
            super(CorpusObject, self).__init__(args[0])
        else:
            super(CorpusObject, self).__init__()

        self.categories = []


def speak(audioString):
    print(audioString)
    # tts = gTTS(text=audioString, lang=detect(audioString))
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nSay something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("\nCan you repeat again Please?")
    except sr.RequestError as e:
        print("\nSystem Error; {0}".format(e))

    return data


def jarvis(data):
    if "what time is it" in data:
        speak(ctime())

    bye_path = os.getcwd() + "/bye.dat"
    f_bye = open(bye_path, "r")
    bye_list = f_bye.read().strip().split("\n")
    for i in range(len(bye_list)):
        if bye_list[i] in data:
            time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if int(time_now[11:13]) > 18 or int(time_now[11:13]) < 4:
                speak("Goodnight.")
                exit()
            else:
                speak('See you later then! Have a good day!')
                exit()

    f_bye.close()


def get_file_path(dotted_path, extension='json'):
    """
    Reads a dotted file path and returns the file path.
    """
    # If the operating system's file path seperator character is in the string
    if os.sep in dotted_path or '/' in dotted_path:
        # Assume the path is a valid file path
        return dotted_path

    parts = dotted_path.split('.')
    if parts[0] == 'chatterbot':
        parts.pop(0)
        parts[0] = DATA_DIRECTORY

    corpus_path = os.path.join(*parts)

    if os.path.exists(corpus_path + '.{}'.format(extension)):
        corpus_path += '.{}'.format(extension)

    return corpus_path


def read_corpus(file_name):
    """
    Read and return the data from a corpus json file.
    """
    with io.open(file_name, encoding='utf-8') as data_file:
        data = yaml.load(data_file)
        # print(data)
        return data


def list_corpus_files(dotted_path):
    """
    Return a list of file paths to each data file in
    the specified corpus.
    """
    CORPUS_EXTENSION = 'yml'

    corpus_path = get_file_path(dotted_path, extension=CORPUS_EXTENSION)
    paths = []

    if os.path.isdir(corpus_path):
        paths = glob.glob(corpus_path + '/**/*.' + CORPUS_EXTENSION, recursive=True)
        # print("Path = ", paths)
    else:
        paths.append(corpus_path)

    paths.sort()
    # print("Paths Final : ", paths)
    return paths


def load_corpus(dotted_path):
    """
    Return the data contained within a specified corpus.
    """
    data_file_paths = list_corpus_files(dotted_path)

    corpora = []

    for file_path in data_file_paths:
        corpus = CorpusObject()
        corpus_data = read_corpus(file_path)

        conversations = corpus_data.get('conversations', [])
        corpus.categories = corpus_data.get('categories', [])
        corpus.extend(conversations)

        corpora.append(corpus)
        bot.train(corpora)
        # print(corpora)

    return corpora


# load_corpus(DATA_DIRECTORY)
path = list_corpus_files(DATA_DIRECTORY)


for files in os.listdir(DATA_DIRECTORY):
    data = open(DATA_DIRECTORY + files, 'r').readlines()
    bot.train(data)

time.sleep(2)
print("\n")
speak("Hello fafasonga, what can I do for you?")
# speak("salut! fafasonga, comment puis-je t'aidé")

while True:
    data = recordAudio()
    jarvis(data)

    # message = data
    message = input("You -: ")
    reply = bot.get_response(message)
    print('ChatBot -: ', reply)
