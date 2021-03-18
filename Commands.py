def getWeather(): 
    g = geocoder.ip('me')
    lat = g.lat
    long = g.lng

    url = requests.get(f'https://api.weather.gov/points/{lat},{long}').json()["properties"]["forecast"]
    engine.say(requests.get(url).json()["properties"]["periods"][0]["detailedForecast"])
    engine.runAndWait()

def getSpeech(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust microphone sensitivty 50 (50-4000, lower is more sensitive)
    # microphone will cancel ambient noise
    with mic as source:
        audio = r.listen(source)

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

