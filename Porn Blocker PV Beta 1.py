import os
import sys
import ctypes
import curses
from optparse import check_choice
import time
import subprocess
import re
import webbrowser

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Skript mit Administratorrechten neu starten
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()

# ASCII-Art-Logo
logo = """
 ██▓███   ▒█████   ██▀███   ███▄    █     ▄▄▄▄    ██▓     ▒█████   ▄████▄   ██ ▄█▀▓█████  ██▀███  
▓██░  ██▒▒██▒  ██▒▓██ ▒ ██▒ ██ ▀█   █    ▓█████▄ ▓██▒    ▒██▒  ██▒▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒▒██░  ██▒▓██ ░▄█ ▒▓██  ▀█ ██▒   ▒██▒ ▄██▒██░    ▒██░  ██▒▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒▒██   ██░▒██▀▀█▄  ▓██▒  ▐▌██▒   ▒██░█▀  ▒██░    ▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ░  ░░ ████▓▒░░██▓ ▒██▒▒██░   ▓██░   ░▓█  ▀█▓░██████▒░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ▒░   ▒ ▒    ░▒▓███▀▒░ ▒░▓  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░▒ ░       ░ ▒ ▒░   ░▒ ░ ▒░░ ░░   ░ ▒░   ▒░▒   ░ ░ ░ ▒  ░  ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
░░       ░ ░ ░ ▒    ░░   ░    ░   ░ ░     ░    ░   ░ ░   ░ ░ ░ ▒  ░        ░ ░░ ░    ░     ░░   ░ 
             ░ ░     ░              ░     ░          ░  ░    ░ ░  ░ ░      ░  ░      ░  ░   ░     
                                           ░                  ░                               
"""

