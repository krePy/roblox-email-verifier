import requests
import re
from threading import Thread
import time
from random import randint
def get_proxy():
    cookies = open("proxies.txt").read()
    lines = cookies.split('\n')
    num_lines = len(lines)
    i = randint(0, num_lines-1)
    return lines[i]
def generate_email():
    cookies = {
    '.AspNetCore.Antiforgery.dXyz_uFU2og': 'CfDJ8E2ZItu0PPFGj4KyvmP5PRQGjFISQv6a6x24_xKcmQ1o2dOQd--8uzn3qdwWOfvSpjFbdkKFP057Adgp3UEVDFf8JdlmgGftbB2BPLaI-51PnsPbL0DEmw0RaFgCxJD1cifw8sQ6SugYRtvs0TfP95Y',
}
    headers = {
    'requestverificationtoken': 'CfDJ8E2ZItu0PPFGj4KyvmP5PRQELrHrAcLJB3EWouCi8ED26ID-YFJ7fxhFqVYhdf8rCfPFUd5qhCirHU784Z8YHDSkR2dO5fpNyceJnpRwCeo0gx-d_iJ34B9_X43DZMOIeOp5cs61LhjJA1qkpJsIDcI',
}
    resp = requests.get("https://tempmailo.com/changemail?_r=0.6912808892321419",proxies={"https": f"http://{get_proxy()}", "http":f"http://{get_proxy()}"}, headers=headers, cookies=cookies)
    return resp.text
def get_inbox(email):
    cookies = {
    '.AspNetCore.Antiforgery.dXyz_uFU2og': 'CfDJ8E2ZItu0PPFGj4KyvmP5PRQGjFISQv6a6x24_xKcmQ1o2dOQd--8uzn3qdwWOfvSpjFbdkKFP057Adgp3UEVDFf8JdlmgGftbB2BPLaI-51PnsPbL0DEmw0RaFgCxJD1cifw8sQ6SugYRtvs0TfP95Y',
    }

    headers = {
    'requestverificationtoken': 'CfDJ8E2ZItu0PPFGj4KyvmP5PRQELrHrAcLJB3EWouCi8ED26ID-YFJ7fxhFqVYhdf8rCfPFUd5qhCirHU784Z8YHDSkR2dO5fpNyceJnpRwCeo0gx-d_iJ34B9_X43DZMOIeOp5cs61LhjJA1qkpJsIDcI',
    }

    json_data = {
    'mail': email,
    }

    response = requests.post('https://tempmailo.com/',proxies={"https": f"http://{get_proxy()}", "http":f"http://{get_proxy()}"}, cookies=cookies, headers=headers, json=json_data)
    return response.text
def csrf(cookie, proxy):
    csr = requests.post("https://friends.roblox.com/v1/contacts/1/request-friendship", cookies={
        '.ROBLOSECURITY': cookie
    },proxies={"https": f"http://{proxy}", "http":f"http://{proxy}"}).headers
    #print(csr)
    return csr["x-csrf-token"]
def verify(cookie):
    proxy = get_proxy()
    email = generate_email()
    print(email)
    cookies = {".ROBLOSECURITY": cookie}
    resp = requests.post("https://accountsettings.roblox.com/v1/email", cookies=cookies,proxies={"https": f"http://{proxy}", "http": f"http://{proxy}"}, headers={"x-csrf-token": csrf(cookie, proxy)}, json={"emailAddress": email})
    ver = requests.post("https://accountsettings.roblox.com/v1/email/verify",proxies={"https": f"http://{proxy}", "http":f"http://{proxy}"}, cookies=cookies, headers={"x-csrf-token": csrf(cookie, proxy)})
    if resp.status_code == 200 and ver.status_code == 200:
        time.sleep(5)
        msg = get_inbox(email)
        #print(msg)
        link = re.search("(?P<url>https?://[^\s]+)", str(msg)).group("url")
        print(str(str(link).split("ticket=")[1]).replace("%3D", "="))
        resp2 = requests.post("https://accountinformation.roblox.com/v1/email/verify",proxies={"https": f"http://{proxy}", "http":f"http://{proxy}"},json={"ticket": str(str(link).split("ticket=")[1]).replace("%3D", "=")}, cookies=cookies,headers={"x-csrf-token": csrf(cookie, proxy)})
        print(resp2.text)
cookies = open("cookies.txt").read().splitlines()

threads = []
for i in range(int(input("How many threads? \n"))):
    thread_cookies = cookies[i::4]
    thread = Thread(target=lambda c: [verify(cookie) for cookie in c], args=(thread_cookies,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread
    
