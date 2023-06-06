import requests
import re
from threading import Thread
import time
from random import randint
import string
import random
import pyfiglet
from rich import print
title = pyfiglet.figlet_format('Kre \n Verifier')
print(f'[red]{title}[/red]')
def get_proxy():
    cookies = open("proxies.txt").read()
    lines = cookies.split("\n")
    num_lines = len(lines)
    i = randint(0, num_lines - 1)
    return lines[i]



def get_inbox(email):

    response = requests.get(
        f"https://lasagna.email/api/inbox/{email}",
        proxies={"https": f"http://{get_proxy()}", "http": f"http://{get_proxy()}"},
    )
    return response.json()["emails"][0]["Body"]


def csrf(cookie, proxy):
 try:
    csr = requests.post(
        "https://friends.roblox.com/v1/contacts/1/request-friendship",
        cookies={".ROBLOSECURITY": cookie},
        proxies={"https": f"http://{proxy}", "http": f"http://{proxy}"},
    ).headers
    # print(csr)
    return csr["x-csrf-token"]
 except:
     print("[red]Invalid cookie[/red]")
     pass


def verify(cookie):
    try:
        extractor = URLExtract()

        proxy = get_proxy()
        email = res = ''.join(random.choices(string.ascii_lowercase
                             , k=10)) + "@lasagna.email"
        print(email)
        cookies = {".ROBLOSECURITY": cookie}
        resp = requests.post(
            "https://accountsettings.roblox.com/v1/email",
            cookies=cookies,
            proxies={"https": f"http://{proxy}", "http": f"http://{proxy}"},
            headers={"x-csrf-token": csrf(cookie, proxy)},
            json={"emailAddress": email},
        )
        ver = requests.post(
            "https://accountsettings.roblox.com/v1/email/verify",
            proxies={"https": f"http://{proxy}", "http": f"http://{proxy}"},
            cookies=cookies,
            headers={"x-csrf-token": csrf(cookie, proxy)},
        )
        print(str(ver.text) + str(resp.text))

        if resp.status_code == 200 and ver.status_code == 200:
            time.sleep(2)
            msg = get_inbox(email)
            # print(msg)
            link = extractor.find_urls(msg)[5]
            print(link)
            resp2 = requests.post(
                "https://accountinformation.roblox.com/v1/email/verify",
                proxies={"https": f"http://{proxy}", "http": f"http://{proxy}"},
                json={"ticket": str(str(link).split("ticket=")[1]).replace("%3D", "=")},
                cookies=cookies,
                headers={"x-csrf-token": csrf(cookie, proxy)},
            )
            if resp2.status_code == 200:
                print("[green]Successfully verified[/green]")
            else:
                print("[red]Failed to verify[/red]")
    except:
        print("[red]Error occured[/red]")
        pass


cookies = open("cookies.txt").read().splitlines()

threads = []
print("[yellow]How many threads?[/yellow]")
for i in range(int(input(""))):
    thread_cookies = cookies[i::4]
    thread = Thread(
        target=lambda c: [verify(cookie) for cookie in c], args=(thread_cookies,)
    )
    thread.start()
    threads.append(thread)

for thread in threads:
    thread
