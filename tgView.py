import os
import requests
import threading
import time
from colorama import Fore

# Constants
N_THREADS = 400  # Number of threads
PROXY_RETRY_ATTEMPTS = 3  # Number of retry attempts for proxies
BOT_TOKEN = '8095096286:AAGtId-d51HL7ezrDnqffKeQ4WF9ONEMieI'  # Your bot token

threads = []  # Thread list

# Print introductory messages
print('[══════════════════[TOOL BY @Itz_Your_4Bhi]══════════════════]')
print('\n')
print('••••••••• ' + Fore.LIGHTCYAN_EX + 'Tool By @Itz_Your_4Bhi' + Fore.LIGHTWHITE_EX +  ' ••••••••')
print('\n')
print('[══════════════════[@Itz_Your_4Bhi]══════════════════]')
print('\n\n')

# Get input from the user for the post link
print(Fore.BLUE + 'Enter Your Post link.')
link1 = input(Fore.LIGHTMAGENTA_EX + 'Post Link 1: ' + Fore.LIGHTYELLOW_EX)
print('\n')
print('----------------------------Tool Started/-------------------------')
print('\n')

def view2(proxy):
    """ Sends views using a given proxy """
    channel = link1.split('/')[3]
    msgid = link1.split('/')[4]
    send_seen(channel, msgid, proxy)

def send_seen(channel, msgid, proxy):
    """ Sends the view to the specified channel and message ID """
    s = requests.Session()
    proxies = {'http': proxy, 'https': proxy}
    
    # First request to get cookie
    for attempt in range(PROXY_RETRY_ATTEMPTS):
        try:
            response = s.get(f"https://t.me/{channel}/{msgid}", timeout=10, proxies=proxies)
            cookie = response.headers['set-cookie'].split(';')[0]
            break
        except requests.RequestException as e:
            print(f"Error getting cookie (attempt {attempt + 1}): {e}")
            if attempt < PROXY_RETRY_ATTEMPTS - 1:
                time.sleep(1)
            else:
                return
    
    headers = {
        "Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie, "Host": "t.me", "Referer": f"https://t.me/{channel}/{msgid}?embed=1",
        "User-Agent": "Chrome"
    }
    data = {"_rl": "1"}
    
    # Second request to send view
    for attempt in range(PROXY_RETRY_ATTEMPTS):
        try:
            response = s.post(f'https://t.me/{channel}/{msgid}?embed=1', json=data, headers=headers, proxies=proxies)
            key = response.text.split('data-view="')[1].split('"')[0]
            now_view = response.text.split('<span class="tgme_widget_message_views">')[1].split('</span>')[0]
            if "K" in now_view:
                now_view = now_view.replace("K", "00").replace(".", "")
            break
        except requests.RequestException as e:
            print(f"Error sending view (attempt {attempt + 1}): {e}")
            if attempt < PROXY_RETRY_ATTEMPTS - 1:
                time.sleep(1)
            else:
                return
    
    headers.update({
        "X-Requested-With": "XMLHttpRequest"
    })
    
    # Third request to verify view
    for attempt in range(PROXY_RETRY_ATTEMPTS):
        try:
            response = s.get(f'https://t.me/v/?views={key}', timeout=10, headers=headers, proxies=proxies)
            if response.text == "true":
                print(Fore.LIGHTGREEN_EX + 'View sent [✅]' + Fore.LIGHTCYAN_EX + f' Sent: {now_view}')
            break
        except requests.RequestException as e:
            print(f"Error verifying view (attempt {attempt + 1}): {e}")
            if attempt < PROXY_RETRY_ATTEMPTS - 1:
                time.sleep(1)
            else:
                return

def scrap():
    """ Fetches and saves proxy lists """
    try:
        https_proxies = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=https&timeout=0", timeout=5).text
        http_proxies = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=0", timeout=5).text
        socks_proxies = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=0", timeout=5).text
    except requests.RequestException as e:
        print(f"Error fetching proxies: {e}")
        return False
    
    with open("proxies.txt", "w") as f:
        f.write(https_proxies + "\n" + http_proxies)
    
    with open("socks.txt", "w") as f:
        f.write(socks_proxies)
    
    return True

def checker(proxy):
    """ Worker function for each thread to process views """
    try:
        view2(proxy)
    except Exception as e:
        print(f"Error in checker: {e}")

def start():
    """ Starts the proxy fetching and view sending process """
    if not scrap():
        return
    
    # Read proxies from files
    with open('proxies.txt', 'r') as f:
        proxies = f.readlines()
    
    for p in proxies:
        p = p.strip()
        if p:
            while threading.active_count() > N_THREADS:
                time.sleep(1)
            thread = threading.Thread(target=checker, args=(p,))
            threads.append(thread)
            thread.start()
    
    with open('socks.txt', 'r') as f:
        proxies = f.readlines()
    
    for p in proxies:
        p = p.strip()
        if p:
            while threading.active_count() > N_THREADS:
                time.sleep(1)
            proxy = "socks5://" + p
            thread = threading.Thread(target=checker, args=(proxy,))
            threads.append(thread)
            thread.start()

def process(run_forever=False):
    """ Controls the execution of the view sending process """
    if run_forever:
        while True:
            start()
            time.sleep(60)  # Adjust the sleep duration as needed
    else:
        start()

process(False)
