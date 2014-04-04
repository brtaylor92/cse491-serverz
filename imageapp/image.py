# image handling API
import cPickle
import sqlite3
import os

IMAGE_DB_FILE = 'images.db'

images = {}

def initialize():
    load()

def load():
    return

def save():
    fp = open(IMAGE_DB_FILE, 'wb')
    cPickle.dump(images, fp)
    fp.close()

def add_image(data):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    db.execute('INSERT INTO image_store (image) VALUES(?)', (data,))
    db.commit()

def get_image(num):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('SELECT i,image FROM image_store WHERE i IS', num)
    i, image = c.fetchone()
    return image

def get_latest_image():
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('SELECT i,image FROM image_store ORDER BY i DESC LIMIT 1')
    i, image = c.fetchone()
    return image