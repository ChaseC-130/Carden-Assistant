import speech_recognition as sr
import subprocess, sys, time
import threading
from Commands import *


# This function is from Real Python: https://realpython.com/python-speech-recognition/#putting-it-all-together-a-guess-the-word-game
def google_speech(recognizer, microphone) -> dict:
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was successful
    "error":   `None` if no error occured, otherwise a string containing an error message if the API could not be reached or speech was unrecognizable
    "transcription": `None` if speech could not be transcribed, otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration = 0.5)
        recognizer.energy_threshold = 150
        audio = recognizer.listen(source)

    # set up the response object
    response = {"success": True,
                "error": None,
                "transcription": None}

    # try recognizing the speech in the recording if a RequestError or UnknownValueError exception is caught, update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "Sorry, I'm having connectivity issues."
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Sorry, I'm having unknown issues."

    return response


# phrases used to initiliaze Carden's listening
my_name = ['carden', 'car then', 'car den', 'carmen', 'carlin', 'pardon', 'cotton', 'are they', 'foreign']
waiting = True
recognizer = sr.Recognizer()
microphone = sr.Microphone()

phrases = {'hello': 'Hi Human',
            'test phrase:':'ok'}



def wait():
    # Listening for google speech
    print("Listening for google")
    response = google_speech(recognizer, microphone)
    pattern = response['transcription']
    if (pattern in phrases):
        say = phrases.get(pattern)
    if (say[0:4] == 'play'):
        song = say[5:]
        play_song(song)
    if (say == 'weather'):
        say = get_weather()
    get_response(say)
    play_file()

while True:

    print("Carden is waiting to be called")
    # offline listening uses pocketsphinx to listen for "carden"
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.energy_threshold = 150
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_sphinx(audio)
    except:
        response = False

    print(response)
    if (response in my_name):
        get_response("I'm listening..")
        play_file()
        print("I heard my name")
        wait()

    
