#!/usr/bin/env python3

import mechanicalsoup
from bs4 import BeautifulSoup
import datetime
import sqlite3
import sys
import os
from mastodon import Mastodon
import urllib.request as urllib3



sql = sqlite3.connect('tootbot.db')
db = sql.cursor()

mastodon = sys.argv[1]
passwd = sys.argv[2]
instance = sys.argv[3]

mastodon_api = None


db.execute("SELECT * FROM toots WHERE date(datum_zeit) = date('now','+2 day')")

sitzungen =  db.fetchall()

for sitzung in sitzungen:
    _, beschreibung, _, datum_zeit, fachbereich, tagesordnung_url = sitzung

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
    out.append(datum_zeit)
    out.append("Fachbereich: #" +  fachbereich.replace(" ", "_").replace(",", ""))
    if tagesordnung_url:
        out.append("Tagesordnung: " + tagesordnung_url)


    toot = "\n".join(out)

    main_toot = mastodon_api.status_post(toot, sensitive=False,
                             in_reply_to_id=None,
                             visibility='unlisted',
                             spoiler_text=None)

    try:
        tagesordnung_html =  urllib3.urlopen(tagesordnung_url)
    except:
        print("No connection to Tagesordnung")

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

            vorlage =  BeautifulSoup(vorlage_html, features="html.parser")
            if vorlage.div.p.span.text == "Beschluss:":
                beschluss = vorlage.find("table", class_="risdeco").div.text
                beschluss = beschluss.replace("\xa0", "")
                beschluss = beschluss.replace("Beschluss:", "")
                beschluss = beschluss.split(" ")

                sub_toots = []
                tmp_toot = "Beschluss:"
                for x in beschluss:
                    # +1 wegen den Leerzeichen und 8 Zeich Platz für "(10/11) "
                    if len(tmp_toot) + len(x) + 2 <= 500 - 8:
                        tmp_toot = tmp_toot + " " + x
                    else:
                        sub_toots.append(tmp_toot)
                        tmp_toot = x

                sub_toots.append(tmp_toot)

                i = 0
                anzahl = len(sub_toots)
                for sub_toot in sub_toots:
                    i = i + 1
                    nr = "(%i/%i) " % (i, anzahl)

                    poll = None
                    if i == anzahl:
                        poll = mastodon_api.make_poll(
                                ["Finde ich gut",
                                 "Finde ich nicht gut",
                                 "Bin mir Unsicher"],
                                 60*60*24*7) # 7 Tage in Sekunden


                    mastodon_api.status_post(nr + sub_toot, sensitive=False,
                                             in_reply_to_id=main_toot["id"],
                                             poll=poll,
                                             visibility='unlisted',
                                             spoiler_text=None)


