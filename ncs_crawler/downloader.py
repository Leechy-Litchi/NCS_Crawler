import json
import requests
class Downloader:
    def __init__(self, args):
        self.rpc = args.rpc
        self.headers = {'Content-Type': 'application/json'}
        self.password = args.password

    def request(self,url,dest,filename):
        jsonrpc = {
            "jsonrpc": "2.0",
            "method": "aria2.addUri",
            "id": "",
            "params": ["token:"+self.password, [url[0]], {'dir':dest,'out':filename}]
        }    
        requests.post(url=self.rpc,data=json.dumps(jsonrpc))  
        if len(url)>1:
            self.request([url[1]],dest,filename+" (Instrument)")        
