#!/usr/bin/python

import urllib.error
import urllib.request
import os.path
import random
import re
import sys
from bs4 import BeautifulSoup

__author__ = "polish"

ROOT_URL = "http://boards.4chan.org"
IMG_URL = "http://i.4cdn.org"
ROOT_DIR = "{REPLACE TO YOUR PATH}"
USERAGENTS = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"
]

def ensure_dir(f):
    f += "/"
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


# get contents from url #
def randomUserAgent():
    return random.choice(USERAGENTS)

USERAGENT = randomUserAgent()


def get_content(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USERAGENT})
        content = urllib.request.urlopen(req).read()
        return content
    except urllib.error.HTTPError as e:
        print("<--404-->", e)
        return False


# save file from url #
def save_file(url, filepath):
    try:
        urllib.request.urlretrieve(url, filepath)
    except Exception as e:
        print(e)


# simple directory structure maker from url #
def dirsfromurl(url):
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    struct = url.split('/')
    filename = struct[-1]
    filetype = filename.split('.')[1]
    subdir = filename.split('.')[0][0:5]

    if (re.match(r"^[A-Za-z ]*$", filename) == None):
        struct.pop()
    fullpath = ''
    for pathname in struct:
        fullpath += pathname + "/"
    fullpath += filetype + "/"
    fullpath += subdir + "/"
    d = os.path.dirname(ROOT_DIR + fullpath)
    if not os.path.exists(d):
        os.makedirs(d)
    return fullpath + filename


def ready(thread, numofpages):
    ensure_dir(ROOT_DIR)
    ensure_dir(ROOT_DIR + 'i.4cdn.org')
    ensure_dir(ROOT_DIR + 'i.4cdn.org/' + thread + '/')

    i = 1
    while i <= numofpages:
        str_i = str(i) if i > 1 else ""
        current_url = "/".join((ROOT_URL, thread, str_i))
        root_url = "/".join((ROOT_URL, thread, ""))
        # print(current_url)
        content = get_content(current_url)
        soupContent = BeautifulSoup(content, 'html.parser')
        links = soupContent.findAll('a', {"class": "replylink"})
        links = list(set(links))
        for a in links:
            thread_url = root_url + a['href']
            cont = get_content(thread_url)
            if cont != False:
                threadContent = BeautifulSoup(cont, 'html.parser')
                images = threadContent.findAll('a', {"class": "fileThumb"})
                # print thread_url
                images = list(set(images))
                for img in images:
                    image_source = "http:" + img['href']
                    img_path = ROOT_DIR + dirsfromurl(image_source)
                    save_file(image_source, img_path)
                    print("Image: " + image_source + " saved: " + img_path)
        i += 1


ready(sys.argv[1], 10)
