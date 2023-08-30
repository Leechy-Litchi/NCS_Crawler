import argparse
import logging
import os

def main():
    parser = argparse.ArgumentParser(
        description="Collect no copyright sounds on ncs.io",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    logging.basicConfig(
        format="[ncscrawler:%(filename)s:L%(lineno)d] %(levelname)-6s %(message)s"
    )
    logging.getLogger().setLevel(logging.INFO)

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="out.json",
        help="save urls as a file, ../Download/out.json as default",
    )
    parser.add_argument(
        "-a",
        "--aria2",
        help="use rpc to download",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        default="9999",
        help="set end page",
    )    
    parser.add_argument(
        "-r",
        "--rpc",
        type=str,
        default="http://127.0.0.1:6800/jsonrpc",
        help="rpc url, http://127.0.0.1:6800/jsonrpc as default",
    )    
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        default="",
        help="rpc secret",
    )   
    parser.add_argument(
        "-d",
        "--destination",
        type=str,
        default=os.getcwd()+"/../Download/",
        help="aria download destination, ../Download/ as default",
    )        
    parser.add_argument(
        "-m",
        "--makelinks",
        type=str,
        default=os.getcwd()+"/../Download/out.json",
        help="make soft links by json file, ../Download/out.json as default",
    )      
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=os.getcwd()+"/../input.json",
        help="input json file to download, ../input.json as default",
    )          
    
    args = parser.parse_args()

    from crawler import Crawler
    import json

    from downloader import Downloader
    Downloader = Downloader(args)

    if args.makelinks and os.path.exists(args.makelinks):
        trdict = json.load(open(args.makelinks))
        Downloader.makeLinks(trdict=trdict)
        return        
        
    if os.path.exists(args.input):
        trdict = json.load(open(args.input))
    else:
        trdict = Crawler(args).run()


    if args.aria2:
        index = 0
        while index<len(trdict["urls"]):
            Downloader.addUri(trdict["urls"][index],trdict["filename"][index])
            index += 1
        Downloader.redownload(trdict=trdict)
            
            


if __name__ == "__main__":
    main()
    