sites = [
    ("|""PornHub ~ 3 Sekunden", [
        ("pornhub.com", "66.254.114.41"),
        ("pornhub-deutsch.net", "216.18.168.20"),
        ("fr.pornhub.org", "66.254.114.41"),
        ("rt.pornhub.org", "66.254.114.41"),
        ("de.pornhubpremium.com", "66.254.114.33"),
        ("es.pornhub.com", "66.254.114.41"),
    ]),
    ("|""xHamster ~ 3 Sekunden", [
        ("xhamster.com", "88.208.60.136"),
        ("ge.xhamster.desi", "172.67.202.84"),
        ("xhopen.com", "185.207.236.242"),
        ("ge.xhamster2.com", "104.21.16.210"),
        ("ge.xhamster1.des", "172.67.158.52"),
        ("ge.xhamster.com", "88.208.60.136")
    ]),
    ("|""Hentai Haven ~ 6 Sekunden", [
        ("hentaihaven.xxx", "104.26.8.94"),
        ("hentaihaven.com", "104.21.43.55"),
        ("hentaihaven.icu", "104.21.15.19"),
        ("hentaihaven.co", "172.67.156.204"),
        ("hentaihaven.online", "195.16.73.90"),
        ("hentaihaven.app", "104.21.1.246"),
        ("hentaihaven.club", "104.21.20.177"),
        ("hentaihaven.ws", "172.67.162.66"),
        ("hentaihaven.vip", "172.67.210.146"),
        ("hentaihaven.su", "104.21.24.167"),
        ("hentaihaven.me", "104.21.14.117"),
        ("nhentaihaven.org", "104.26.13.249")
    ]),
    ("|""XVIDEOS ~ 4 Sekunden", [
        ("xvideos.com", "185.88.181.3"),
        ("xvideos3.com", "172.64.153.203"),
        ("xvideos2.com", "172.64.155.85"),
        ("xvideos5.com", "104.18.54.128"),
        ("xvideos4.com", "104.18.43.33"),
        ("xvideos.es", "172.64.144.205"),
        ("de.xvideos.com", "185.88.181.10")
    ]),
    ("|""XNXX ~ 3 Sekunden", [
        ("www.xnxx.com", "185.88.181.58"),
        ("xnxx.health", "104.26.5.154"),
        ("xnxx.de", "141.0.173.169"),
        ("xnxx2.com", "104.18.34.49"),
        ("xnxx.tv", "172.64.145.87"),
        ("xnxx.rest", "172.67.160.119")
    ]),
    ("|""The Porn dude ~ 3 Sekunden", [
        ("theporndude.com", "104.19.131.104"),
        ("theporndude.vip", "104.21.28.16"),
        ("theporndude.org", "172.67.73.96"),
        ("theporndude.net", "104.26.1.220"),
        ("porndudedeutsch.com", "104.21.96.53"),
        ("porndudecasting.com", "104.22.68.115"),
    ]),
    ("|""hAnime ~ 3 Sekunden", [
        ("hanime.tv", "104.21.234.245"),
        ("hanimehentai.tv", "104.21.12.52"),
        ("hanimes.org", "172.67.151.98"),
        ("hanime.watch", "172.67.194.230"),
        ("hanime.su", "104.21.19.5"),
        ("hanime.baby", "172.67.158.157"),
    ]),
    ("|""fuq ~ 2 Sekunden", [
        ("fuq.com", "128.199.47.205"),
        ("fuq.casa", "172.67.200.96"),
        ("fuq.bet", "104.21.95.178"),
    ]),
    ("|""Youporn ~ 2 Sekunden", [
        ("youporn.com", "66.254.114.79"),
        ("de.youporn.com", "66.254.114.79"),
    ]),
    ("|""Porn.com ~ < 1 Sekunde", [
        ("porn.com", "185.88.180.167"),
    ]),
    ("|""porno.com ~ < 1 Sekunde", [
        ("porno.com", "141.0.173.133")
    ]),
    ("|""Superporn ~ < 1 Sekunde", [
        ("superporn.com", "104.21.233.170")
    ]),
    ("|""HDTube.Porn ~ 2 Sekunden", [
        ("de.hdtube.porn", "104.26.10.88"),
        ("hdtube.porn", "172.67.70.213"),
        ("www.hdtube.porn", "104.26.10.88")
    ]),
    ("|""PornHat ~ 3 Sekunden", [
        ("pornhat.com", "104.26.4.214"),
        ("pornhat.one", "172.67.73.223"),
        ("pornhat.net", "185.240.30.112"),
        ("pornhat.yachts", "172.67.202.37"),
        ("pornhat.video", "104.21.56.90"),
        ("pornhat.vip", "109.206.164.52"),
        ("pornhat.tv", "172.67.176.189"),
        ("de.pornhat.one", "104.26.2.217")
    ]),
    ("|""Eporner ~ 2 Sekunden", [
        ("eporner.baby", "165.232.98.105"),
        ("www.eporner.com", "94.75.220.9"),
        ("eporner.video ", "172.67.71.237")
    ]),
    ("|""Porn Better ~ < 1 Sekunde", [
        ("porn-better.com", "85.13.132.199"),  
    ]),
    ("|""xxxi.porn ~ 2 Sekunden", [
        ("xxxi.porn", "172.67.178.33"),
        ("de.xxxi.porn", "104.21.43.103"),
        ("ixxx.com", "167.71.71.84"),
        ("ixxxcom.click", "172.67.206.138"),
        ("ixxx.cc", "50.31.188.9"),
    ]),
    ("|""Redtube ~ 6 Sekunden", [
        ("redtube.com", "66.254.114.238"),
        ("redtubedeutsch.com", "104.21.234.122"),
        ("redtube.com.br", "66.254.114.238"),
        ("redtube-porn.beauty", "172.67.150.54"),
        ("redtubedeutsch.com", "104.21.234.122"),
        ("redtube.estate", "104.21.1.31"),
        ("redtube.net.pl", "141.95.32.185"),
        ("redtube.fitness", "172.67.198.38"),
        ("redtube.net.pl", "141.95.32.185"),
        ("redtubepremium.com", "66.254.114.78"),
        ("redtub.online", "104.21.1.252"),
        ("fr.redtube.com", "66.254.114.238")
    ]),
    ("|""FoxPorns ~ 2 Sekunden", [
        ("foxporns.com", "88.208.55.241"),
        ("foxporns.net", "104.21.69.144"),
        ("foxpornos.com", "104.21.79.197"), 
        ("foxporn.me", "172.67.180.195")
    ]),
    ("|""PornOne ~ < 1 Sekunde", [
        ("pornone.com" ,"104.26.15.226")
    ]),                                                 #Ab hier ist Pub. Beta 2 (was die Seiten angeht)
    ("|""Pornmate ~ 1 Sekunde", [
        ("pornmate.com", "104.21.234.148"),
        ("mypornmate.com", "23.254.243.233"),
    ]),
    ("|""porn300 ~ 1 Sekunden", [
        ("porn300.com", "104.21.63.163"),
        ("porn300.pro", "162.251.110.74"),
        ("2porn300.best", "185.149.132.22"),
    ]),
    ("|""Porn Biz ~ 1 Sekunde", [
        ("porno.biz", "194.145.208.195"),
        ("porn.biz", "172.67.71.195"),
    ]),
    ("|""Toroporno ~ < 1 Sekunde", [
        ("toroporno.com", "146.190.28.184"),
    ]),
    ("|""SexVid ~ 3 Sekunden", [
        ("www.sexvid.xxx", "213.174.152.197"),
        ("de.sexvid.xxx", "213.174.152.197"),
        ("www.sexvid.porn", "192.243.54.251"),
        ("www.sexvid.pro", "192.243.54.250")
    ]),
    ("|""SpankBang ~ 3 Sekunden", [
        ("spankbang.com", "104.19.130.98"),
        ("spankbang.party", "104.18.30.242"),
        ("spankbanglive.com", "104.17.117.12"),
        ("spankbang.run", "104.21.9.64"),
        ("es.spankbanglive.com", "104.17.118.12"),
        ("spankbangs.co.uk", "212.1.209.50")
    ]),
    ("|""Youjizz ~ 2 Sekunden", [
        ("youjizz.casino", "104.21.69.70"),
        ("youjizz.com", "66.254.114.242"),
        ("youjizz.markets", "104.21.24.143"),
        ("youjiz.world", "172.67.150.91"),
    ]),
    ("|""PornHoarder ~ 3 Sekunden", [
        ("ww8.pornhoarder.tv", "172.67.175.136"),
        ("ww7.pornhoarder.tv", "172.67.175.136"),
        ("www.pornhoarder.tv", "172.67.175.136"),
        ("wwvv.pornhoarder.tv", "172.67.175.136"),
        ("pornhoarder.org", "104.21.10.151"),
        ("pornhoarders.com", "172.67.175.162"),
        ("ww6.pornhoarder.tv", "104.21.91.163")
    ]),                                             #Pub. Beta 3
    ("|""Private.com ~ < 1 Sekunde", [
        ("de.private.com", "185.94.237.137")
    ]),
    ("|""JavGG ~ 2 Sekunden", [
        ("javgg.pro", "104.21.52.89"),
        ("javgg.net", "104.26.0.238"),
        ("javgg.sbs", "104.21.10.217"),
        ("javbest.tv", "172.67.221.202"),
        ("jav.guru", "104.26.5.14"),
    ]),
    ("|""OK.PORN ~ 2 Sekunden", [
        ("ok.porn", "104.21.73.191"),
        ("ok.xxx", "104.26.9.232"), 
        ("okporn.xxx", "104.21.57.119"),
        ("pornsok.com", "212.7.209.233"),
        ("okporn.com", "109.206.163.22"),
    ]),
    ("|""Bellesa ~ 2 Sekunden", [
        ("bellesa.co", "104.19.142.110"),
        ("bboutique.co", "104.18.40.225"),
        ("bellesaplus.co", "172.64.151.155"), 
        ("everythingcantiks.com", "151.101.66.236"),
    ]),
    ("|""Hobby.porn ~ < 1 Sekunde", [
        ("hobby.porn", "185.149.132.188")
    ]),
    ("|""Beeg.Porn 6 Sekunden", [
        ("beeg.porn", "172.67.184.95"),
        ("beeg.com", "172.67.181.179"),
        ("beeg.works", "104.21.44.199"),
        ("beeg.world", "104.21.87.50"),
        ("free-beeg.icu", "172.67.175.67"),
        ("beegs.me", "104.21.12.141"),
        ("beeg.sex", "104.21.234.62"),
        ("beeg.day", "104.21.91.35"),
        ("beeg.work", "104.21.7.132"),
        ("beegs.rocks", "172.67.200.18"),
        ("beeg24.org", "172.67.203.225"),
        ("beeg-pornos.com", "172.67.132.229"),
        ("mybeegporn.com", "45.84.30.5"),
    ]),
    ("|""Pornpen.ai ~ < 1 Sekunde", [
        ("pornpen.ai", "104.26.4.30"),
    ]),
    ("|""AnalVids ~ < 1 Sekunde", [
        ("analvids.com", "185.120.71.26"),
    ]),
    ("|""24xxx.porn ~ 1 Sekunde", [
        ("24xxx.porn", "51.83.223.165"),
        ("24xxx.me", "51.89.96.105"),
    ]),
    ("|""RedPorn ~ 2 Sekunden", [
        ("redporn.porn", "104.21.27.68"),
        ("redporn.xxx", "172.67.176.30"),
        ("redtube.com", "66.254.114.238"),
        ("redporn.tv", "172.67.211.150"),
    ]),
    ("|""Punishworld.com ~ 1 Sekunde", [
        ("punishworld.com", "104.26.2.187"),
        ("thepornlist.net", "172.67.68.7"),
    ]),
    ("|""AnyPorn ~ 2 Sekunden", [
        ("anyporn.com", "88.208.55.1"),
        ("anyporn.bond", "172.67.163.130"),
        ("anyporn.asia", "172.67.170.55"),
    ]),
    ("|""AllClassic.porn ~ < 1 Sekunde", [
        ("allclassic.porn", "51.91.30.41"),
    ]),
    ("|""7DAK ~ < 1 Sekunde", [
        ("7dak.com", "172.67.31.126")
    ]),
    ("|""HornyBank ~ < 1 Sekunde", [
        ("hornybank.com", "194.187.96.37")
    ]),
    ("|""BustyBus ~ 1 Sekunde", [
        ("bustybus.com", "104.21.59.68"),
        ("basti-bus.de", "153.92.220.185"),
    ]),
    ("|""Check Porn ~ < 1 Sekunde", [
        ("check.porn", "172.67.217.234"),
    ]),
    ("|""Pornohd ~ 2 Sekunden", [
        ("en.pornohd.porn", "137.74.57.139"),
        ("www.pornohd.sex", "87.98.227.15"),
        ("en.xhdporno.porn", "91.134.158.98"),
        ("pornohd.ro", "172.67.181.69"),
        ("pornhd.com", "159.223.211.188"),
    ]),
    ("|""PornHubs ~ < 1 Sekunde", [
        ("pornhubs.video", "104.21.234.160"),
    ]),
    ("|""Evooli ~ < 1 Sekunde", [
        ("evooli.com", "104.21.52.177")
    ]),
    ("|""Meta Porn ~ < 1 Sekunde", [
        ("metaporn.com", "159.223.211.188"),
    ]),
    ("|""freeporn.rodeo ~ 2 Sekunden", [
        ("freeporn.rodeo", "31.133.208.9"),
        ("sextube.rodeo", "109.206.176.92"),
        ("sexvideo.rodeo", "31.133.223.72"),
        ("freeporn.onl", "62.122.169.41"),
    ]),
    ("|""4 Porn ~ < 1 Sekunde", [
        ("4porn.com", "188.72.227.100"),
    ]),
    ("|""77 Porn ~ < 1 Sekunde", [
        ("777.porn", "172.67.144.187"), 
    ]),
    ("|""Dark porn ~ < 1Sekunde ", [
        ("darknessporn.com", "104.26.1.111"),
    ]),
    ("|""Hot-Sex-Tube ~ 1 Sekunde", [
        ("hot-sex-tube.com", "192.243.50.48"),
        ("hotsextube.tv", "104.21.26.158"),
    ]),
    ("|""PeluGuauDog ~ < 1 Sekunde", [
        ("peluguaudog.es", "104.21.0.135"),
    ]),
    ("|""Freieporno ~ < 1 Sekunde", [
        ("freieporno.com", "172.67.161.191")
    ]),
    ("|""Cartoon Porn Videos ~ 2 Sekunde", [
        ("cartoonpornvideos.com", "159.223.211.188"),
        ("cartoonporn.com", "104.27.204.89"),
        ("cartoonpornvids.com", "104.21.234.176")
    ]),
    ("|""18porn.wtf ~ 2 Sekunden", [
        ("18porn.wtf", "208.122.193.58"),
        ("18porn.sex", "208.122.193.61"),
        ("18pornhd.com", "84.247.3.181"),
    ]),
    ("|""Hentai City ~ < 1 Sekunde", [
         ("hentaicity.com", "216.18.168.54"),
    ]),
    ("|""Lobster Tube ~ < 1 Sekunde", [
        ("lobstertube.com", "146.190.28.184"),
    ]),
    ("|""The Best Fetish Sites ~ 2 Sekunden", [
        ("thebestfetishsites.com ", "104.25.232.88"),
        ("thebestfetishsites.com.atlaq.com", "172.67.176.167"),
        ("fetishsites.net", "107.180.56.177")
    ]),
    ("|""The Porn Guy - Dude ~ 2 Sekunden", [
        ("thepornguy.org", "104.21.23.31"),
        ("thepornlist.net", "104.26.14.211"),
        ("thepornmap.com", "141.193.213.10"),
        ("thepornlist.net", "172.67.68.7"),
    ]),
    ("|""Multporn ~ 2 Sekunden", [
        ("multporn.net", "104.22.22.184"),
        ("multporn.xxx", "104.21.30.94"),
        ("rule34.art", "104.21.72.75"),
    ]),
    ("|""Melons Tube ~ < 1 Sekunde", [
        ("melonstube.com", "167.172.42.100")
    ]),
    ("|""4Tube ~ 2 Sekunden", [
        ("4tube.com", "104.20.223.111"),
        ("4tube.casa", "104.21.12.78"),
        ("4tube.info", "213.174.130.131"),
        ("4tube.live", "154.49.142.172"),
        ("4tube.hu", "172.67.142.51"),
    ]),
    ("|""Jerkmate ~ 2 Sekunden", [
        ("jerkmate.com", "18.164.116.108"),
        ("jerkmatelive.com", "207.246.147.189"),
        ("jerkmates.com", "199.59.247.188"),
        ("jerkmate.tv", "54.236.103.10")      
    ]),
    ("|""3danimalporn.com ~ 2 Sekunden", [
        ("3danimalporn.com", "104.21.234.176"),
        ("animalporn.me", "104.21.19.173"),
        ("animalporn.in", "104.21.234.89"),
    ]),
    ("|""dinotube.com ~ < 1 Sekunde", [
        ("dinotube.com", "188.166.10.168")
    ]),
    ("|""Faphouse ~ < 1 Sekunde", [
        ("faphouse.com", "104.18.36.19"),
    ]),
    ("|""Prime Porn List ~ < 1 Sekunde", [
        ("primepornlist.com", "67.227.203.111")
    ]),
    ("|""Xossipy.com ~ < 1 Sekunde", [
        ("xossipy.com", "104.21.69.48")
    ]),
    ("|""tbpsl.com ~ < 1 Sekunde", [
      ("tbpsl.com", "64.20.37.43"),
      ("thepornlist.net", "104.26.15.211")
    ]),
]

