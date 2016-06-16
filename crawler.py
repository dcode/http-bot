__author__ = 'Matthew'

import urllib2
import sys
import os

dir = os.path.dirname(__file__)
from random import randint
#from timeout import timeout
from datetime import datetime, date

import requests
USER_AGENT = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'}



class Crawler:

    def __init__(self, start, startNum):
        self.startNum = startNum
        self.root = os.path.dirname(__file__)
        self.log = self.root + 'log.txt'
        self.start = start
        self.count = 0
        self.pool = set([])
        self.visited = []
        self.snapshots = []
        self.running = True
        self.startCrawler()

    def getRootLink(self, link):
        raw = link.split("/")[2]
        ret = "http://" + raw
        return ret

    def printLog(self, count, url):
        self.snapshots.append(self.getRootLink(url))
        with open(self.log, "w") as f:
            f.write(str(count) + "\n")
            f.write("\n")
            for item in self.snapshots:
                f.write(item + "\n")

    def getLinks(self, text, parent):
        links = []
        aSplit = text.split('<a href="')[1:]
        for aTag in aSplit:
            linkRaw = aTag.split('"')[0]
            links.append(linkRaw)
        ret = []
        for link in links:
            temp = self.sanitize(link, parent)
            if temp != None:
                ret.append(temp)
        if len(self.pool) < 2000:
            self.pool.update(ret)
        else:
            self.pool = set(ret) #this encourages randomness when backtracking.
        return ret
    
    #@timeout(5)
    def getText(self, link):
        #html = requests.get(url, headers=USER_AGENT).text()
        html = urllib2.urlopen(link, None, 5).read()
        return html

    def specialCases(self, link): #Put special cases here
        # if "/wiki/" == link[:6]: #Example
        #     return True
        # else:
        #     return False
        return True

    def sanitize(self, new, old):
        if not self.specialCases(new):
            return None
        else:
            if new == None or new == "":
                return None
            elif new[:4] == "http":
                return new
            elif new[0] == "/" and old != None and old != "":
                return self.getRootLink(old) + new
            elif new[:3] == "www":
                return "http://" + new
            elif new[:3] == "../":
                pass
            elif new[:3] == "//w":
                return "http:" + new
            elif len(new) > 1000:
                pass
            else:
                pass

    def getRandomFromPool(self):
        if len(self.pool) == 0:
            print("FATAL FAILURE: Pool Empty")
        rand = randint(0,len(self.pool) - 1)
        ret = list(self.pool)[rand]
        self.pool.remove(ret)
        return ret

    def writeResponse(self, text):
        with open(self.response, "a") as f:
            f.write(text + "\n")

    def getRandomLink(self, links):
        if links != []:
            found = False
            ret = ""
            while not found and links != []:
                rand = randint(0,len(links) - 1)
                temp = links[rand]
                if temp not in self.visited:
                    ret = temp
                    found = True
                else:
                    links.remove(temp)
            if ret == "":
                ret = self.getRandomFromPool()
            return ret
        else:
            return self.getRandomFromPool()

    def doStuff(self, HTML, currLink):
        #Whatever side effects you want the crawler to do.
        pass

    def startCrawler(self):
        self.startTime = datetime.now().time()
        curr = self.start
        raw = urllib2.urlopen(curr).read()
        links = self.getLinks(raw, curr)
        failures = 0

        while self.count < self.startNum:
            curr = self.getRandomLink(links)
            try:
                self.visited.append(curr)
                if True:
                    raw = self.getText(curr)
                    links = self.getLinks(raw, curr)
                    print(curr)
                    self.doStuff(raw, curr)
                    self.count += 1
                    if self.count % 50 == 0:
                        self.printLog(self.count, curr)

                else:
                    if len(links) >= 1:
                        pass
                        #print("Crawler failed on: " + curr)

                    else:
                        pass
                        #print("CRAWLER FAIL")

            except:
                failures += 1
                print("url failed: " + curr)
            if failures == 200000:
                print("CRITICAL ERROR: Too many failures on " + curr)
                curr = self.getRandomFromPool()
                failures = 0
        end = datetime.now().time()
        total = datetime.combine(date.today(), end) - \
                datetime.combine(date.today(), self.startTime)
        with open(self.log, "a") as f:
            f.write("Total time: " + str(total) + "\n")
        print("done!")

if __name__ == "__main__":
    crawler = Crawler("http://www.iub.edu", 10) #start link
