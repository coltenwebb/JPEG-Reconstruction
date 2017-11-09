import tensorflow as tf
import os

from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Input, Dense, Reshape, Flatten
from keras.models import Model, Sequential

import matplotlib.pyplot as plt

# Size of the image data
SIZE = (256, 256)

train_datagen = ImageDataGenerator(rescale=1./255)

# Args for the training data generator. Both x and y should be identical,
# so they are put into a tuple
train_generator_args = dict(target_size=SIZE,
        batch_size=32,
        class_mode=None,
        color_mode='grayscale',
        seed=1)

train_generator_x = train_datagen.flow_from_directory(
        'bin/train/compressed/', **train_generator_args)

train_generator_y = train_datagen.flow_from_directory(
        'bin/train/uncompressed/', **train_generator_args)

train_generator = zip(train_generator_x, train_generator_y)

# Validation data generator
validation_generator_x = train_datagen.flow_from_directory(
        'bin/validate/compressed/',
        target_size=SIZE,
        batch_size=32,
        class_mode=None,
        color_mode='grayscale',
        seed=1)

validation_generator_y = train_datagen.flow_from_directory(
        'bin/validate/uncompressed/',
        target_size=SIZE,
        batch_size=32,
        class_mode=None,
        color_mode='grayscale',
        seed=1)



model = Sequential()

model.add(Flatten(input_shape=(256,256,1)))
model.add(Dense(32, input_shape=(65536,), activation='relu'))
model.add(Dense(65536, input_shape=(32,), activation='sigmoid'))
model.add(Reshape((256,256,1), input_shape=(65536,)))
# model.output_shape => (None, 256, 256, 1)

model.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])

# thing = train_generator_y.next()
# thing[0].shape

# Utility function that displays the image from a tensor shape (256,256,1)
def reconstruct(tensor):
    plt.figure(figsize=(10, 10))

    ax = plt.subplot(2, 1, 1)
    plt.imshow(tensor.reshape(256, 256))
    plt.gray()
    ax.get_xaxis().set_visible(True)
    ax.get_yaxis().set_visible(True)

    plt.show()

model.fit_generator(
        train_generator,
        steps_per_epoch=2000,
        epochs=1)

thing = train_generator_x.next()
reconstruct(thing[0])

prediction = model.predict(thing)

reconstruct(prediction[3])
