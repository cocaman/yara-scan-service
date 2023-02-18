#!/usr/bin/env python3
import requests
import argparse
import json
import re
import os
import sys
import time

__author__      = "Corsin Camichel"
__copyright__   = "Copyright 2020, Corsin Camichel"
__license__     = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__     = "1.0"
__email__       = "cocaman@gmail.com"

logfile = 'yara_scan_upload.log'

# Please put your API key in apikey.json if you do not want to use it in the CLI (recommended)
API_KEY = ""
try:
    with open('apikey.json') as f:
        array = json.load(f)
        API_KEY = array['apikey']
        #print(f"API key found: {API_KEY}")
except IOError:
    pass

try:
    logf = open(logfile, 'a')
except:
    print(f'Can not open logfile for apending: {logfile}' )
    sys.exit()

def log(text):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    logf.write(f'{now} {text}\n')
    #print(text)

parser = argparse.ArgumentParser(description='Upload a Yara rule to be scanned on Yara Scan Service')
parser.add_argument('-f', '--file', help='Yara rule to upload (required)', type=str, metavar="YARA-FILE", required=True, nargs=argparse.ONE_OR_MORE)
parser.add_argument('-a', '--apikey', help='Your personal API key (Storage in apikey.json is recommended)', type=str, metavar="apikey", required=False, default=API_KEY)
parser.add_argument('-d', '--daily', help='Run this rule now and every daily', dest="daily", required=False, default=False, action='store_true')
parser.add_argument('-w', '--weekly', help='Run this rule now and once per week (Sunday)', dest="weekly", required=False, default=False, action='store_true')
parser.set_defaults(feature=True)
args = parser.parse_args()

headers = {'APIKEY': args.apikey}
data = {}

files = []
# append filenames of yara rules as identifier to URL to tell them apart
identifier = ''
print(args.file)

for f in args.file:
    files.append(('file[]', open(f,'rb')))
    fname = os.path.basename(f)
    identifier += fname + '__'

file_list = identifier[:-2]
identifier = re.sub(r'\W', '_', file_list)

if(args.daily):
    data = {"daily" : "true"}
if(args.weekly):
    data = {"weekly" : "true"}

response = requests.post('https://riskmitigation.ch/yara-scan/api/', files=files, headers=headers, data=data)
json_data = json.loads(response.text)
status = json_data['status']

print(f"Yara Scan status: {status}")
if(status == "ok"):
    print(f"The scan is running, you will receive an email with the results or you can download the results file from here: https://riskmitigation.ch/yara-scan/results/{json_data['id']}/#{identifier}")
    log(f"https://riskmitigation.ch/yara-scan/results/{json_data['id']}/#{identifier} {file_list}")
    print(f'logged to {logfile}')
