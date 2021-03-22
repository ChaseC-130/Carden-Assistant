import geocoder, requests, json, boto3, vlc, time, spotipy
from spotipy.oauth2 import SpotifyClientCredentials




def play_song(song):
    # uses environment variables SPOTIPY_CLIENT_ID 
    # and SPOTIPY_CLIENT_SECRET
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    sp.start_playback(uris=['spotify:track:6rqhFgbbKwnb9MLmUQDhG6'])

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