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



def checkRedir(url, spam_link_domains, redir_depth, spamCaseResultSet):
    if redir_depth == 0:
        spamCaseResultSet.add(False)
        return

    elif redir_depth < 0:
        print("error case 1")

    res = requests.get(url)

    # 1. Check direct redirection (status code)

    # Direct redirection occured
    if res.status_code == 301 or res.status_code == 302:
        if checkSpamDirectly(res.url, spam_link_domains):
            spamCaseResultSet.add(True)
            return
        else:
            checkRedir(res.url, spam_link_domains, redir_depth - 1)
            return

    elif res.ok:
        # 2. Check undirect redirection (html <a> including)
        html = BeautifulSoup(res.text, 'html.parser')
        all_as = html.find_all("a")
        all_hrefs = set()

        for each_a in all_as:
            href = each_a.attrs['href']
            if checkSpamDirectly(href, spam_link_domains):
                spamCaseResultSet.add(True)
                return
            all_hrefs.add(href)

        if len(all_hrefs) == 0:
            spamCaseResultSet.add(True)
            return

        elif len(all_hrefs) == 1:
            for each_href in all_hrefs:
                checkRedir(each_href, spam_link_domains, redir_depth - 1)
            return

        elif len(all_hrefs) > 1:
            procs = []
            for each_href in all_hrefs:
                proc = Process(target=checkRedir, args=(each_href, spam_link_domains, redir_depth-1, spamCaseResultSet))
                procs.append(proc)
                proc.start()

            for proc in procs:
                proc.join()

    else:
        spamCaseResultSet.add(False)
        return



def isSpam(content, spam_link_domains, redir_depth):
    spamCaseResultSet = set()
    spamCaseLinkSet = set()

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
        # Firstly check link text directly included spam link or not
        if checkSpamDirectly(each_link, spam_link_domains):
            return True

        # Secondly check whether redirection include spam cases
        proc = Process(target=checkRedir, args=(each_link, spam_link_domains, redir_depth, spamCaseResultSet))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    if True in spamCaseResultSet:
        return True

    # If there are not any cases that return True, it should not be spam mail
    return False



if __name__ == '__main__':
    isSpam("spam spam https://www.sample.com http://www.sample2.com", ["txtx"], 1)
    # isSpam("spam spam", ["txtx"], 3)