game_sites = [
    ("|""Gamecore ~ 2 Sekunden", [
        ("gamcore.com", "51.195.73.91"),
        ("gamecore.com", "91.237.98.22"),
        ("gamcore.ch", "51.195.73.91"),
        ("sandbox.gamecore.com", "51.195.73.91"),
        ("coregames.com", "20.69.134.17")
    ]),
    ("|""PornGamesHub ~ 2 Sekunden", [
        ("porngameshub.com", "159.203.159.148"),
        ("porngameshub.net", "104.21.95.90"),
        ("porngameshub.us", "154.62.106.248"),
        ("porngames.com", "208.74.151.171"),
        ("porngames.games", "104.18.8.78")
    ]),
    ("|""Games of Desire ~ 1 Sekunde", [                   
        ("www.gamesofdesire.com", "109.236.88.144"),
        ("gamesofdesired.com", "172.67.160.136"),
    ]),
    ("|""Mopoga.com ~ < 1 Sekunde", [
        ("mopoga.com", "66.254.114.223")
    ]),
    ("|""Sexemulator ~ < 1 Sekunde", [
        ("www.sexemulator.com", "18.164.124.64")
    ]),
    ("|""Adult Sex Games ~ 2 Sekunden", [
        ("adult-sex-games.com", "74.206.182.195"),
        ("adultgamesworld.com", "172.67.200.144"),
        ("adultgames.games", "104.18.8.78")
    ]),
    ("|""Sexy Fuck Games ~ < 1 Sekunde", [
        ("www.sexyfuckgames.com", "104.23.135.18")
    ]),
    ("|""Sex Games cc ~ < 1 Sekunde", [
        ("www.sexgames.cc", "172.67.72.145")
    ]),
    ("|""MyCandyGames ~ 1 Sekunde", [
        ("www.mycandygames.com", "89.111.52.142"),
        ("files.mycandygames.com", "89.111.52.142")
    ]),
    ("|""porngames.com ~ < 1 Sekunde", [
        ("porngames.com", "208.74.151.171"),
    ]),
    ("|""XXX Games ~ < 1 Sekunde", [
        ("xxxgames.games", "104.18.8.78"),
    ]),
    ("|""Adult Games World ~ < 1 Sekunde", [
        ("adultgamesworld.com", "104.21.50.38"),
    ]),
    ("|""Nutako ~ 2 Sekunden", [
        ("nutaku.net", "66.254.114.205"),
        ("nowintk.com", "66.254.114.112"),
        ("nutaku.com", "66.254.114.205"),
    ]),
    ("|""adultgames.games ~ < 1 Sekunde", [
        ("adultgames.games", "104.18.8.78")
    ]),
    ("|""Adult Games Collector ~ < 1 Sekunde", [
        ("adultgamescollector.com", "104.21.234.39")
    ]),
    ("|""Lewdspot ~ 1 Sekunde", [
        ("lewdspot.com", "66.254.114.223"),
        ("rosadeiventisoladelba.com", "81.88.48.78"),
    ]),
    ("|""WetPussyGames ~ 1 Sekunde", [
        ("sexgamesclub.com", "172.67.68.76"),
        ("wetpussygames.com", "104.26.1.242")
    ]),
    ("|""Graphotism.com ~ < 1 Sekunde", [
        ("graphotism.com", "104.21.90.33")
    ]),
    ("|""AdultGamesOn ~ < 1 Sekunde", [
        ("adultgameson.com", "104.21.234.155")
    ]),
    ("|""Play Porn Game ~ < 1 Sekundes", [
        ("playporngames.com", "173.214.252.3")
    ]),
    ("|""androidmo.im ~ < 1 Sekunde", [
        ("androidmo.im", "31.210.171.171")
    ]),
    ("|""Play Free XXX Games ~ < 1 Sekunde", [
        ("xxxgames.biz", "45.60.96.161")        
    ]),
    ("|""BestPornGames ~ 2 Sekunden", [
        ("bestporngames.com", "104.21.21.126"),
        ("bestporngames.games", "172.67.185.65"),
        ("bestporngames.cc", "104.21.3.101"),
    ]),
    ("|""SexGames.xxx ~ 1 Sekunde", [
        ("sexgames.xxx", "104.21.55.224"),
        ("sexgames.cc", "172.67.72.145"),
    ]),
    ("|""Hentai Flash Games ~ 2 Sekunden", [
        ("h-flash.com", "172.67.74.64"),
        ("h-flash.com", "104.26.0.147"),
        ("hentai-flash-games.com", "198.49.71.175"),
        ("2adultflashgames.com", "74.206.182.204")
    ]),
    ("|""freesexygames.com ~ 1 Sekunde", [
        ("sexflashgame.org", "31.172.74.38"),
        ("sexflashgames.org", "199.59.243.226")
    ]),
    ("|""comdotgame.com ~ < 1 Sekunde", [
        ("comdotgame.com", "104.21.234.151"),
    ]),
    ("|""StripSkunk ~ 2 Sekunden", [
        ("stripskunk.com", "104.26.9.14"),
        ("stripskunk.com.prostats.org", "198.7.121.127"),
        ("stripselector.com.siteindices.com", "45.33.74.84")
    ]),
    ("|""playsexgames.xxx ~ 1 Sekunde", [
        ("playsexgames.xxx", "173.214.252.5"),
        ("playsex.games", "93.127.179.27")
    ]),
    ("|""Gamecax ~ < 1 Sekunde", [
        ("gamecax.com", "104.21.34.231")
    ]),


]

