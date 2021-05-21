#!/usr/bin/env python3
import requests
from requests.packages.urllib3.util.retry import Retry
import argparse
import json
import os
import re
import pyzipper
import sys
import glob
import time

Retry(total=5)

__author__      = "Arnim Rupp, Corsin Camichel"
__copyright__   = "Copyright 2021, Arnim Rupp, Corsin Camichel"
__license__     = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__     = "1.0"
__email__       = "cocaman@gmail.com"

def download_sample(sha256_hash, malware):
    data = { 'query': 'get_file', 'sha256_hash': sha256_hash }
    
    if glob.glob(f"{sha256_hash}*"):
        print(f"File already there: {sha256_hash}")
        return 

    filename = sha256_hash+'.zip'

    got_it = False
    
    for x in range(5):
        try:
            response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=15, allow_redirects=True)
            got_it = True
            break
        except Exception as error:
            wait = 3 ** x 
            print(f"Exception occured during download {filename}, waiting for {wait} seconds before retry. Error: {error}")
            time.sleep( wait )


    open(filename, 'wb').write(response.content)

    try:
        with pyzipper.AESZipFile(filename) as zf:
            zf.pwd = b'infected'
            my_secrets = zf.extractall(".")
            files = zf.namelist()
            for f in files:
                os.rename(f, f"{f}_{malware}")
        os.remove(sha256_hash+'.zip')
    except Exception as error:
        print(f"Exception occured on file {filename} : {error}")

def check_string_in_list(string, listi):
    for l in listi:
        if l in string:
            return True
    return False

parser = argparse.ArgumentParser(description='Download malware samles found by Yara Scan Service from MalwareBazaar (https://bazaar.abuse.ch/)')
parser.add_argument('-j', '--json', help='JSON file with results from Yara Scan Service (required)', metavar="FILE", required=True, nargs=argparse.ONE_OR_MORE, action='append')
parser.add_argument('-p', '--path', help='Path to store the samples in (default ./samples/)', type=str, metavar="FILE", required=False, default="samples/")
parser.add_argument('-e', '--exclude', help='Exclude malware which matches this string (case ignore)', required=False, nargs=argparse.ONE_OR_MORE, action='append')
parser.add_argument('-i', '--include', help='Include only malware which matches this string (case ignore)', required=False, nargs=argparse.ONE_OR_MORE, action='append')
parser.add_argument('-m', '--malware_name', help='Do not append name of malware to stored samples filename', type=str, required=False, default='')
parser.add_argument('-n', help='Do not download anything, just show what would be done', action='store_true', required=False, default=False)
parser.set_defaults(feature=True)
args = parser.parse_args()


exclude = []
include = []

if args.exclude:
    for e in args.exclude:
        exclude.append(e[0].lower() )

if args.include:
    for i in args.include:
        include.append(i[0].lower() )

dont = args.n
malware_name = args.malware_name


print(args.include)
print( args.json)

root =  os.getcwd()
for jsonlist in args.json:
    jsonfile = jsonlist[0]
    print(f"Doing jsonfile: {jsonfile}")
    os.chdir(root)
    with open(jsonfile) as j:
        samples = json.load(j)

    if not dont:
        try:
            os.mkdir(args.path)
        except:
            pass

        try:
            sample_dir = os.path.splitext(os.path.basename(jsonfile))[0]
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
            print("Error: ", e)

        print('Downloading to ' + os.getcwd() )

    for sample in samples:
        hhash = sample['sha256']
        malware_up = sample['malware']
        malware = malware_up.lower()

        download_this = True

        if include:
            download_this = False

        if include and check_string_in_list(malware, include):
            download_this = True
            
        if exclude and check_string_in_list(malware, exclude):
            download_this = False

        if download_this:
            print(f"{sample['sha256']} {sample['rule']} {sample['malware']}") 
            if not dont:
                download_sample(hhash, malware_up)
