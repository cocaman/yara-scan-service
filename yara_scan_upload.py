#!/usr/bin/env python3
import requests
import argparse
import json

__author__      = "Corsin Camichel"
__copyright__   = "Copyright 2020, Corsin Camichel"
__license__     = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__     = "1.0"
__email__       = "cocaman@gmail.com"

# Set your API key here if you do not want to use it the CLI (recommended)
API_KEY = ""

parser = argparse.ArgumentParser(description='Upload a Yara rule to be scanned on Yara Scan Service')
parser.add_argument('-f', '--file', help='Yara to upload (required)', type=str, metavar="FILE", required=True, nargs=argparse.ONE_OR_MORE)
parser.add_argument('-a', '--apikey', help='Your personal API key', type=str, metavar="apikey", required=False, default=API_KEY)
args = parser.parse_args()

headers = {'APIKEY': args.apikey}
files = []
for f in args.file:
    files.append(('file[]', open(f,'rb')))

response = requests.post('https://riskmitigation.ch/yara-scan/api/', files=files, headers=headers)
json_data = json.loads(response.text)
status = json_data['status']

print(f"Yara Scan status: {status}")
if(status == "ok"):
    print(f"The scan is running, you will receive an email with the results or you can download the results file from here: https://riskmitigation.ch/yara-scan/results/{json_data['id']}/")
