#!/usr/bin/env python3

import mechanicalsoup
from bs4 import BeautifulSoup
import datetime
import sqlite3
import sys
import os
from mastodon import Mastodon



sql = sqlite3.connect('tootbot.db')
db = sql.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS toots (ID INTEGER PRIMARY KEY
           AUTOINCREMENT, beschreibung text, anlass text,
           datum_zeit DATETIME, fachbereich text, tagesordnung_url)''')


mastodon = sys.argv[1]
passwd = sys.argv[2]
instance = sys.argv[3]

mastodon_api = None

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

        db.execute('''SELECT * FROM toots WHERE beschreibung = ? AND anlass = ?
                   and datum_zeit = ? and fachbereich = ? and
                   tagesordnung_url = ?''',
                   (beschreibung, anlass, datum_zeit, fachbereich,
                    tagesordnung_url))  # noqa

        last = db.fetchone()
        if last is None:
            if mastodon_api is None:
                if not os.path.isfile(instance+'.secret'):
                    if Mastodon.create_app(
                        'tootbot',
                        api_base_url='https://'+instance,
                        to_file=instance+'.secret'
                    ):
                        print('tootbot app created on instance '+instance)
                    else:
                        print('failed to create app on instance '+instance)
                        sys.exit(1)


                try:
                    mastodon_api = Mastodon(
                        client_id=instance+'.secret',
                        api_base_url='https://'+instance
                    )
                    mastodon_api.log_in(
                        username=mastodon,
                        password=passwd,
                        scopes=['read', 'write'],
                        to_file=mastodon+".secret"
                    )
                except:
                    print("ERROR: First Login Failed!")
                    sys.exit(1)


            out = []
            out.append(beschreibung)
            out.append(datum_string + " " + zeit)
            out.append("Fachbereich: #" +  fachbereich.replace(" ", "_").replace(",", ""))
            if tagesordnung_url:
                out.append("Tagesordnung: " + tagesordnung_url)


            toot = "\n".join(out)

            mastodon_api.status_post(toot, sensitive=False,
                                     in_reply_to_id=None,
                                     visibility='unlisted',
                                     spoiler_text=None)

            db.execute('''INSERT INTO toots (beschreibung, anlass, datum_zeit,
                       fachbereich, tagesordnung_url) VALUES ( ? , ? , ? , ?, ?)
                       ''',
                       (beschreibung, anlass, datum_zeit, fachbereich,
                        tagesordnung_url))
            sql.commit()

