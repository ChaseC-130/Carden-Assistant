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
        recognizer.adjust_for_ambient_noise(source)
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

unknown = ["Sorry, I didn't get that."]
phrases = {'hello': ['Hi human', None],
        'weather': [get_weather, None]}

while waiting:
    print("Carden is waiting to be called")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer.energy_threshold = 150
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_sphinx(audio)
    except:
        response = False

    print(response)
    if (response in my_name):
        
        waiting = False
        get_response("I'm listening..")
        play_file()
        print("I heard my name")
while not waiting:
    # Listening for google speech
    response = google_speech(recognizer, microphone)
    pattern = response['transcription']
    say, command = phrases.get(pattern, unknown)
    if (say == get_weather()):
        say = get_weather()
    get_response(say)
    time.sleep(3)
    #thread.start_new_thread(play_file(), ())
    t1 = threading.Thread(target = play_file())
    waiting = True