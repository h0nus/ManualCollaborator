import requests
import base64
import argparse
import os
import subprocess
import json
import random
import time
import datetime

#User your own (Burp->Burp Collaborator Client-> set a number you'd like and generate themall!)
collabs = ["o8xye122t5lwdvd63z8i4ze1asgi47.burpcollaborator.net",
           "h1jr7uvvmyep6o6zws1bxs7u3l9cx1.burpcollaborator.net",
           "ibxshv5wwzoqgpg06tbc7thvdmje73.burpcollaborator.net",
           "7rzhxkllco4fwewpmir1nixktbz4nt.burpcollaborator.net",
           "wvv619pagd84030eq7vqr719x03urj.burpcollaborator.net",
           "1kmbqeef5ix9p8pjfckvgcqem5s0gp.burpcollaborator.net",
           "woo6u9ia9d14t3tej7oqk7u9q0wwkl.burpcollaborator.net",
           "j1lt7wvxm0er6q61wu1dxu7w3n9kx9.burpcollaborator.net",
           "446eahyiplhc9b9mzf4y0fah68c60v.burpcollaborator.net",
           "zqt9wckdbg37v6vhlaqtmawcs3y2mr.burpcollaborator.net"]

#parses Json response
def loadJson(data):
    datas = json.loads(data)
    if len(datas) == 0:
        print("[!] No interactions found, please retry")
        return
    else:
        responses = datas["responses"]
        for i in range(len(responses)):
            dats = responses[i]["data"]
            print("Interaction n. {}:\n\tProtocol: {}\n\tTime: {}\n\tClient: {}".format(
                i, responses[i]["protocol"], convert_java_millis(responses[i]["time"]), responses[i]["client"]))
            if responses[i]["protocol"] == 'http':
                print("\tRequest: {}".format(dats["request"]))
            elif responses[i]["protocol"] == 'https':
                print("\tRequest: {}".format(dats["request"]))
            elif responses[i]["protocol"] == 'dns':
                print("\tRawRequest: {}".format(dats["rawRequest"]))

#convert java timestamp to python's one
def convert_java_millis(java_time_millis):
    """Provided a java timestamp convert it into python date time object"""
    ds = datetime.datetime.fromtimestamp(
        int(str(java_time_millis)[:10])) if java_time_millis else None
    ds = ds.replace(hour=ds.hour, minute=ds.minute, second=ds.second,
                    microsecond=int(str(java_time_millis)[10:]) * 1000)
    return ds.strftime("%Y-%m-%d %H:%M:%S")

#get the data with the used secret, rememeber to use your own secret if you chnage the collabs at line 12
#how to get your own secret: https://0x00sec.org/t/achieving-persistent-access-to-burp-collaborator-sessions/14311
def getData(secret):
    print("[*] Getting interactions")
    polling_uri = "http://polling.burpcollaborator.net/burpresults?biid={}".format(
        secret)
    session = requests.Session()
    headers = {'User-Agent': 'OhMyAgent'}
    response = session.get(polling_uri, headers=headers)
    return response.text

#main
def main():
    parser = argparse.ArgumentParser(
        description='Manual collaborator by h0nus7')
    parser.add_argument('--secret', dest="secret", action='store', type=str,
                        default="g9%2bFQ4%2bNK86RSeFSjL%2bA%2fmv0buhnryThQDAekWacmRE%3d", help='Secret key used for polling')
    parser.add_argument('--bid', dest="bid", action='store', type=str,
                        default=random.choice(collabs), help='set custom Burp Collaborator ID')
    args = parser.parse_args()
    print("[+] Manual Collaborator by h0nus7\n[!] Please run the tool only after you sent your tests as after first poll results will be deleted")
    data = getData(args.secret)
    loadJson(data)


if __name__ == '__main__':
    main()
