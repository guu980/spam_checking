import re
from pprint import pprint
# from threading import Thread
from multiprocessing import Process

import requests
from bs4 import BeautifulSoup

def makeHttpRequest(url):
    req = requests.get(url)

    # 1. Check direct redirection (status code)
    # extract url from Content

    # 2. Check undirect redirection (html <a> including)



def isSpam(content, spam_link_domains, redirectionPath):
    result = False

    # Check whether there is URL in content
    link_regex = re.compile(r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    pre_links = re.findall(link_regex, content)
    links = [each_link[0] for each_link in pre_links]

    if not links:
        return False
    else:
        pprint(links)

    # Check each links whether connected to spam link or not
    procs = []
    for each_link in links:
        # Firstly check link directly included spam link or not
        for each_spam_link in spam_link_domains:
            if each_spam_link in each_link:
                result = True
                return result

        # Secondly check whether redirection exists or not
        # Make Http request Parellely by multiprocesessing
        proc = Process(target=makeHttpRequest, args=each_link)
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()


    # pool = Pool(processes=len(links))
    # pool.map(makeHttpRequest())

    return result

def main():
    isSpam("spam spam https://www.sample.com http://www.sample2.com", ["txtx"], 3)
    # isSpam("spam spam", ["txtx"], 3)

main()