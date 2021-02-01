#!/usr/bin/env python3

import mechanicalsoup
from bs4 import BeautifulSoup
import datetime
import sqlite3
import sys
import os
import urllib.request as urllib3


sql = sqlite3.connect('ris.db')
db = sql.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS sitzungen (ID INTEGER PRIMARY KEY
           AUTOINCREMENT, beschreibung text, anlass text,
           datum_zeit DATETIME, fachbereich text, tagesordnung_url text,
           toot_status int)''')

db.execute('''CREATE TABLE IF NOT EXISTS beschluss (ID INTEGER PRIMARY KEY
           AUTOINCREMENT, sitzungen_id int,
           beschluss text, toot_status int)''')

ris_url = "https://ris.osnabrueck.de/bi/si018_a.asp?showall=true"

browser = mechanicalsoup.StatefulBrowser()
browser.open(ris_url)

# "Lupe" auswählen
browser.select_form('form[action="si018_a.asp"]')
# Klick auf "Lupe"
response = browser.submit_selected()


# Um alle Sitzungen anzuzeigen
browser.open_relative("si018_a.asp?showall=true")

soup = browser.get_current_page()

table = soup.find('table', {"class": "tl1"})
rows = table.find_all('tr',  class_=["zl11", "zl12"])



front_url = "https://ris.osnabrueck.de/bi/"
for row in rows :
    if (row is not None):

        tds = row.find_all("td")

        tagesordnung_url = tds[1].find("a")
        if tagesordnung_url:
            tagesordnung_url = front_url + tagesordnung_url["href"]
        else:
            tagesordnung_url = ""

        beschreibung = tds[1].string
        if not beschreibung:
            continue

        anlass = tds[2].string
        if not anlass:
            continue

        datum_string = tds[6].string
        zeit = tds[7].string
        if datum_string and zeit:
            datum_zeit = datetime.datetime.strptime(datum_string + " " + zeit[:5], "%d.%m.%Y %H:%M")
        else:
            continue

        fachbereich = tds[8].string

        db.execute('''SELECT id, tagesordnung_url FROM sitzungen WHERE beschreibung = ?
                   AND anlass = ? AND datum_zeit = ? AND fachbereich = ?''',
                   (beschreibung, anlass, datum_zeit, fachbereich))
        last = db.fetchone()

        # Füge neuen Eintrag hinzu wenn noch nicht vrohande
        if last is None:
            db.execute('''INSERT INTO sitzungen (beschreibung, anlass, datum_zeit,
                       fachbereich, tagesordnung_url, toot_status) VALUES ( ? , ? , ? , ?, ?, ?)
                       ''',
                       (beschreibung, anlass, datum_zeit, fachbereich,
                        tagesordnung_url, 0))
            sql.commit()

        # Update sitzungseintrag wenn eine Tagesordnung da ist.
        elif last[1] == '' and tagesordnung_url:
            db.execute('''UPDATE sitzungen SET tagesordnung_url = '{}' WHERE ID = {};
                       '''.format(tagesordnung_url, last[0]))

            sql.commit()

            tagesordnung_html =  urllib3.urlopen(tagesordnung_url)

            try:
                tagesordnung_html =  urllib3.urlopen(tagesordnung_url)
            except:
                print("No connection to Tagesordnung")
                continue


            # Bekomme die Beschlüsse
            tagesordnung =  BeautifulSoup(tagesordnung_html, features="html.parser")

            table = tagesordnung.find('table', {"class": "tl1"})
            rows = table.find_all('tr',  class_=["zl11", "zl12"])

            for row in rows:
                if row is not None:
                    tds = row.find_all("td")
                    if not tds[5].string:
                        continue

                    v_link = tds[5].find("a")
                    if not v_link:
                        continue

                    if  v_link["href"][:2] != "vo":
                        continue

                    try:
                        vorlage_html =  urllib3.urlopen("https://ris.osnabrueck.de/bi/" + tds[5].find("a")["href"])
                    except:
                        print("No connection to Vorlage")
                        continue

                    # Speicher die Beschlüsse der Sitzung
                    vorlage =  BeautifulSoup(vorlage_html, features="html.parser")
                    if vorlage.div.p.span.text == "Beschluss:":
                        beschluss = vorlage.find("table", class_="risdeco").div.text
                        beschluss = beschluss.replace("\xa0", "")
                        beschluss = beschluss.replace("Beschluss:", "")

                        db.execute('''INSERT INTO beschluss (sitzungen_id, beschluss, toot_status)
                                   VALUES ( ? , ? , ?)''',(last[0], beschluss, 0))
                        sql.commit()


