import rss2toot

print("VFL")
rss2toot.toot('https://www.vfl.de/feed/', 'https://osna.social', appname='vfl')

print("Stadt")
rss2toot.toot('https://www.osnabrueck.de/index.php?id=index&type=9818&type=9818', 'https://osna.social', appname='stadt')

print("Uni")
rss2toot.toot('https://www.uni-osnabrueck.de/kommunikation/kommunikation-und-marketing-angebot-und-aufgaben/pressestelle/pressemeldungen/?no_cache=1&type=9818', 'https://osna.social', appname='uni')

print("Kooperationsstelle")
rss2toot.toot('https://www.kooperationsstelle-osnabrueck.de/news.xml', 'https://osna.social', appname='kooperationsstelle')

print("NDR-Podcast")
rss2toot.toot('https://www.ndr.de/ndr1niedersachsen/podcast4654.xml', 'https://osna.social', appname='ndr-podcast')

print("Feuerwehr")
rss2toot.toot('https://www.feuerwehrnews-os.de/feed', 'https://osna.social', appname='feuerwehr')

print("IGMetall")
rss2toot.toot('https://www.igmetall-osnabrueck.de/rss.xml', 'https://osna.social', appname='igmetall')

print("NOZ")
rss2toot.toot('https://nitter.net/noz_os/search/rss?f=tweets&e-replies=on&e-nativeretweets=on', 'https://osna.social', appname='noz')

print("VOS")
rss2toot.toot('https://nitter.net/vos_info/search/rss?f=tweets&e-replies=on&e-nativeretweets=on', 'https://osna.social', appname='vos')

print("Zoo")
rss2toot.toot('https://nitter.net/ZooOsnabrueck/search/rss?f=tweets&e-replies=on&e-nativeretweets=on', 'https://osna.social', appname='zoo')

print("HS")
rss2toot.toot('https://nitter.net/HS_Osnabrueck/search/rss?f=tweets&e-replies=on&e-nativeretweets=on', 'https://osna.social', appname='hs')

print("Kreis")
rss2toot.toot('https://nitter.net/lkosnabrueck/search/rss?f=tweets&e-replies=on&e-nativeretweets=on', 'https://osna.social', appname='kreis')

print("ADFC")
rss2toot.toot('https://nitter.net/adfc_os/search/rss?f=tweets&e-replies=on&e-nativeretweets=on', 'https://osna.social', appname='adfc')

print("Polizei")
rss2toot.toot('https://nitter.net/Polizei_OS/search/rss?f=tweets&e-replies=on&e-nativeretweets=on', 'https://osna.social', appname='polizei')
