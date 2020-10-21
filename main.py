import re
from pprint import pprint
# from threading import Thread
from multiprocessing import Process

import requests
from bs4 import BeautifulSoup

def checkSpamDirectly(each_link, spam_link_domains):
    for each_spam_link in spam_link_domains:
        if each_spam_link in each_link:
            return True

    return False

def checkRedir(url, spam_link_domains, redir_depth):
    if redir_depth == 0:
        return False

    elif redir_depth < 0:
        print("error case 1")

    res = requests.get(url)

    # 1. Check direct redirection (status code)

    # Direct redirection occured
    if res.status_code == 301 or res.status_code == 302:
        if checkSpamDirectly(res.url, spam_link_domains):
            return True
        else:
            return checkRedir(res.url, spam_link_domains, redir_depth-1)

    elif res.ok:
        # 2. Check undirect redirection (html <a> including)
        html = BeautifulSoup(res.text, 'html.parser')
        all_as = html.find_all("a")
        all_hrefs = set()

        for each_a in all_as:
            href = each_a.attrs['href']
            if checkSpamDirectly(href, spam_link_domains):
                return True
            all_hrefs.add(href)

        for each_href in all_hrefs:
            if checkRedir(each_href, spam_link_domains, redir_depth-1):
                return True

        return False

    else:
        return False



def isSpam(content, spam_link_domains, redir_depth):

    # Check whether there is URL in content
    link_regex = re.compile(r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    pre_links = re.findall(link_regex, content)
    links = [each_link[0] for each_link in pre_links]

    if not links:
        return False
    else:
        pprint(links)

    # Check each links whether connected to spam link or not
    # procs = []
    for each_link in links:
        # Firstly check link directly included spam link or not
        if checkSpamDirectly(each_link, spam_link_domains):
            return True

        # Secondly check whether redirection exists or not
        if checkRedir(each_link, spam_link_domains, redir_depth):
            return True

    return False

    # Make Http request Parellely by multiprocesessing
    # proc = Process(target=makeHttpRequest, args=each_link)
    # procs.append(proc)
    # proc.start()

    # for proc in procs:
    #     proc.join()


    # pool = Pool(processes=len(links))
    # pool.map(makeHttpRequest())



def main():
    isSpam("spam spam https://www.sample.com http://www.sample2.com", ["txtx"], 3)
    # isSpam("spam spam", ["txtx"], 3)

main()