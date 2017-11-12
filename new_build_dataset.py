import csv
import urllib.request as request
import requests
import os.path
import os
import errno
from PIL import Image

NUMBER_TO_DOWNLOAD = 20000

def generate_url_list(linestoread):
    ret = []
    with open('images.csv', newline='', encoding='utf8') as csvfile:
        imagereader = csv.DictReader(csvfile)
        for row in imagereader:
            ret.append((row['ImageID'], row['OriginalURL']))
            linestoread -= 1
            if (linestoread <= 0):
                break
    return ret


# Utility function to make directory
def mkdir(path):
    print('Creating directory: ' + path)
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    print('Done!')


def image_from_url(url):
    r = requests.get(url, stream=True)
    r.raw.decode_content = True  # Content-Encoding
    im = Image.open(r.raw)
    return im


if __name__ == "__main__":

    mkdir('bin/train/compressed/all')
    mkdir('bin/train/uncompressed/all')
    mkdir('bin/validate/compressed/all')
    mkdir('bin/validate/uncompressed/all')

    # images is a list of tuples (imageid, url)
    print('Creating URL List')
    images = generate_url_list(NUMBER_TO_DOWNLOAD)
    print('Done!')

    i = 0
    for image in images:
        url = image[1]
        img_name = image[0]

        i += 1
        print(
            'Downloading Image: {0} of {1}'.format(i, NUMBER_TO_DOWNLOAD),
            end='\r')
        type = 'validate' if i % 5 == 0 else 'train'
        filepath = 'bin/' + type + '/{}/all/' + img_name + '.jpg'

        if os.path.isfile(filepath.format('compressed')) and os.path.isfile(filepath.format('uncompressed')):
            continue

        im = image_from_url(url)
        im = im.resize((96, 96), resample=Image.LANCZOS)

        im.save(filepath.format('uncompressed'), format="jpeg", quality=100)
        im.save(filepath.format('compressed'), format="jpeg", quality=20)
    print('\nDone!')
