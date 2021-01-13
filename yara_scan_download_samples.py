#!/usr/bin/env python3
import requests
import argparse
import json
import os
import re
import pyzipper
import sys

__author__      = "Arnim Rupp, Corsin Camichel"
__copyright__   = "Copyright 2021, Arnim Rupp, Corsin Camichel"
__license__     = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__     = "1.0"
__email__       = "cocaman@gmail.com"

def download_sample(sha256_hash):
    data = { 'query': 'get_file', 'sha256_hash': sha256_hash }
    response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=15, allow_redirects=True)
    open(sha256_hash+'.zip', 'wb').write(response.content)
    with pyzipper.AESZipFile(sha256_hash+".zip") as zf:
        zf.pwd = b'infected'
        my_secrets = zf.extractall(".")
    os.remove(sha256_hash+'.zip')

parser = argparse.ArgumentParser(description='Download malware samles found by Yara Scan Service from MalwareBazaar (https://bazaar.abuse.ch/)')
parser.add_argument('-j', '--json', help='JSON file with results from Yara Scan Service (required)', type=str, metavar="FILE", required=True)
parser.add_argument('-p', '--path', help='Path to store the samples in (default ./samples/)', type=str, metavar="FILE", required=False, default="samples/")
parser.set_defaults(feature=True)
args = parser.parse_args()

with open(args.json) as j:
    samples = json.load(j)

try:
    os.mkdir(args.path)
except:
    pass

try:
    sample_dir = os.path.splitext(os.path.basename(args.json))[0]
    if not re.match('[a-fA-F0-9]*$', sample_dir):
        print('ERROR: wrong directory name: ' , sample_dir)
        sys.exit()
    os.chdir(args.path)
    try:
        os.mkdir(sample_dir)
    except:
        pass
    os.chdir(sample_dir)
except Exception as e:
    print(e)

print('Downloading to ' + os.getcwd() )
for sample in samples:
    hash = sample['sha256']
    download_sample(hash)
