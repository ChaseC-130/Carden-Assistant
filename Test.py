import pyttsx3
import speech_recognition as sr
import sys
import subprocess
from Commands import *


# This function is from Real Python: https://realpython.com/python-speech-recognition/#putting-it-all-together-a-guess-the-word-game
def recognize_speech_from_mic(recognizer, microphone) -> dict:
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
        recognizer.energy_threshold(50)
        audio = recognizer.listen(source)

    # set up the response object
    response = {"success": True,
                "error": None,
                "transcription": None}

    # try recognizing the speech in the recording if a RequestError or UnknownValueError exception is caught, update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_sphinx(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


conversions = {'weather' : ['weather', 'whether', 'wet her', 'where there']}


my_phrases = {'hello': ['Hi!, How are you?', None],
              'who are you': ['I am Carden', None],
              'weather' : [getWeather(), None]
              }

unknown_command_phrase = ["Sorry, I don't understand", None]

engine = pyttsx3.init()

engine.setProperty('rate', 125)

while True:
    engine.runAndWait()
    
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print("Say something!")
    # call function
    response = recognize_speech_from_mic(recognizer, microphone)
    pattern = response['transcription']  # get transcription from response dict
    if not (pattern in my_phrases):
        for x in conversions:
            if (pattern == conversions[x]):
                pattern = conversions.index(x)
    say, command = my_phrases.get(pattern, unknown_command_phrase)  # retrieve response from my_phrases
    engine = pyttsx3.init()
    engine.say(say)
    if command == None:
        print(f'The response returned by the speech recognition engine was:\n{pattern}.\n')
        pass
    elif command == 'exit':
        sys.exit()
    else: 
        subprocess.check_output(command, shell=True)  # assumes you have these properly configured
        pass