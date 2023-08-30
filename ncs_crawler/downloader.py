import json
import requests
import os


class Downloader:
    def __init__(self, args):
        self.rpc = args.rpc
        self.headers = {'Content-Type': 'application/json'}
        self.password = args.password
        self.destination = args.destination

    def addUri(self,url,filename):
        jsonrpc = {
            "jsonrpc": "2.0",
            "method": "aria2.addUri",
            "id": "",
            "params": ["token:"+self.password, [url[0]], {'dir':self.destination,'out':filename+".mp3"}]
        }    
        requests.post(url=self.rpc,data=json.dumps(jsonrpc))  
        if len(url)>1:
            self.addUri([url[1]],filename+" (Instrument)") 
    
    def makeLinks(self,trdict):
        import shutil
        for genre in trdict["genres"]:
            try:
                os.mkdir(self.destination+genre)
            except FileExistsError:
                pass
        index = 0
        for filename in trdict["filename"]:
            if trdict["moods"][index] == []:
                firstmood = ""
            else:
                firstmood = trdict["moods"][index][0]
            firstmoodpath = self.destination+trdict["genres"][index]+"/"+firstmood
            if os.path.exists(firstmoodpath)!=True:
                os.mkdir(firstmoodpath)
            try:
                shutil.move(self.destination+"/"+filename+".mp3",firstmoodpath+"/"+filename+".mp3")
                shutil.move(self.destination+"/"+filename+" (Instrument).mp3",firstmoodpath+"/"+filename+" (Instrument).mp3")
            except FileNotFoundError:
                pass
            except FileExistsError:
                pass
            for moods in trdict["moods"][index][1:]:
                moodpath = self.destination+trdict["genres"][index]+"/"+moods
                if os.path.exists(moodpath)!=True:
                    os.mkdir(moodpath)
                try:
                    os.symlink(firstmoodpath+"/"+filename+".mp3",moodpath+"/"+filename+".mp3")
                    if os.path.exists(firstmoodpath+"/"+filename+" (Instrument).mp3"):
                        os.symlink(firstmoodpath+"/"+filename+" (Instrument).mp3",moodpath+"/"+filename+" (Instrument).mp3")
                except FileExistsError:
                    pass                            
            index += 1

    def redownload(self,trdict):
        import time
        while self.tellActive()!=0:
            time.sleep(1)
        files = os.listdir(self.destination)
        redownloadFiles = []
        for file in files:
            # if os.path.isdir(file):
                filesplit = os.path.splitext(file)
                if filesplit[-1] == ".aria2":
                    # files.index(file)
                    redownloadFiles.append(filesplit[0])
        for i in redownloadFiles:
            os.remove(i+".mp3")
            os.remove(i+".aria2")
            if i[:-12] != "(Instrument)":
                index = trdict["filename"].index(i)
                addUri(trdict["urls"][index][0],i)
            else:
                index = trdict["filename"][:-12].index(i)
                addUri(trdict["urls"][index][1],i)
        self.makeLinks(trdict)

    def tellActive(self):
        jsonrpc = {
            "jsonrpc": "2.0",
            "method": "aria2.tellActive",
            "id": "",
            "params": ["token:"+self.password]
        }    
        response = requests.post(url=self.rpc,data=json.dumps(jsonrpc))    
        return len(json.loads(response.content)["result"])
    
