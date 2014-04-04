# image handling API
import cPickle
import os

IMAGE_DB_FILE = 'images.db'

images = {}

def initialize():
    load()

def load():
    global images
    if os.path.exists(IMAGE_DB_FILE):
        fp = open(IMAGE_DB_FILE, 'rb')
        images = cPickle.load(fp)
        fp.close()

        print 'Loaded: %d images' % (len(images))

def save():
    fp = open(IMAGE_DB_FILE, 'wb')
    cPickle.dump(images, fp)
    fp.close()

def add_image(data):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
        
    images[image_num] = data

    save()
    
    return image_num

def get_image(num):
    return images[num]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]
