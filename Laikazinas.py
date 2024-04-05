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
temp= 1
piej_laikapstakli= {'temperatūra', 'temperatūra pēc jūtām', 'gaisa mitrums', 'nokrišņi', "vēja ātrums, brāzma un virziens"}


for i in range(16):
    print(laikazinas['list'][i]['main']['temp'])



