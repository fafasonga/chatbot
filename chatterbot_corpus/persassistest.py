import os
import webbrowser
import time, datetime
from gtts import gTTS
from time import ctime
from datetime import datetime
from langdetect import detect
import speech_recognition as sr
from subprocess import Popen, PIPE, STDOUT


def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang=detect(audioString))
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Can you repeat again Please?")
    except sr.RequestError as e:
        print("System Error; {0}".format(e))

    return data


def jarvis(data):
    if "how are you" in data:
        speak("I am fine thank you")

    if "what are you doing" in data:
        speak("I am learning coding, what are you doing?")

    if "what time is it" in data:
        speak(ctime())

    if "search for" in data:
        data = data.split(" ")
        search_item = data[2]
        strURL = "https://www.google.com/search?q=" + search_item
        speak("Hold on, I will direct you on google search for " + search_item + " in the web browser")
        webbrowser.open(strURL, new=2)

    if "where is" in data:
        data = data.split(" ")
        location = data[2]
        strURL = "https://www.google.nl/maps/place/" + location
        speak("Hold on, I will show you where " + location + " is...")
        # os.system("chromium-browser https://www.google.nl/maps/place/" + location + "/&amp;")
        webbrowser.open(strURL, new=2)

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

    if "play music" or "play songs" in data:
        data = data.split(" ")
        songz = data[0]

        # cmd = input('> ')

        # music = None
        # music = Popen(
        #     'mpg321 /Users/admin/Music/iTunes/iTunes Media/Music/Unknown Artist/Unknown Album/Jason Derulo - _Try Me_ ft. J.Lo & Matoma (Official Audio).mp3'.split(
        #         ' ', 1), stdout=PIPE, stderr=STDOUT, close_fds=True)

        music = None
        cmd = songz
        if cmd.lower() == 'play':
            music = Popen(
                'mpg321 /Users/admin/Music/iTunes/iTunes Media/Music/Unknown Artist/Unknown Album/Jason Derulo - _Try Me_ ft. J.Lo & Matoma (Official Audio).mp3'.split(
                    ' ', 1), stdout=PIPE, stderr=STDOUT, close_fds=True)

# initialization
time.sleep(2)
speak("Hello fafasonga, what can I do for you?")
while 1:
    data = recordAudio()
    jarvis(data)

