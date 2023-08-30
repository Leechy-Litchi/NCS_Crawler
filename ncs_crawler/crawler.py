import logging
import os
from bs4 import BeautifulSoup
import requests
import json


MAIN_PAGE_URL = "https://ncs.io/music-search?q=&genre=&page="

class Crawler:
    def __init__(self, args):
        self.args = args
    def saveFile(self,trdict):
        json.dump(trdict,fp=open(self.args.output,"w+"))
    def run(self):
        pages = "1"
        req = requests.get(MAIN_PAGE_URL+pages).content
        soup = BeautifulSoup(req,"lxml")
        trcounts = 0
        trdict = {"filename":[],"genres":[],"moods":[],"urls":[]}
        for trs in soup.find_all("tr"):
            if trcounts < 2:
                trcounts += 1
            else:
                tdcounts = 0
                for tds in trs.find_all("td"):
                    if tdcounts < 3:
                        tdcounts += 1
                        continue
                    else:
                        tdcounts += 1
                    match tdcounts:
                        case 4:
                            filename = tds.find("span").text+" - "+tds.find("p").text
                            filename = filename.replace(",","&")
                            trdict["filename"].append(filename)
                        case 5:
                            moods = []
                            for tags in tds.find_all("a"):
                                if len(trdict["genres"])<trcounts-1:
                                    trdict["genres"].append(tags.text)
                                else:
                                    moods.append(tags.text)
                            trdict["moods"].append(moods)
                        # TODO: 6 compare update time

                        case 7:
                            urlcount = len(tds.text.split(","))
                        case 8:
                            a = tds.find("a")["data-tid"]
                            if urlcount>1:
                                url = ["https://ncs.io/track/download/"+a,"https://ncs.io/track/download/i_"+a]
                                trdict["urls"].append(url)
                            else:
                                trdict["urls"].append(["https://ncs.io/track/download/"+a])
                trcounts += 1       
        self.saveFile(trdict)                     
        return trdict
        
