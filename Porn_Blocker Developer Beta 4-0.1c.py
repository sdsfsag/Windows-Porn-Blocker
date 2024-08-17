import curses
import time
import subprocess

# Liste von Webseiten, IP-Adressen und zugehörigen Domains
sites = [
    ("PornHub ~ 27 Sekunden", [
        ("pornhub.com", "66.254.114.41"),
        ("pornhub-deutsch.net", "216.18.168.20"),
        ("fr.pornhub.org", "66.254.114.41"),
        ("rt.pornhub.org", "66.254.114.41"),
        ("de.pornhubpremium.com", "66.254.114.33"),
        ("es.pornhub.com", "66.254.114.41")
    ]),
    ("xHamster ~ 24 Sekunden", [
        ("xhamster.com", "88.208.60.136"),
        ("ge.xhamster.desi", "172.67.202.84"),
        ("xhopen.com", "185.207.236.242"),
        ("ge.xhamster2.com", "104.21.16.210"),
        ("ge.xhamster1.des", "172.67.158.52")
    ]),
    ("Hentai Haven ~ 45 Sekunden", [
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
    ("XVIDEOS ~ 29 Sekunden", [
        ("xvideos.com", "185.88.181.3"),
        ("xvideos3.com", "172.64.153.203"),
        ("xvideos2.com", "172.64.155.85"),
        ("xvideos5.com", "104.18.54.128"),
        ("xvideos4.com", "104.18.43.33"),
        ("xvideos.es", "172.64.144.205"),
        ("de.xvideos.com", "185.88.181.10")
    ]),
    ("XNXX ~ 27 Sekunden", [
        ("www.xnxx.com", "185.88.181.58"),
        ("xnxx.health", "104.26.5.154"),
        ("xnxx.de", "141.0.173.169"),
        ("xnxx2.com", "104.18.34.49"),
        ("xnxx.tv", "172.64.145.87"),
        ("xnxx.rest", "172.67.160.119")
    ]),
    ("The Porn dude ~ 21 Sekunden", [
        ("theporndude.com", "104.19.131.104"),
        ("theporndude.vip", "104.21.28.16"),
        ("theporndude.org", "172.67.73.96"),
        ("theporndude.net", "104.26.1.220")
    ]),
    ("hAnime ~ 27 Sekunden", [
        ("hanime.tv", "104.21.234.245"),
        ("hanimehentai.tv", "104.21.12.52"),
        ("hanimes.org", "172.67.151.98"),
        ("hanime.watch", "172.67.194.230"),
        ("hanime.su", "104.21.19.5"),
        ("hanime.baby", "172.67.158.157"),
    ])    

]   

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

    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Blockieren der IP-Adresse für {domain}: {e}")

def loading_screen(stdscr, ip_address, duration, total_duration):
    stdscr.clear()
    stdscr.addstr(0, 0, "Bitte warten...")
    stdscr.refresh()
    steps = 10
    step_duration = total_duration / steps
    for i in range(steps):
        if i == 2:
            stdscr.addstr(1, 0, f"IP gefunden: {ip_address}")
        if i == 6:
            stdscr.addstr(1, 0, "Blockiere...")
            stdscr.refresh()
            time.sleep(duration)
        stdscr.addstr(3, 0, "[" + "#" * (i + 1) + " " * (steps - 1 - i) + "]")
        stdscr.refresh()
        time.sleep(step_duration)

def main(stdscr):
    curses.curs_set(0)
    current_index = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Welche Seite willst du blockieren?")
        stdscr.addstr(1, 0, "_______________________________")

        for i, (name, _) in enumerate(sites):
            if i == current_index:
                stdscr.addstr(3 + i, 0, f"{name}", curses.A_REVERSE)
            else:
                stdscr.addstr(3 + i, 0, f"{name}")
        
        # Fenstergröße ermitteln
        max_y, max_x = stdscr.getmaxyx()
        

        stdscr.addstr(max_y - 1, max_x - len("Developer Beta 4-0.1c") - 1, "Developer Beta 4-0.1c")

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            current_index = (current_index + 1) % len(sites)
        elif key == curses.KEY_UP:
            current_index = (current_index - 1) % len(sites)
        elif key == ord('\n'):
            selected_site, domains = sites[current_index]
            loading_screen(stdscr, domains[0][1], 3, 5)
            for domain, ip_address in domains:
                loading_screen(stdscr, ip_address, 1, 2)
                block_ip(ip_address, domain)
            stdscr.clear()
            stdscr.addstr(0, 0, f"{selected_site} wurde erfolgreich blockiert!")
            stdscr.addstr(3, 0, "Programm wird beendet...")
            
            # Fenstergröße ermitteln
            max_y, max_x = stdscr.getmaxyx()
            
            # "Developer Beta 4-0.1b" unten rechts hinzufügen
            stdscr.addstr(max_y - 1, max_x - len("Developer Beta 4-0.1c") - 1, "Developer Beta 4-0.1c")

            stdscr.refresh()
            time.sleep(7)
            break

curses.wrapper(main)
