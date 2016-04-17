#!/usr/bin/env python3

import sys
import os

from urllib import request
from PIL import Image

MONSTER_IMAGE_URL = "http://puzzledragonx.com/en/img/monster/MONS_"
MONSTER_THUMBNAIL_URL = "http://puzzledragonx.com/en/img/book/"

MONSTER_IMAGE_PREFIX = "IMG_"
MONSTER_THUMBNAIL_PREFIX = "THMB_"
IMAGE_TYPE = ".jpg"
THUMBNAIL_TYPE = ".png"

MONSTER_IMAGE_DIR = "../monster_images/"
MONSTER_THUMBNAIL_DIR = "../monster_thumbnails/"

def retrieve_monster_image(id):
    image_url = monster_image_url(id) 
    image_name = monster_image_name(id)

    request.urlretrieve(image_url, MONSTER_IMAGE_DIR + image_name)

def retrieve_monster_thumbnail(id):
    thumbnail_url = monster_thumbnail_url(id)
    thumbnail_name = monster_thumbnail_name(id)

    request.urlretrieve(thumbnail_url, MONSTER_THUMBNAIL_DIR + thumbnail_name)

def monster_image_url(id):
    return MONSTER_IMAGE_URL + str(id) + IMAGE_TYPE

def monster_thumbnail_url(id):
    return MONSTER_THUMBNAIL_URL + str(id) + THUMBNAIL_TYPE

def monster_image_name(id):
    return MONSTER_IMAGE_PREFIX + str(id) + IMAGE_TYPE

def monster_thumbnail_name(id):
    return MONSTER_THUMBNAIL_PREFIX + str(id) + THUMBNAIL_TYPE

def crop_monster_image(img_path):
    src_img = Image.open(img_path)
    dst_img = src_img.crop((0, 13, src_img.size[0], src_img.size[1]))
    dst_img.save(img_path, quality=100)

def process_monster(id):
    save_dir = MONSTER_IMAGE_DIR + monster_image_name(id)

    if not os.path.isfile(MONSTER_IMAGE_DIR + monster_image_name(id)):
        try:
            retrieve_monster_image(id)
            crop_monster_image(save_dir)
        except:
            print("Could not retrieve image for monster " + str(id))
    else:
        print("Monster IMG " + str(id) + " already exists")

    if not os.path.isfile(MONSTER_THUMBNAIL_DIR + monster_thumbnail_name(id)):
        try:
            retrieve_monster_thumbnail(id)
        except:
            print("Could not retrieve thumbnail for monster " + str(id))
    else:
        print("Monster THMB " + str(id) + " already exists")

def main():
    l_bound = int(sys.argv[1])
    u_bound = int(sys.argv[2])

    for i in range(l_bound, u_bound + 1):
        process_monster(i)

if __name__ == "__main__":
    main()