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
        help="save urls as a file, out.json as default",
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
        help="end page",
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
        default=os.getcwd()+"/Download/",
        help="aria download destination, ./Download/ as default",
    )         
    
    args = parser.parse_args()

    from crawler import Crawler
    import time
    import random
    trdict = Crawler(args).run()
    if args.aria2:
        from downloader import Downloader
        Downloader = Downloader(args)
        index = 0
        while index<len(trdict["urls"]):
            Downloader.request(trdict["urls"][index],args.destination,trdict["filename"][index])
            index += 1
            
            


if __name__ == "__main__":
    main()