import sys
import requests
import time

description = 'A simple wrapper for waifu2x.'
DEMO_API_URL = 'http://waifu2x.udp.jp/api'
NOISE = ('none', 'low', 'high', 'highest')

SRC_MONSTER_IMG_PREFIX = "../monster_images/IMG_"
DST_MONSTER_IMG_HD_PREFIX = "../monster_images_hd/HD_IMG_"

SRC_MONSTER_THMB_PREFIX = "../monster_thumbnails/THMB_"
DST_MONSTER_THMB_HD_PREFIX = "../monster_thumbnails_hd/HD_THMB_"

IMG_TYPE = ".jpg"
THMB_TYPE = ".png"
DST_TYPE = ".png"

def post_image(img, filename='', **kwargs):
    url = DEMO_API_URL
    data = dict(scale='none', noise='highest')
    data.update(kwargs)
    res = requests.post(url, data=data, files={'file': (filename, img, 'image/jpeg', {'Expires': '0'})})
    return res.content

def convert_monster_image_hd(id, scale, noise):
    src_image_name = src_monster_image_name(id)
    dst_image_name = dst_monster_image_hd_name(id)
    with open(src_image_name, "rb") as src_img:
        try:
            res = post_image(src_img, filename=src_image_name, scale=scale, noise=noise)
        except requests.HTTPError:
            print('Something wrong with the Internet, please try again later.')
        else:
            if sys.getsizeof(res) < 256:
                print("Expected file is too small: " + str(sys.getsizeof(res)))
                time.sleep(3)
                convert_monster_image_hd(id, scale, noise)
            else:
                with open(dst_image_name, 'wb') as dst_image:
                    dst_image.write(res)

def convert_monster_thumbnail_hd(id, scale, noise):
    src_thumbnail_name = src_monster_thumbnail_name(id)
    dst_thumbnail_name = dst_monster_thumbnail_hd_name(id)
    with open(src_thumbnail_name, "rb") as src_thmb:
        try:
            res = post_image(src_thmb, filename=src_thumbnail_name, scale=scale, noise=noise)
        except requests.HTTPError:
            print('Something wrong with the Internet, please try again later.')
        else:
            if sys.getsizeof(res) < 256:
                print("Expected file is too small: " + str(sys.getsizeof(res)))
                time.sleep(3)
                convert_monster_thumbnail_hd(id, scale, noise)
            else:
                with open(dst_thumbnail_name, 'wb') as dst_thumbnail:
                    dst_thumbnail.write(res)

def src_monster_image_name(id):
    return SRC_MONSTER_IMG_PREFIX + str(id) + IMG_TYPE

def src_monster_thumbnail_name(id):
    return SRC_MONSTER_THMB_PREFIX + str(id) + THMB_TYPE

def dst_monster_image_hd_name(id):
    return DST_MONSTER_IMG_HD_PREFIX + str(id) + DST_TYPE

def dst_monster_thumbnail_hd_name(id):
    return DST_MONSTER_THMB_HD_PREFIX + str(id) + DST_TYPE

def process_monster(id, scale, noise, should_process_image, should_process_thumbnail):
    if should_process_image:
        try:
            convert_monster_image_hd(id, scale, noise)
            print("Retrieved monster img: " + str(id))
        except Exception as e:
            print("Error: " + str(e))
            print("Could not find monster image " + str(id))

    if should_process_thumbnail:
        try:
            convert_monster_thumbnail_hd(id, scale, noise)
            print("Retrieved monster thmb: " + str(id))
        except Exception as e:
            print("Error: " + str(e))
            print("Could not find monster thumbnail " + str(id))

def main():
    l_bound = int(sys.argv[1])
    u_bound = int(sys.argv[2])
    scale = int(sys.argv[3])
    noise = int(sys.argv[4])
    should_process_image = int(sys.argv[5]) == 1
    should_process_thumbnail = int(sys.argv[6]) == 1

    for i in range(l_bound, u_bound + 1):
        process_monster(i, scale, noise, should_process_image, should_process_thumbnail)
        time.sleep(3)


if __name__ == '__main__':
    main()