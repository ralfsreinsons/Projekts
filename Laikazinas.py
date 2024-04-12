import requests
pilseta = input("Ievadiet pilsetu:")
geo= requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + pilseta +'&limit=1&appid=d5f36631cc643ceb4aca81a4466d58e1').json()[0]

lat= geo['lat']  
lon= geo['lon']

laikazinas = requests.get('http://api.openweathermap.org/data/2.5/forecast?lat=' + str(lat)+'&lon='+ str(lon)+ '&units=metric&appid=d5f36631cc643ceb4aca81a4466d58e1').json()
saule = requests.get('https://api.sunrise-sunset.org/json?lat='+ str(lat)+'&lng=' + str(lon) +'&date=today').json()['results']

saullekts = saule['sunrise']
saulriets= saule['sunset']
dienas_gar = saule['day_length']



piej_laikapstakli= ["temperatūra", "temperatūra pēc jūtām", "gaisa mitrums", "nokrišņi", "vējš", "spiediens", "redzamība", "mākoņu daudzums", "saullēkts", "saulriets"]
print(piej_laikapstakli)

izv_laikapstakli= input("Ievadiet nepieciešamās prognozes no pieejamajām:")


for i in range(16):
    temp = laikazinas['list'][i]['main']['temp']
    tempjutam = laikazinas['list'][i]['main']['feels_like']
    spiediens = laikazinas['list'][i]['main']['pressure']
    gaisamitrums = laikazinas['list'][i]['main']['humidity']
    laikapstakli = laikazinas['list'][i]['weather'][0]['main']
    laikaapraksts=laikazinas['list'][i]['weather'][0]['description']
    makonudaudz = laikazinas['list'][i]['clouds']['all']
    vejaatrums = laikazinas['list'][i]['wind']['speed']
    vejavirziens = laikazinas['list'][i]['wind']['deg']
    vejabrazma = laikazinas['list'][i]['wind']['gust']
    redzamiba = laikazinas['list'][i]['visibility']
    nokrisnuiesp = laikazinas['list'][i]['pop']


    prognoze_trish=[temp, feels_like, pressure, humidity, weather, clouds, wind_speed, visibility, pop]
    print(prognoze_trish)

vajadzprognoze = izv_laikapstakli.split(' ')
