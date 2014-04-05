# image handling API
import sqlite3

def initialize():
    load()

def load():
    return

def save():
    return

def add_image(data):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('INSERT INTO image_store (image) VALUES(?)', (data,))
    db.commit()
    db.close()

def get_image(num):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    #c.execute('SELECT i,image FROM image_store WHERE i IS', num)
    i, image = c.fetchone()
    #db.close()
    return image

def get_latest_image():
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('SELECT i,image FROM image_store ORDER BY i DESC LIMIT 1')
    i, image = c.fetchone()
    db.close()
    return image