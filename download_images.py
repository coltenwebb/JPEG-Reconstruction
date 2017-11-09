import csv
import urllib.request as request
import os.path

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

if __name__ == "__main__":
    NUMBER_TO_DOWNLOAD = 110

    print('Creating URL List')
    images = generate_url_list(NUMBER_TO_DOWNLOAD)
    print('Done!')

    i = 0
    for image in images:
        i += 1
        filepath = 'src/{}.jpg'.format(image[0])
        print('Downloading Image: {0} of {1}'.format(i, NUMBER_TO_DOWNLOAD), end='\r')
        if (not os.path.isfile(filepath)):
            request.urlretrieve(image[1], filepath)
    print('\nDone!')
