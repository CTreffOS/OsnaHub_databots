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

print("Polizei")
rss2toot.toot('https://www.presseportal.de/rss/dienststelle_104236.rss2', 'https://osna.social', appname='polizei')

print("Feuerwehr")
rss2toot.toot('https://www.feuerwehrnews-os.de/feed', 'https://osna.social', appname='feuerwehr')

print("Zoll")
rss2toot.toot('https://www.presseportal.de/rss/dienststelle_121236.rss2', 'https://osna.social', appname='zoll')

print("IGMetall")
rss2toot.toot('https://www.igmetall-osnabrueck.de/rss.xml', 'https://osna.social', appname='igmetall')

