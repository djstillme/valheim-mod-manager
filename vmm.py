#!/usr/bin/env python3

import requests
import time
import warnings
import csv
import os
import shutil
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
from configparser import ConfigParser
from googlesearch import search

file = 'config.ini'
config = ConfigParser()
config.read(file)
warnings.simplefilter("ignore")
chunk_size = 1024
modsdir = str(config['PARAMETERS']['mods_dir'])
modscsv = str(config['PARAMETERS']['mods_csv'])
depcsv = str(config['PARAMETERS']['dependencies_csv'])
mod_dependencies = []

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

    dependencies = []
    h5 = soup.find_all('h5')
    for index, tag in enumerate(h5):
        if index > 0:
            dependencies.append(tag.get_text(strip=True))

    for item in dependencies:
        if item not in mod_dependencies:
            mod_dependencies.append(item)
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


def emptyfolder(modsdir) -> None:
    """
    Emptys folder on first iteration
    """
    dirs = os.listdir(modsdir)
    for doc in dirs:
        actualdir = modsdir + '/' + doc
        print(modsdir + '/' + doc)
        if doc.endswith('.dll'):
            pass
        elif os.path.isfile(actualdir):
            os.remove(actualdir)
        elif os.path.isdir(actualdir):
            shutil.rmtree(actualdir)

def emptyfolder2(modsdir) -> None:
    """
    Removes leftover zip files
    """
    dirs = os.listdir(modsdir)
    for doc in dirs:
        actualdir = modsdir + '/' + doc
        if doc.endswith('.zip'):
            os.remove(actualdir)

def handle_dependencies() -> None:
    """
    Creates the list of dependencies in dependencies.csv
    """
    mod_dep_urls = []

    for i in mod_dependencies:
        for url in search(i, tld="co.in", num=1, stop=1):
            getversions(url)

    mod_dependencies.remove('denikson-BepInExPack_Valheim')

    for mod in mod_dependencies:
        for url in search(mod, tld="co.in", num=1, stop=1):
            mod_dep_urls.append(url)

    with open('dependencies.csv', 'w') as file:
        file.truncate(0)

    with open('dependencies.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for link in mod_dep_urls:
            writer.writerow([link])

def main():

    print(f"{GREEN}CLEARING MODS FOLDER...{RESET}")
    emptyfolder(modsdir)
    urls = read_csv(modscsv)

    print(f"{GREEN}DOWNLOADING PRIMARY MODS (this may take some time...){RESET}")

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

        newpath = os.path.join(modsdir, mod)
        os.makedirs(newpath)
        shutil.unpack_archive(fileloc, modsdir + '/' + mod)

    handle_dependencies()

    print(f"{GREEN}GATHERING MOD DEPENDENCIES){RESET}")

    with open('get_dependencies.py') as file:
        code = file.read()
        exec(code)

    print(f"{GREEN}CLEANING UP...{RESET}")
    emptyfolder2(modsdir)

    print(f"{GREEN}MODS SUCCESFULLY INSTALLED!{RESET}")

if __name__ == "__main__":
    main()
