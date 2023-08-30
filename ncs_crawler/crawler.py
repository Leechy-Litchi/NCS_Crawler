import logging
import os
from bs4 import BeautifulSoup
import requests
import json
import threading


MAIN_PAGE_URL = "https://ncs.io/music-search?q=&genre=&page="

class Crawler:
    def __init__(self, args):
        self.args = args

    def saveFile(self,trdict):
        outjson = self.args.destination+self.args.output
        with open(outjson,mode='w',encoding='utf-8') as file:
            json.dump(trdict,fp=file)
            file.close()

    def crawl(self,pages,trdict):
            req = requests.get(MAIN_PAGE_URL+str(pages)).content
            soup = BeautifulSoup(req,"lxml")
            alltrs = soup.find_all("tr")
            if len(alltrs)==1:
                return False
            trcounts = 0
            for trs in alltrs:
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
                                filename = filename.replace(","," &")
                                filename = filename.replace("/","／")
                                trdict["filename"].append(filename)
                            case 5:
                                moods = []
                                for tags in tds.find_all("a"):
                                    # need to optimize
                                    if len(trdict["genres"])-20*(pages-1)<trcounts-1:
                                        trdict["genres"].append(tags.text.replace("/","／"))
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
            print("Loading Pages:"+str(pages))  
            return True

    def run(self):
        pages = 1     
        trdict = {"filename":[],"genres":[],"moods":[],"urls":[]}   
        while pages<=self.args.end:
            if self.crawl(pages,trdict):
                pages += 1                 
            else:
                break
        self.saveFile(trdict) 
        return trdict
        
