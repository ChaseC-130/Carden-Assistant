import geocoder, pyttsx3, requests, json
import speech_recognition as sr
from Commands import *


keywords = {}
engine = pyttsx3.init()
engine.setProperty('rate', 195)

phrases = {}

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