def getWeather(): 
    g = geocoder.ip('me')
    lat = g.lat
    long = g.lng
    url = requests.get(f'https://api.weather.gov/points/{lat},{long}').json()["properties"]["forecast"]
    return requests.get(url).json()["properties"]["periods"][0]["detailedForecast"]
    