strict_sites = [
    ("|""Character ai", [
        ("character.ai", "104.18.222.226"),
        ("https://play.google.com/store/apps/details?id=ai.character.app&hl=en_US&pli=1", "142.250.176.206")
    ])



]


last_action = []

def block_ip(ip_address, domain):
    try:
        rule_name_out = f"BlockSite_Out_{domain.replace('.', '_')}"
        rule_name_in = f"BlockSite_In_{domain.replace('.', '_')}"

        subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name=' + rule_name_out, 'dir=out', 'action=block', 'remoteip=' + ip_address], check=True)
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name=' + rule_name_in, 'dir=in', 'action=block', 'remoteip=' + ip_address], check=True)

        hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
        with open(hosts_path, 'a') as hosts_file:
            hosts_file.write(f"127.0.0.1 {domain}\n")
            hosts_file.write(f"127.0.0.1 www.{domain}\n")

        # Letzte Aktion speichern
        last_action.append((ip_address, domain))

    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Blockieren der IP-Adresse für {domain}: {e}")

def block_all_sites(stdscr):
    max_y, max_x = stdscr.getmaxyx()
    # Beide Listen kombinieren
    all_sites = sites + game_sites
    total_domains = sum(len(domains) for name, domains in all_sites)
    domains_blocked = 0

    for name, domains in all_sites:
        site_name = extract_site_name(name)
        for domain, ip_address in domains:
            domains_blocked += 1
            percentage = int((domains_blocked / total_domains) * 100)
            loading_screen(stdscr, ip_address, site_name, percentage)
            block_ip(ip_address, domain)
    stdscr.clear()
    message = "Alle Seiten wurden erfolgreich blockiert!"
    stdscr.addstr(max_y // 2, (max_x - len(message)) // 2, message)
    stdscr.refresh()
    time.sleep(7)

def unblock_last_action():
    if not last_action:
        return

    ip_address, domain = last_action.pop()

    try:
        rule_name_out = f"BlockSite_Out_{domain.replace('.', '_')}"
        rule_name_in = f"BlockSite_In_{domain.replace('.', '_')}"

        subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=' + rule_name_out], check=True)
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=' + rule_name_in], check=True)

        hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
        with open(hosts_path, 'r') as hosts_file:
            lines = hosts_file.readlines()

        with open(hosts_path, 'w') as hosts_file:
            for line in lines:
                if domain not in line:
                    hosts_file.write(line)

    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Entblocken der IP-Adresse für {domain}: {e}")

def loading_screen(stdscr, ip_address, site_name, percentage):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Bitte warten... ({percentage}% abgeschlossen)")
    stdscr.addstr(1, 0, f"Blockiere {site_name} - IP: {ip_address}")
    stdscr.refresh()
    time.sleep(0.2)

def extract_site_name(name):
    """Extrahiert den Namen der Website ohne führendes '|' und Zeitangabe."""
    # Entferne führendes '|' und Leerzeichen
    name = name.lstrip('|').strip()
    # Entferne die Zeitangabe
    match = re.match(r"^(.*?)(?: ~ \d+ Sekunden)?$", name)
    if match:
        return match.group(1).strip()
    else:
        return name

def draw_version(stdscr):
    """Zeigt die Version in der unteren rechten Ecke an."""
    max_y, max_x = stdscr.getmaxyx()
    version_text = "PV Pub. Beta 1"
    stdscr.addstr(max_y - 1, max_x - len(version_text) - 1, version_text, curses.color_pair(2))

def open_support_page(stdscr):
    # Öffnet die Support-Seite im Browser
    webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1&to=pblocker.supprt@gmail.com")

def parent_version_function(stdscr):
    webbrowser.open("https://github.com/sdsfsag/Windows-Porn-Blocker/blob/main/Porn%20Blocker%20Public%20Beta%202.exe")

def exit_program(stdscr):
    # Funktion zum Beenden des Programms
    sys.exit()
 
def show_info(stdscr):
    stdscr.clear()
    info_text = """Unterschied zwischen 'Porn Blocker' und 'Porn Blocker PV'. Der Unterschied ist, dass die PV (Parent Version) ein wenig mehr Funktionen enthält, wie dass man das Programm auf dem Computer seines Kindes ausführen kann und das Kind nichts merkt.

            ===BLOCKIEREN===

            'Alles blockieren' - Blockiert alles.

            'Strict block' - blockiert alles + Seiten die eigentlich nicht schlimm sind, aber für Pornografische Zwecke verwendet werden können.

            'Manuell blockieren' - kann falsch verstanden werden, aber dort kann man alle verfügbaren Seiten manuell blockieren.

            'Sex-Game-Blocker' - das selbe wie beim 'Manuell blockieren' nur mit Sex Games

            'Strict Mode' - blockiert Seiten/Apps die eigentlich nichts mit Pornografie zutun haben, aber dafür verwendet werden können"

            ===SUPPORT===

            'Support' - öffnet eine Seite, auf der Sie dem Entwickler eine Nachricht senden können (Beschwerden, Feedback, etc.)

            'Info' - zeigt Informationen über das Programm an.


            Unter der '|===WEITERE=VERSIONEN===|' Kategorie finden Sie weitere Versionen vom 'Porn Blocker'
        """
    max_y, max_x = stdscr.getmaxyx()
    start_y = 5  # Startposition weiter oben festlegen

    # Text in Zeilen aufteilen
    lines = info_text.split('\n')

    # Verarbeiten der Zeilen und Einfügen von Leerzeilen gemäß Ihrer Anforderungen
    processed_lines = []
    previous_line_was_heading = False
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('===') and stripped_line.endswith('==='):
            # Es ist eine Überschrift
            if processed_lines and not previous_line_was_heading:
                # 3 Leerzeilen zwischen vorherigem Text und dieser Überschrift einfügen
                processed_lines.extend(['', '', ''])
            processed_lines.append(stripped_line)
            # 2 Leerzeilen nach der Überschrift einfügen
            processed_lines.extend(['', ''])
            previous_line_was_heading = True
        else:
            processed_lines.append(stripped_line)
            previous_line_was_heading = False

            # Spezielle Behandlung für die gewünschte Zeile
            if stripped_line == "'Info' - zeigt Informationen über das Programm an.":
                # 4 zusätzliche Leerzeilen einfügen
                processed_lines.extend(['', '', '', ''])

    total_lines = len(processed_lines)

    # Berechnung der Anzahl der Zeilen, die auf dem Bildschirm angezeigt werden können
    display_height = max_y - start_y - 2  # Reserviere 2 Zeilen für Anweisungen

    # Startposition für das Scrollen
    position = 0

    while True:
        stdscr.clear()
        y = start_y
        line_idx = position
        # Anzeige der Zeilen innerhalb des aktuellen Fensters
        while y < max_y - 1 and line_idx < total_lines:
            line = processed_lines[line_idx]
            if line.strip() == '':
                # Leere Zeile, y erhöhen
                y += 1
            else:
                # Zeile zentriert anzeigen
                stdscr.addstr(y, (max_x - len(line)) // 2, line)
                y += 1
            line_idx += 1
        # Anweisungen anzeigen mit color_pair(4)
        instructions = "(Pfeiltasten zum Scrollen, ESC zum Zurückkehren)"
        stdscr.addstr(max_y - 1, (max_x - len(instructions)) // 2, instructions, curses.color_pair(4))
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            if position + display_height < total_lines:
                position += 1  # Nach unten scrollen
        elif key == curses.KEY_UP:
            if position > 0:
                position -= 1  # Nach oben scrollen
        elif key == 27:  # ESC-Taste zum Beenden
            break

    stdscr.clear()
    stdscr.refresh()

def main_menu(stdscr):
    curses.curs_set(0)
    current_column_index = 1  # Start in der mittleren Spalte
    current_item_index = 0

    columns = [
        {
            'header': '|===SUPPORT===|',  
            'items': [
                'Support',
                'Info'
            ],
        },
        {
            'header': '|===BLOCKIEREN===|',     #B͟L͟O͟C͟K͟I͟E͟R͟E͟N
            'items': [
                'Alles blockieren (dauert am längsten) ~ 2,4 Minuten',
                'Manuell blockieren',
                'Sex-Game-Blocker',
                'Strict Mode',
                'Beenden'
            ]
        },
        {
            'header': '|===WEITERE=VERSIONEN===|',      #W͟E͟I͟T͟E͟R͟E=V͟E͟R͟S͟I͟O͟N͟E͟N
            'items': ['Normal PBlocker']
        }
    ]

    menu_actions = {
        'Support': open_support_page,
        'Info': show_info,
        'Alles blockieren (dauert am längsten) ~ 2,4 Minuten': block_all_sites,
        'Manuell blockieren': manual_block_menu,
        'Sex-Game-Blocker': game_block_menu,
        'Strict Mode': strict_mode_menu,
        'Beenden': exit_program,
        'Normal PBlocker': parent_version_function,
    }

    while True:
        stdscr.clear()

        # Logo anzeigen
        logo_lines = logo.splitlines()
        max_y, max_x = stdscr.getmaxyx()
        logo_y = 2  # Startposition des Logos
        for i, line in enumerate(logo_lines):
            stdscr.addstr(logo_y + i, (max_x - len(line)) // 2, line, curses.color_pair(1))

        # Berechne die Breite für jede Spalte
        col_width = max_x // 3

        start_y = logo_y + len(logo_lines) + 2  # Startposition des Menüs

        for col_idx, column in enumerate(columns):
            x_start = col_idx * col_width
            y_start = start_y

            # Überschrift zentriert anzeigen und hervorheben
            header = column['header']
            header_width = len(header)
            stdscr.addstr(y_start, x_start + (col_width - header_width) // 2,
                          header, curses.A_BOLD | curses.color_pair(3))
            y_start += 2  # Platz für Überschrift

            # Menüoptionen anzeigen
            for item_idx, item in enumerate(column['items']):
                y = y_start + item_idx

                item_width = len(item)
                x = x_start + (col_width - item_width) // 2  # Zentriert in der Spalte

                if col_idx == current_column_index and item_idx == current_item_index:
                    stdscr.addstr(y, x, item, curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, item)

        draw_version(stdscr)  # Version anzeigen

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_LEFT and current_column_index > 0:
            current_column_index -= 1
            current_item_index = 0  # Reset item index when changing columns
        elif key == curses.KEY_RIGHT and current_column_index < len(columns) - 1:
            current_column_index += 1
            current_item_index = 0  # Reset item index when changing columns
        elif key == curses.KEY_UP:
            if current_item_index > 0:
                current_item_index -= 1
        elif key == curses.KEY_DOWN:
            if current_item_index < len(columns[current_column_index]['items']) - 1:
                current_item_index += 1
        elif key == ord('\n'):
            selected_item = columns[current_column_index]['items'][current_item_index]
            action = menu_actions.get(selected_item)
            if action:
                if action == exit_program:
                    break  # Beenden der Applikation
                else:
                    action(stdscr)
        elif key == 27:  # ESC-Taste zum Beenden
            break

        stdscr.refresh()

def manual_block_menu(stdscr):
    current_index = 0
    current_page = 0

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        header_lines = 2
        footer_lines = 3  # Reserve 3 lines for page indicator and padding

        available_rows = max_y - header_lines - footer_lines

        if not sites:
            stdscr.addstr(0, 0, "Keine Seiten verfügbar zum Blockieren.", curses.color_pair(1))
            stdscr.refresh()
            stdscr.getch()
            break

        max_button_width = max(len(name) for name, _ in sites) + 2
        cols = max_x // max_button_width
        if cols == 0:
            cols = 1  # Avoid division by zero

        rows = available_rows
        page_size = cols * rows
        total_pages = (len(sites) + page_size - 1) // page_size

        # Hinweis zur Navigation anzeigen
        stdscr.addstr(0, 0, "ESC drücken, um zurückzukehren.", curses.color_pair(1))

        # Get the items for the current page
        page_start = current_page * page_size
        page_end = min(page_start + page_size, len(sites))
        page_sites = sites[page_start:page_end]

        # Sites in einem Gitter anzeigen
        for idx, (name, _) in enumerate(page_sites):
            col = idx % cols
            row = idx // cols
            x = col * max_button_width
            y = row + header_lines

            if idx == current_index:
                stdscr.addstr(y, x, name, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, name)

        # Draw page indicator
        page_indicator = ""
        if current_page == 0 and total_pages > 1:
            page_indicator = f"{current_page + 1} >"
        elif current_page == total_pages - 1 and total_pages > 1:
            page_indicator = f"< {current_page + 1}"
        elif total_pages > 1:
            page_indicator = f"< {current_page + 1} >"

        stdscr.addstr(max_y - 2, (max_x - len(page_indicator)) // 2, page_indicator)

        draw_version(stdscr)  # Version anzeigen

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            if current_index >= cols:
                current_index -= cols
            else:
                # Go to previous page if possible
                if current_page > 0:
                    current_page -= 1
                    current_index += page_size - cols
        elif key == curses.KEY_DOWN:
            if current_index + cols < len(page_sites):
                current_index += cols
            else:
                # Go to next page if possible
                if current_page < total_pages - 1:
                    current_page += 1
                    current_index %= cols
        elif key == curses.KEY_LEFT:
            if current_index > 0:
                current_index -= 1
            else:
                # At first item, go to previous page if possible
                if current_page > 0:
                    current_page -= 1
                    # Set current_index to last item on previous page
                    current_index = min(len(sites[(current_page + 1) * page_size - page_size:]) - 1, page_size - 1)
        elif key == curses.KEY_RIGHT:
            if current_index < len(page_sites) - 1:
                current_index += 1
            else:
                # At last item, go to next page if possible
                if current_page < total_pages - 1:
                    current_page += 1
                    current_index = 0
        elif key == ord('\n'):
            # Calculate the index of the selected site in the full list
            selected_index = current_page * page_size + current_index
            if selected_index < len(sites):
                selected_site = sites[selected_index]
                site_name = extract_site_name(selected_site[0])
                domains = selected_site[1]
                total_domains = len(domains)
                domains_blocked = 0
                for domain, ip_address in domains:
                    block_ip(ip_address, domain)
                    domains_blocked += 1
                    percentage = int((domains_blocked / float(total_domains)) * 100)
                    loading_screen(stdscr, ip_address, site_name, percentage)
                stdscr.clear()
                message = f"{site_name} wurde blockiert!"
                stdscr.addstr(max_y // 2, (max_x - len(message)) // 2, message)
                stdscr.refresh()
                time.sleep(2)
        elif key == 27:  # ESC
            break

def game_block_menu(stdscr):
    current_index = 0
    current_page = 0

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        header_lines = 2
        footer_lines = 3  # Reserve 3 lines for page indicator and padding

        available_rows = max_y - header_lines - footer_lines

        try:
            max_button_width = max(len(name) for name, _ in game_sites) + 2
        except ValueError:
            max_button_width = 20  # Fallback-Wert, falls game_sites leer ist

        cols = max_x // max_button_width
        if cols == 0:
            cols = 1  # Avoid division by zero

        rows = available_rows
        page_size = cols * rows
        total_pages = (len(game_sites) + page_size - 1) // page_size

        # Hinweis zur Navigation anzeigen
        stdscr.addstr(0, 0, "ESC drücken, um zurückzukehren.", curses.color_pair(1))

        # Get the items for the current page
        page_start = current_page * page_size
        page_end = min(page_start + page_size, len(game_sites))
        page_sites = game_sites[page_start:page_end]

        # Sites in einem Gitter anzeigen
        for idx, (name, _) in enumerate(page_sites):
            col = idx % cols
            row = idx // cols
            x = col * max_button_width
            y = row + header_lines

            if idx == current_index:
                stdscr.addstr(y, x, name, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, name)

        # Draw page indicator
        page_indicator = ""
        if current_page == 0 and total_pages > 1:
            page_indicator = f"{current_page + 1} >"
        elif current_page == total_pages - 1 and total_pages > 1:
            page_indicator = f"< {current_page + 1}"
        elif total_pages > 1:
            page_indicator = f"< {current_page + 1} >"

        stdscr.addstr(max_y - 2, (max_x - len(page_indicator)) // 2, page_indicator)

        draw_version(stdscr)
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            if current_index >= cols:
                current_index -= cols
            else:
                # Go to previous page if possible
                if current_page > 0:
                    current_page -= 1
                    current_index += page_size - cols
        elif key == curses.KEY_DOWN:
            if current_index + cols < len(page_sites):
                current_index += cols
            else:
                # Go to next page if possible
                if current_page < total_pages - 1:
                    current_page += 1
                    current_index %= cols
        elif key == curses.KEY_LEFT:
            if current_index > 0:
                current_index -= 1
            else:
                # At first item, go to previous page if possible
                if current_page > 0:
                    current_page -= 1
                    # Set current_index to last item on previous page
                    previous_page_sites = game_sites[(current_page) * page_size : (current_page + 1) * page_size]
                    current_index = min(len(previous_page_sites) - 1, page_size - 1)
        elif key == curses.KEY_RIGHT:
            if current_index < len(page_sites) - 1:
                current_index += 1
            else:
                # At last item, go to next page if possible
                if current_page < total_pages - 1:
                    current_page += 1
                    current_index = 0
        elif key == ord('\n'):
            # Calculate the index of the selected site in the full list
            selected_index = current_page * page_size + current_index
            if selected_index < len(game_sites):
                selected_site = game_sites[selected_index]
                site_name = extract_site_name(selected_site[0])
                for domain, ip_address in selected_site[1]:
                    loading_screen(stdscr, ip_address, site_name, 100)
                    block_ip(ip_address, domain)
                stdscr.clear()
                message = f"{site_name} wurde blockiert!"
                stdscr.addstr(max_y // 2, (max_x - len(message)) // 2, message)
                stdscr.refresh()
                time.sleep(2)
        elif key == 27:  # ESC to exit
            break

def strict_mode_menu(stdscr):
    current_index = 0
    current_page = 0

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        header_lines = 2
        footer_lines = 3  # Reserve 3 lines for page indicator and padding

        available_rows = max_y - header_lines - footer_lines

        if not strict_sites:
            stdscr.addstr(0, 0, "Keine strengen Seiten verfügbar zum Blockieren.", curses.color_pair(1))
            stdscr.refresh()
            stdscr.getch()
            break

        max_button_width = max(len(name) for name, _ in strict_sites) + 2
        cols = max_x // max_button_width
        if cols == 0:
            cols = 1  # Avoid division by zero

        rows = available_rows
        page_size = cols * rows
        total_pages = (len(strict_sites) + page_size - 1) // page_size

        # Hinweis zur Navigation anzeigen
        stdscr.addstr(0, 0, "ESC drücken, um zurückzukehren.", curses.color_pair(1))

        # Get the items for the current page
        page_start = current_page * page_size
        page_end = min(page_start + page_size, len(strict_sites))
        page_sites = strict_sites[page_start:page_end]

        # Sites in einem Gitter anzeigen
        for idx, (name, _) in enumerate(page_sites):
            col = idx % cols
            row = idx // cols
            x = col * max_button_width
            y = row + header_lines

            if idx == current_index:
                stdscr.addstr(y, x, name, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, name)

        # Draw page indicator
        page_indicator = ""
        if current_page == 0 and total_pages > 1:
            page_indicator = f"{current_page + 1} >"
        elif current_page == total_pages - 1 and total_pages > 1:
            page_indicator = f"< {current_page + 1}"
        elif total_pages > 1:
            page_indicator = f"< {current_page + 1} >"

        stdscr.addstr(max_y - 2, (max_x - len(page_indicator)) // 2, page_indicator)

        draw_version(stdscr)  # Version anzeigen

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            if current_index >= cols:
                current_index -= cols
            else:
                # Go to previous page if possible
                if current_page > 0:
                    current_page -= 1
                    current_index += page_size - cols
        elif key == curses.KEY_DOWN:
            if current_index + cols < len(page_sites):
                current_index += cols
            else:
                # Go to next page if possible
                if current_page < total_pages - 1:
                    current_page += 1
                    current_index %= cols
        elif key == curses.KEY_LEFT:
            if current_index > 0:
                current_index -= 1
            else:
                # At first item, go to previous page if possible
                if current_page > 0:
                    current_page -= 1
                    current_index = min(len(strict_sites[(current_page + 1) * page_size - page_size:]) - 1, page_size - 1)
        elif key == curses.KEY_RIGHT:
            if current_index < len(page_sites) - 1:
                current_index += 1
            else:
                # At last item, go to next page if possible
                if current_page < total_pages - 1:
                    current_page += 1
                    current_index = 0
        elif key == ord('\n'):
            # Calculate the index of the selected site in the full list
            selected_index = current_page * page_size + current_index
            if selected_index < len(strict_sites):
                selected_site = strict_sites[selected_index]
                site_name = extract_site_name(selected_site[0])
                domains = selected_site[1]
                total_domains = len(domains)
                domains_blocked = 0
                for domain, ip_address in domains:
                    block_ip(ip_address, domain)
                    domains_blocked += 1
                    percentage = int((domains_blocked / float(total_domains)) * 100)
                    loading_screen(stdscr, ip_address, site_name, percentage)
                stdscr.clear()
                message = f"{site_name} wurde blockiert!"
                stdscr.addstr(max_y // 2, (max_x - len(message)) // 2, message)
                stdscr.refresh()
                time.sleep(2)
        elif key == 27:  # ESC
            break

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) #Halt Logo Farbe
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK) #Farbe für die Version unten rechts
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) #Farbe für die Überschriften also "Support", "Blockieren", "Weitere Versionen"
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK) # Farbe fr "Mit Pfeiltasten scrollen ding bei "Info"
    main_menu(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
