from os import listdir
from os.path import isfile, join
from PIL import Image, ImageFilter

SIZE = (256, 256)
PATH = 'src/'
OUT_TRAIN = 'bin/train/'
OUT_VALIDATE = 'bin/validate/'

# Only populates the list with paths to jpeg files
files = [join(PATH, f) for f in listdir(PATH) \
    if isfile(join(PATH, f)) and join(PATH, f).endswith('.jpg')]

print('Files to be built: ')
print(files)

def build():
  # Iterates through the files, and keep tracks of the files with an integer.
  index = 0
  for file in files:
    index += 1

    # Opens and resizes the current image. LANCZOS is apparently the prettiest but slowest
    im = Image.open(file)
    im = im.resize(SIZE, resample=Image.LANCZOS)

    # Makes every 5 images a part of the validation set (20%)
    outpath = OUT_VALIDATE if index % 5 == 0 else OUT_TRAIN
    # Save a uncompressed and compressed copy
    im.save(outpath + 'uncompressed/all/{}.jpg'.format(index), format="jpeg", quality=100)
    im.save(outpath + 'compressed/all/{}.jpg'.format(index), format="jpeg", quality=10)

    im.close()

build()
