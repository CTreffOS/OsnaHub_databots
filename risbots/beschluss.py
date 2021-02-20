#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sqlite3
import sys
import os
from mastodon import Mastodon
import urllib.request as urllib3


sql = sqlite3.connect('ris.db')
db = sql.cursor()

mastodon = "" # Bot mail
passwd = "" # Bot Paswort
instance = "" # Mastodon Instance

mastodon_api = None

get_sitzung_query = """SELECT id, beschreibung, datum_zeit, fachbereich, tagesordnung_url
                       FROM sitzungen
                       WHERE date(datum_zeit) <= date('now','+3 day')
                       AND date(datum_zeit) >= date('now')
                       AND tagesordnung_url!=''
                       AND toot_status<2;"""



db.execute(get_sitzung_query)

sitzungen = db.fetchall()

for sitzung in sitzungen:

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

    id, beschreibung, datum_zeit, fachbereich, tagesordnung_url = sitzung

    db.execute('''UPDATE sitzungen SET toot_status = '{}' WHERE ID = {};
               '''.format(2, id))
    sql.commit()


    out = []
    out.append(beschreibung)
    out.append(datum_zeit)
    out.append("Fachbereich: #" +  fachbereich.replace(" ", "_").replace(",", ""))
    out.append("Tagesordnung: " + tagesordnung_url)


    toot = "\n".join(out)

    main_toot = mastodon_api.status_post(toot, sensitive=False,
                             in_reply_to_id=None,
                             visibility='unlisted',
                             spoiler_text=None)

    db.execute("SELECT beschluss FROM beschluss WHERE sitzungen_id={}".format(id))
    beschluesse = db.fetchall()
    for beschluss in beschluesse:
        beschluss = beschluss[0].split(" ")

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

