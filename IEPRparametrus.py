import requests
import sqlite3
import PySimpleGUI as sg

connection = sqlite3.connect("projekta_datubaze.db")
curs = connection.cursor()

piej_laikapstakli = ["1-temperatūra", "2-temperatūra pēc jūtām", "3-spiediens", "4-gaisa mitrums", "5-nokrišņi", "6-nokrišņu apraksts",
                     "7-mākoņu daudzums", "8-vēja ātrums", "9-vēja virziens", "10-vēja brēzma", "11-redzamība", "12-nokrišņu iespējamība",
                     "13-saulriets", "14-saullēkts"]

mervienibas = [" C°", " C°", " mbar", " %", "", "", " %", " m/s", "°", " m/s", " m", " %", "UTC", "UTC", ""]

layout = [
    [sg.Text('Laikapstākļi:')],
]

for item in piej_laikapstakli:
    layout.append([sg.Text(item)])

layout.append([sg.Text('Ievadiet pilsetu:', font=('Helvetica', 12)), sg.InputText(key='-PILS-')])
layout.append([sg.Text('Ievadiet nepieciešamās prognozes no pieejamajām:', font=('Helvetica', 12)), sg.InputText(key='-LAIKA-')])

layout.append([sg.Button('Ok'), sg.Button('Apskatīt laikapstākļus'), sg.Button('Ielādēt iepriekšējos iestatījumus')])

window = sg.Window('', layout)



while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Ok':
        window.close() 
    elif event == 'Apskatīt laikapstākļus':
        izv_laikapstakli = values['-LAIKA-'] + ', 15'
        pilseta = values['-PILS-']
        izv_laikapstakli = izv_laikapstakli.split(",")

        geo = requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + pilseta + '&limit=1&appid=d5f36631cc643ceb4aca81a4466d58e1').json()[0]

        lat = geo['lat']
        lon = geo['lon']

        laikazinas = requests.get('http://api.openweathermap.org/data/2.5/forecast?lat=' + str(lat) + '&lon=' + str(lon) + '&units=metric&appid=d5f36631cc643ceb4aca81a4466d58e1').json()
        saule = requests.get('https://api.sunrise-sunset.org/json?lat=' + str(lat) + '&lng=' + str(lon) + '&date=today').json()['results']

        saullekts = saule['sunrise']
        saulriets = saule['sunset']
        dienas_gar = saule['day_length']

        for i in range(len(izv_laikapstakli)):
            izv_laikapstakli[i] = izv_laikapstakli[i].replace(" ", "")
            if not izv_laikapstakli[i].isdigit():
                sg.popup_error(f"{i+1}. ievadītais parametrs nav skaitlis")
            elif int(izv_laikapstakli[i]) < 1 or int(izv_laikapstakli[i]) > 15:
                sg.popup_error(f"{i+1}. ievadītais parametrs ir ārpus pieejamajiem parametriem")

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
        pass
    elif event == 'Ielādēt iepriekšējos iestatījumus':
        izv_laikapstakli= curs.execute("SELECT Parametri FROM izsaukumi ORDER BY ID_izsaukuma DESC LIMIT 1").fetchone()
        izv_laikapstakli=str(izv_laikapstakli)
        izv_laikapstakli= izv_laikapstakli[2:-3].split(',')
        for i in range(len(izv_laikapstakli)):
            izv_laikapstakli[i]= izv_laikapstakli[i].split('-')[0]

        window['-LAIKA-'].update(','.join(izv_laikapstakli))

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




window.close()
connection.close()
