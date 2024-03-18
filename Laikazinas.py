import requests
pilseta = input("Ievadiet pilsetu:")
geo= requests.get('http://api.openweathermap.org/geo/1.0/direct?q={pilseta}&limit=5&appid=d5f36631cc643ceb4aca81a4466d58e1').json()[0]
kord= [geo['lat'], geo['lon']]
print(geo)


laikapst= requests.get('https://api.tomorrow.io/v4/weather/forecast?location={kord}&apikey=daDpfCTk68foELkxKjdeWq6WyPSTEdCC').json()

