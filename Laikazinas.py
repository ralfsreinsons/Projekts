import requests
pilseta = input("Ievadiet pilsetu:")
geo= requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + pilseta +'&limit=1&appid=d5f36631cc643ceb4aca81a4466d58e1').json()[0]

lat= geo['lat']  
lon= geo['lon']

laikapst= requests.get('https://api.tomorrow.io/v4/weather/forecast?location=' + str(lat) + ',' +  str(lon) +'&apikey=daDpfCTk68foELkxKjdeWq6WyPSTEdCC').json()

print(laikapst)