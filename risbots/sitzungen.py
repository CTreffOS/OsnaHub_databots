#!/usr/bin/env python3

from datetime import datetime
import sqlite3
import sys
import os
from mastodon import Mastodon

sql = sqlite3.connect('ris.db')
db = sql.cursor()

mastodon = "" # Bot mail
passwd = "" # Bot Paswort
instance = "" # Mastodon Instance

get_query = """SELECT id, beschreibung, datum_zeit, fachbereich, tagesordnung_url
            FROM sitzungen WHERE date(datum_zeit) <= date('now','+7 day')
            AND date(datum_zeit) > date('now')
            AND toot_status = 0;"""

mastodon_api = None

db.execute(get_query)
sitzungen =  db.fetchall()
for sitzung in sitzungen:

    # Verbinden mit Mastodon
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
    datum_zeit = datetime.strptime(datum_zeit, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")

    out = []
    out.append(beschreibung)
    out.append(datum_zeit)
    out.append("Fachbereich: #" +  fachbereich.replace(" ", "_").replace(",", ""))
    if tagesordnung_url:
        out.append("Tagesordnung: " + tagesordnung_url)


    toot = "\n".join(out)

    # Auf Mastodon tooten
    mastodon_api.status_post(toot, sensitive=False,
                             in_reply_to_id=None,
                             visibility='unlisted',
                             spoiler_text=None)

    db.execute('''UPDATE sitzungen SET toot_status = '{}' WHERE ID = {};
               '''.format(1, id))
    sql.commit()
