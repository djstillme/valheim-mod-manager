#!/usr/bin/env python3

import requests
import time
import warnings
import csv
import os
import shutil
from bs4 import BeautifulSoup
from tqdm import tqdm
from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser()
config.read(file)
warnings.simplefilter("ignore")

chunk_size = 1024
modsdir = str(config['PARAMETERS']['mods_dir'])
modscsv = str(config['PARAMETERS']['mods_csv'])
depcsv = str(config['PARAMETERS']['dependencies_csv'])

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"  # Reset to default color

def getversions(url) -> str:
    """
    Finds specific version of mod to be downloaded, and dependencies
    """
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    links = []

    for link in soup.find_all('a'):
        if type(link.get('href')) == str:
            if 'https://thunderstore.io/package/download/' in link.get('href'):
                links.append(link.get('href'))
    return links[0]

def truncate(url, iterations):
    """
    Truncates and formats mod name to be legible in the progress bar
    """
    if iterations == 3:
        return url
    else:
        newurl = url[0:url.rfind('/')]
        return truncate(newurl, iterations+1)

def read_csv(file_path) -> list:
    """
    Scans requested mods and formats them and stores into a list
    """
    data_list = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            cleaned_row = [element.strip() for element in row if element.strip()]
            data_list.extend(cleaned_row)
    return data_list

def main():
    urls = read_csv(depcsv)

    print(f"{GREEN}DOWNLOADING MOD DEPENDENCIES...{RESET}")

    for i in range(len(urls)):
        modversion = getversions(urls[i])
        req = requests.get(modversion, stream=True)
        filename = req.url[modversion.rfind('/'):]
        index_one = truncate(modversion, 0)
        mod = modversion[len(index_one)+1:-1]
        filesize = int(req.headers['content-length'])
        fileloc = modsdir + '/' + filename

        with open(fileloc, 'wb') as f:
            for chunk in tqdm(
                iterable=req.iter_content(chunk_size=chunk_size),
                total=filesize/chunk_size,
                unit='MB',
                ascii='-#',
                desc=mod
            ):
                if chunk:
                    f.write(chunk)

        newpath = os.path.join(modsdir, os.path.splitext(filename)[0])
        os.makedirs(newpath)
        shutil.unpack_archive(fileloc, modsdir + '/' + os.path.splitext(filename)[0])

if __name__ == "__main__":
    main()
