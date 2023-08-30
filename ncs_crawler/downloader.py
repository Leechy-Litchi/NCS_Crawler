import json
import requests

class Downloader:
    def __init__(self, args):
        self.rpc = args.rpc
        self.headers = {'Content-Type': 'application/json'}
        self.password = args.password
        self.dest = args.destination

    def addUri(self,url,filename):
        jsonrpc = {
            "jsonrpc": "2.0",
            "method": "aria2.addUri",
            "id": "",
            "params": ["token:"+self.password, [url[0]], {'dir':self.dest,'out':filename+".mp3"}]
        }    
        requests.post(url=self.rpc,data=json.dumps(jsonrpc))  
        if len(url)>1:
            self.addUri([url[1]],self.dest,filename+" (Instrument)") 

    def redownload(self,trdict):
        import time
        import os
        while self.tellActive()!=0:
            time.sleep(1)
        files = os.listdir(self.dest)
        redownloadFiles = []
        for file in files:
            # if os.path.isdir(file):
                filesplit = os.path.splitext(file)
                if filesplit[-1] == ".aria2":
                    # files.index(file)
                    redownloadFiles.append(filesplit[0])
        print(redownloadFiles)
        for i in redownloadFiles:
            os.remove(i+".mp3")
            os.remove(i+".aria2")
            if i[:-12] != "(Instrument)":
                index = trdict["filename"].index(i)
                requests(trdict["urls"][index][0],i)
            else:
                index = trdict["filename"][:-12].index(i)
                requests(trdict["urls"][index][1],i)
    def tellActive(self):
        jsonrpc = {
            "jsonrpc": "2.0",
            "method": "aria2.tellActive",
            "id": "",
            "params": ["token:"+self.password]
        }    
        response = requests.post(url=self.rpc,data=json.dumps(jsonrpc))          
        return len(json.loads(response.content)["result"])