import csv
import urllib.request as request
import requests
import os.path
import os
import errno
from PIL import Image

# Utility function to make directory
def mkdir(path):
    print('Creating directory: ' + path)
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    print('Done!')

# Returns a list of the files in a path
def listfiles(path):
    return [
        f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
    ]


if __name__ == "__main__":
    PATH = './bin/validate/uncompressed/all'
    OUT_PATH = './test_data/all/'
    images = listfiles(PATH)
    mkdir(OUT_PATH)
    for image in images:
        im = Image.open(os.path.join(PATH, image))
        im.save(os.path.join(OUT_PATH, image), quality=50, format='jpeg')
