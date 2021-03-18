import pyttsx3
import speech_recognition as sr
from Commands import *

def getSpeech(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust microphone sensitivty 50 (50-4000, lower is more sensitive)
    # microphone will cancel ambient noise
    with microphone as source:
        audio = recognizer.listen(source)

    # set up object to respond
    response = {
        "success" : True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_sphinx(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "I'm sorry, it appears I am having technical issues."
    except sr.UnknownValueError:
        # couldn't understand
        response["error"] = "I'm sorry, I didn't get that."

    return response



keywords = {}
engine = pyttsx3.init()
engine.setProperty('rate', 195)

phrases = {'Carden' : ["I'm listening..."],
        'Weather' : [getWeather()]}

# main loop
while True:
    engine.runAndWait()
    r = sr.Recognizer()
    r.energy_sthreshold = 50
    r.adjust_for_ambient_noise(source)
    mic = sr.Microphone(device_index=1)

    response = getSpeech(r, mic)
    pattern = response['transcription']
    if (phrases.contains(pattern)):
        engine.say(phrase.get(pattern))
    else:
        engine.say("Sorry, I didn't get that.")
    engine = pyttsx3.init()
    engine.say(say)