import geocoder, requests, json, boto3, vlc, pafy
from youtube_search import YoutubeSearch



def stop():
    if (media.is_playing()):
        media.stop()

def play_song(song):
    result = json.loads(YoutubeSearch(song, max_results=1).to_json())
    print(result)
    url = 'https://www.youtube.com' + result['videos'][0]['url_suffix']
    video = pafy.new(url)
    best = video.getbestaudio()
    media = vlc.MediaPlayer(best.url)
    media.play()

def get_response(text):
    polly_client = boto3.Session().client('polly')
    response = polly_client.synthesize_speech(VoiceId='Joey',
            OutputFormat='mp3',
            Text = text)

    file = open('speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()

def get_weather(): 
    g = geocoder.ip('me')
    lat = g.lat
    long = g.lng
    url = requests.get(f'https://api.weather.gov/points/{lat},{long}').json()["properties"]["forecast"]
    return requests.get(url).json()["properties"]["periods"][0]["detailedForecast"]
    
def play_file():
    media = vlc.MediaPlayer('speech.mp3')
    media.play()