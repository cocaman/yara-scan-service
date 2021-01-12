#!/usr/bin/env python3
import requests
import argparse
import json
import os
import re
import sys

__author__      = "Arnim Rupp, Corsin Camichel"
__copyright__   = "Copyright 2020, Arnim Rupp, Corsin Camichel"
__license__     = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__     = "1.0"
__email__       = "cocaman@gmail.com"

samplesdir='samples'
bazaar_download='../malware-bazaar/bazaar_download.py'

# Please put your API key in apikey.json if you do not want to use it the CLI (recommended)
API_KEY = ""
try:
    with open('apikey.json') as f:
        array = json.load(f)
        API_KEY = array['apikey']
        #print(f"API key found: {API_KEY}")
except IOError:
    pass


parser = argparse.ArgumentParser(description='Download malware samles found by Yara Scan Service from MalwareBazaar (https://bazaar.abuse.ch/)')
parser.add_argument('-j', '--json', help='JSON file with results from Yara Scan Service (required)', type=str, metavar="FILE", required=True)
parser.add_argument('-a', '--apikey', help='Your personal API key (Storage in apikey.json is recommended)', type=str, metavar="apikey", required=False, default=API_KEY)
parser.set_defaults(feature=True)
args = parser.parse_args()

headers = {'APIKEY': args.apikey}
jsonfile = args.json

print("Doing: ", jsonfile)
with open(jsonfile) as j:
    samples = json.load(j)


try:
    os.mkdir(samplesdir)
except:
    pass

try:
    newdir = jsonfile.replace('.json', '')
    print("newdir: ", newdir)
    if not re.match('[a-fA-F0-9]*$', newdir):
        print('ERROR: wrong directory name: ' , newdir)
        sys.exit()
    os.chdir(samplesdir)
    try:
        os.mkdir(newdir)
    except:
        pass
    os.chdir(newdir)
except Exception as e: 
    print(e)

print('Downloading to ' + os.getcwd() )

for sample in samples:
    url = sample['sha256']

    cmd = bazaar_download + ' -u --hash ' + url
    print(cmd)
    # really unpythonish to call a .py via os.system but it works and bazaar_download.py would need some functions, someday ...
    os.system(cmd)

