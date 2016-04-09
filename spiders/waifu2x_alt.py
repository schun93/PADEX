#!/usr/bin/env python3

import sys
import requests
import bs4
import time

from bs4 import BeautifulSoup
from urllib import request


description = 'A simple wrapper for waifu2x.'
DEMO_API_URL = 'http://waifu2x.booru.pics'
UPLOAD_API_ENDPOINT = '/Home/upload'

SRC_MONSTER_IMG_PREFIX = "../monster_images/IMG_"
DST_MONSTER_IMG_HD_PREFIX = "../monster_images_hd/HD_IMG_"

SRC_MONSTER_THMB_PREFIX = "../monster_thumbnails/THMB_"
DST_MONSTER_THMB_HD_PREFIX = "../monster_thumbnails_hd/HD_THMB_"

IMG_TYPE = ".jpg"
THMB_TYPE = ".png"
DST_TYPE = ".png"

def post_image(img, filename='', **kwargs):
    url = DEMO_API_URL + UPLOAD_API_ENDPOINT
    data = dict(scale=2, denoise=2)
    data.update(kwargs)
    
    while True:
        try:
            res = requests.post(url, data=data, files={'img': (filename, img, 'image/jpeg')})
            soup = BeautifulSoup(res.content, "lxml")
            image_url = DEMO_API_URL + soup.find("div", {"id" : "img"}).find("a", text="PNG")["href"]
        except Exception as e:
            retry_url = res.url
            print("Failed for image: " + filename + "\nException: " + str(e) + ".\nAttempting to recover at url: " + retry_url + " " + str("upload" not in retry_url))
            if "upload" not in retry_url:
                for i in range(0, 10):
                    print("Attempt: #" + str(i))
                    time.sleep(3)
                    res = requests.get(retry_url)
                    soup = BeautifulSoup(res.content, "lxml")
                    
                    try:
                        image_url = DEMO_API_URL + soup.find("div", {"id" : "img"}).find("a", text="PNG")["href"]

                        print("Recovered: " + filename + "\n")

                        return image_url
                    except:
                        image_url = None
            else:
                print("Failed because redirection to home page. " + str(res) + "\n")
                data.update(kwargs)
                time.sleep(10)
                continue
        else:
            if image_url != None:
                print("Retrieved: " + filename + "\n")
                break

    return image_url

def convert_monster_image_hd(id, scale, denoise):
    src_image_name = src_monster_image_name(id)
    dst_image_name = dst_monster_image_hd_name(id)
    with open(src_image_name, "rb") as src_img:
        try:
            image_url = post_image(src_img, filename=src_image_name, scale=scale, denoise=denoise)
            request.urlretrieve(image_url, dst_monster_image_hd_name(id))
        except requests.HTTPError:
            print('Something wrong with the Internet, please try again later.')

def convert_monster_thumbnail_hd(id, scale, denoise):
    src_thumbnail_name = src_monster_thumbnail_name(id)
    dst_thumbnail_name = dst_monster_thumbnail_hd_name(id)
    with open(src_thumbnail_name, "rb") as src_thmb:
        try:
            image_url = post_image(src_thmb, filename=src_thumbnail_name, scale=scale, denoise=denoise)
            request.urlretrieve(image_url, dst_monster_thumbnail_hd_name(id))
        except requests.HTTPError:
            print('Something wrong with the Internet, please try again later.')

def src_monster_image_name(id):
    return SRC_MONSTER_IMG_PREFIX + str(id) + IMG_TYPE

def src_monster_thumbnail_name(id):
    return SRC_MONSTER_THMB_PREFIX + str(id) + THMB_TYPE

def dst_monster_image_hd_name(id):
    return DST_MONSTER_IMG_HD_PREFIX + str(id) + DST_TYPE

def dst_monster_thumbnail_hd_name(id):
    return DST_MONSTER_THMB_HD_PREFIX + str(id) + DST_TYPE

def process_monster(id, scale, denoise, should_process_image, should_process_thumbnail):
    if should_process_image == 1:
        try:
            convert_monster_image_hd(id, scale, denoise)
        except Exception as e:
            print("Could not find monster image " + str(id) + " " + str(e))
            print("Error: " + str(e) + "\n")

    if should_process_thumbnail == 1:
        try:
            convert_monster_thumbnail_hd(id, scale, denoise)
        except Exception as e:
            print("Could not find monster thumbnail " + str(id))
            print("Error: " + str(e) + "\n")


def main():
    l_bound = int(sys.argv[1])
    u_bound = int(sys.argv[2])
    scale = int(sys.argv[3])
    denoise = int(sys.argv[4])
    should_process_image = int(sys.argv[5])
    should_process_thumbnail = int(sys.argv[6])

    for i in range(l_bound, u_bound + 1):
        process_monster(i, scale, denoise, should_process_image, should_process_thumbnail)


if __name__ == '__main__':
    main()