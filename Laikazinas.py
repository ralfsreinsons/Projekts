import requests
import sqlite3
connection = sqlite3.connect("projekta_datubaze.db")
curs = connection.cursor()

pilseta = input("Ievadiet pilsetu:")
geo= requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + pilseta +'&limit=1&appid=d5f36631cc643ceb4aca81a4466d58e1').json()[0]

lat= geo['lat']  
lon= geo['lon']

laikazinas = requests.get('http://api.openweathermap.org/data/2.5/forecast?lat=' + str(lat)+'&lon='+ str(lon)+ '&units=metric&appid=d5f36631cc643ceb4aca81a4466d58e1').json()
saule = requests.get('https://api.sunrise-sunset.org/json?lat='+ str(lat)+'&lng=' + str(lon) +'&date=today').json()['results']

saullekts = saule['sunrise']
saulriets= saule['sunset']
dienas_gar = saule['day_length']



piej_laikapstakli= ["1-temperatūra", "2-temperatūra pēc jūtām","3-spiediens", "4-gaisa mitrums", "5-nokrišņi", "6-nokrišņu apraksts","7-mākoņu daudzums", "8-vēja ātrums","9-vēja virziens","10-vēja brēzma", "11-redzamība",  "12-nokrišņu iespējamība", "13-saulriets", "14-saullēkts"]
mervienibas = [" C°", " C°", " mbar", " %", "", "", " %", " m/s", "°", " m/s", " m", " %", "UTC", "UTC", ""]
for i in piej_laikapstakli:
    print(i, end='\n')

izv_laikapstakli = input("Ievadiet nepieciešamās prognozes no pieejamajām:") + ', 15'
izv_laikapstakli = izv_laikapstakli.split(",")

for i in range(len(izv_laikapstakli)):
    izv_laikapstakli[i] = izv_laikapstakli[i].replace(" ", "")
    if izv_laikapstakli[i].isalpha():
        raise Exception( str(i+1) + ".ievadītas parametrs nav skaitlis")
    elif int(izv_laikapstakli[i])>0 and int(izv_laikapstakli[i])<16:
        pass
    else:
        raise Exception( str(i+1) + ".ievadītas parametrs skaitlis ir ārpus piedāvātajiem parametriem")


# Testēšanai - pareizi ievadīts izvēlētais laikapstākļu parametrs
# rez=0
# for i in range(len(piej_laikapstakli)):
#     for k in range(len(izv_laikapstakli)):
#         if izv_laikapstakli[k]== piej_laikapstakli[i]:
#             rez+=1

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
    laiks = laikazinas['list'][i]['dt_txt']
    prognoze_trish_list=[temp, tempjutam , spiediens , gaisamitrums, laikapstakli, laikaapraksts, makonudaudz, vejaatrums, vejavirziens, vejabrazma, redzamiba, nokrisnuiesp, saullekts, saulriets, laiks]
    izvadamie_dati= []
    for i in range(len(izv_laikapstakli)):
        izvadamie_dati.append(str(prognoze_trish_list[int(izv_laikapstakli[i])-1]) + mervienibas[int(izv_laikapstakli[i])-1])
    
    print(izvadamie_dati)

# Ievada izmantojot vrdus nevis ciparus
#     prognoze3h=dict()
#     for i in range(len(prognoze_trish_list)):
#         prognoze3h.update({piej_laikapstakli[i] : prognoze_trish_list[i]})
#     for k in range(len(izv_laikapstakli)):
#         print(prognoze3h[izv_laikapstakli[k]])
# print(prognoze3h)

izv_laikapstakli = izv_laikapstakli[:-1]
for i in range(len(izv_laikapstakli)):
    izv_laikapstakli[i]= piej_laikapstakli[int(izv_laikapstakli[i]) - 1]


def get_next_id(column_name):
    curs.execute(f"SELECT MAX({column_name}) FROM izsaukumi")
    max_id = curs.fetchone()[0]
    return max_id + 1 if max_id is not None else 1

def insert_values_as_row(values):
    nakam_id_izsaukuma = get_next_id("ID_izsaukuma")
    nakam_id_lietotaja = get_next_id("ID_lietotaja")
    curs.execute("INSERT INTO izsaukumi (ID_izsaukuma, Parametri, ID_lietotaja) VALUES (?, ?, ?)", 
                 (nakam_id_izsaukuma, ','.join(str(v) for v in values), nakam_id_lietotaja))
    connection.commit()


insert_values_as_row(izv_laikapstakli)


rows = curs.execute("SELECT Parametri FROM izsaukumi ORDER BY ID_izsaukuma DESC LIMIT 5").fetchall()
for row in rows:
    print(row)



connection.close()

