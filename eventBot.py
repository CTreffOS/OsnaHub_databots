#!usr/bin/env python3
# -*- coding: utf-8 -*-

import ipdb 
import time
import json
import requests

URL = 'https://www.os-kalender.de/os/'
API_URL = 'https://os-kalender.de/systm/api.php'
now_since_epoch_time = int(time.time())
tenDays = now_since_epoch_time + 86400 * 10
amountItems = 6

""" 
#zum Extrahieren der Ortsnamen
orte = ''
for x in range(1, 34):
    response = requests.post(API_URL,
        {
            'cmd': 'ort',
            'ortId': x
        }
    )
    ort = json.loads(response.text)['data']
    orte = orte + ' ' + ort['name']
print(orte)
"""

response = requests.post(API_URL, 
        {
            'cmd': 'tips',
            'rubrik': 1,
            'orte': 'Alle', #Noch nicht sicher, ob das hier korrekt ist. Integer??? var orteStringified = JSON.stringify(activeOrte);
            'timeFrom': now_since_epoch_time,
            'timeTo': tenDays,
            'limit': amountItems,
            'theme': 'os'
        }
    )

data = json.loads(response.text)['data']
data = json.loads(json.dumps(data))
for event in range(amountItems-1):
    titel = data[event]['veranstaltung']
    beginn_text = data[event]['zeit']
    beginn = data[event]['datum_start']
    ende = data[event]['datum_ende']
    location = data[event]['o_location']

ipdb.set_trace()