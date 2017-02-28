#!/usr/bin/python
import json
import os
import random
import socket
import urllib.request

import requests
import time

import sys
from requests import HTTPError

POSSIBLE_ERRORS = (HTTPError,
                   socket.error,
                   requests.exceptions.InvalidSchema,
                   requests.exceptions.ConnectionError)

ROOT_URL = "http://boards.4chan.org"
API_URL = "http://api.4chan.org"
IMAGES_URL = "http://i.4cdn.org"

ROOT_DIR = "YOUR_ROOT_DIR"


USERAGENTS = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"
]


def random_user_agent():
    return random.choice(USERAGENTS)

USER_AGENT = random_user_agent()


def get_content(url):
    try:
        req = requests.get(url, headers={'User-Agent': USER_AGENT}, verify=False, timeout=20)
        if req.status_code == 200:
            return req.content
    except POSSIBLE_ERRORS as error:
        print(url)
        print("This url causes the following error:", error)
        return ""
    except requests.exceptions.Timeout:
        return "timeout"

def get_image_url(thread, filename, extension):
    return IMAGES_URL + "/" + thread + "/" + filename  + extension

def get_thread_url(thread, thread_no):
    return "/".join((API_URL, thread, "thread",  str(thread_no) + ".json"))

# simple directory structure maker from url #
def generatedir(filename, filetype):
    fullpath = ''
    fullpath += filetype + "/"
    d = os.path.dirname(ROOT_DIR + fullpath)
    if not os.path.exists(d):
        os.makedirs(d)
    return fullpath + filename + filetype

def save_file(url, filepath):
    try:
        urllib.request.urlretrieve(url, filepath)
    except Exception as e:
        print(e)

def get_thread_elements(thread):
    current_url = "/".join((API_URL, thread, "catalog.json"))
    content = json.loads(get_content(current_url))
    for pages in content:
        for threads in pages['threads']:
            content = get_content(get_thread_url(thread, threads["no"]))
            if content is not None:
                thread_content = json.loads(content)
                for post in thread_content['posts']:
                    if "tim" in post:
                        image_url = get_image_url(thread, str(post["tim"]), post["ext"])
                        save_file(
                            image_url,
                            ROOT_DIR + generatedir(str(post["tim"]), post["ext"])
                        )
                        print(image_url)
            sys.stdout.write("\n")


get_thread_elements(sys.argv[1])
