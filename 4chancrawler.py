#!/usr/bin/python

import urllib.error
import urllib.request
import os.path
import re
import sys
from PIL import Image
from bs4 import BeautifulSoup

__author__ = "polish"

ROOT_URL = "http://boards.4chan.org"
IMG_URL = "http://i.4cdn.org"
ROOT_DIR = "{CHANGE IT TO YOUR LOCAL DOWNLOAD FOLDER}"

def ensure_dir(f):
    f += "/"
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


# get contents from url #
def get_content(url):
    try:
        return urllib.request.urlopen(url).read()
    except urllib.error.HTTPError as e:
        print("<--404-->", e)
        return False


# save file from url #
def save_file(url, filepath):
    urllib.request.urlretrieve(url, filepath)


# simple directory structure maker from url #
def dirsfromurl(url,size):
    width = size[0]
    height = size[1]
    whdir = str(width)+"x"+str(height)
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    struct = url.split('/')
    filename = struct[-1]
    filetype = filename.split('.')[1]
    if (re.match(r"^[A-Za-z ]*$", filename) == None):
        struct.pop()
    fullpath = ''
    for pathname in struct:
        fullpath += pathname + "/"
    fullpath += filetype + "/"
    fullpath += whdir + "/"
    d = os.path.dirname(ROOT_DIR + fullpath)
    if not os.path.exists(d):
        os.makedirs(d)
    return fullpath + filename


def getsizes(uri):
    # get file size *and* image size (None if not known)
    file = urllib.request.urlopen(uri)
    try:
        im = Image.open(file)
        resolution = im.size
    except:
        resolution = (0,0)
    return resolution



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
        soupContent = BeautifulSoup(get_content(current_url), 'html.parser')
        links = soupContent.findAll('a', {"class": "replylink"})
        for a in links:
            thread_url = root_url + a['href']
            cont = get_content(thread_url)
            if cont != False:
                threadContent = BeautifulSoup(cont, 'html.parser')
                images = threadContent.findAll('a', {"class": "fileThumb"})
                # print thread_url
                for img in images:
                    images_url = "/".join((IMG_URL, thread))
                    image_source = "http:" + img['href']
                    size = getsizes(image_source)
                    img_path = ROOT_DIR + dirsfromurl(image_source, size)
                    save_file(image_source, img_path)
                    print("Image: " + image_source + " saved: " + img_path+" | size: "+ str(size))
        i += 1


ready(sys.argv[1], 10)
