import pyttsx3
import speech_recognition as sr
import sys
import subprocess


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
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


my_phrases = {'hello': ['Hi!, How are you?', None],
              'who are you': ['I am Elsi, voice assistant', None],
              'what can you do': ["I can turn on film or music, open application and that's all :)", None],
              'how can I call you?': ['You can call me Elsi', None],
              'stop': ['Turning off', 'exit'],
              'exit': ['Goodbye ;)', 'exit'],
              'turn off': ['One moment please...', 'exit'],
              'telegram': ['One moment', telegram],
              'open telegram': ['Opening....', telegram],
              'Elsi open telegram': ['Yes sir', telegram],
              'viber': ['One moment', viber],
              'open viber': ['Opening....', viber]}

unknown_command_phrase = ["Didn't catch it, repeat please", None]

engine = pyttsx3.init()

en_voice_id_m = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
en_voice_id_f = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
gb_voice_id_f = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"

voices = engine.getProperty('voices')
engine.setProperty('voice', en_voice_id_f)
engine.setProperty('rate', 195)
#engine.say("Hello. I'm Elsi, your voice assistant. I can do anything u want")
while True:
    engine.runAndWait()
    
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print("Say something!")
    # call function
    response = recognize_speech_from_mic(recognizer, microphone)
    pattern = response['transcription']  # get transcription from response dict
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