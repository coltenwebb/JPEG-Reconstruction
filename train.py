import os

from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

import model as model

train_datagen = ImageDataGenerator(rescale=1./255)

# Args for the training data generator. Both x and y should be identical,
# so they are put into a tuple
generator_args = dict(target_size=(256,256),
        batch_size=32,
        class_mode=None,
        color_mode='grayscale',
        seed=1)

train_generator_x = train_datagen.flow_from_directory(
        'bin/train/compressed/', **generator_args)

train_generator_y = train_datagen.flow_from_directory(
        'bin/train/uncompressed/', **generator_args)

train_generator = zip(train_generator_x, train_generator_y)

# Validation data generator
validate_generator_x = train_datagen.flow_from_directory(
        'bin/validate/compressed/', **generator_args)

validate_generator_y = train_datagen.flow_from_directory(
        'bin/validate/uncompressed/', **generator_args)

validate_generator = zip(validate_generator_x, validate_generator_y)


model = model.get_model()

model.fit_generator(
        train_generator,
        steps_per_epoch=200,
        epochs=10,
        validation_data=validate_generator,
        validation_steps=6)

model.save_weights('weights.h5')
print('Saved weights as weights.h5')
