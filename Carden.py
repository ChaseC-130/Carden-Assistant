import speech_recognition as sr
import subprocess, sys, time
import threading
import Commands



def google_speech(recognizer, microphone) -> dict:
    # adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration = 0.5)
        recognizer.energy_threshold = 150
        audio = recognizer.listen(source)

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
my_name = ['carl', 'carlin', 'garden', 'carden', 'car then', 'car den', 'carmen', 'carlin', 'pardon', 'cotton', 'are they', 'foreign']
recognizer = sr.Recognizer()
microphone = sr.Microphone()

phrases = {'hello': 'Hi Human',
            'weather': 'get_weather()'}



def wait():
    # Listening for google speech
    print("Listening for google")
    response = google_speech(recognizer, microphone)
    pattern = response['transcription']
    
    if (pattern in phrases):
        say = phrases.get(pattern)
    else:
        say = pattern



    if (say[0:4] == 'play'):
        song = say[5:]
        play_song(song)
    else:
        if (say in dir(Commands)):
            say = eval(say)
        get_response(say)
        play_file()
    

while True:
    print("Carden is waiting to be called")
    # offline listening uses pocketsphinx to listen for "carden"
    with microphone as source:
        #recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.energy_threshold = 150
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_sphinx(audio)
    except:
        response = False
    words = response.split(" ")
    print(words)
    
    for word in words:
        if (word in my_name):
            get_response("I'm listening..")
            play_file()
            print("I heard my name")
            wait()


    
