import os

from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import keras

import model as model

import argparse

parser = argparse.ArgumentParser(description='Trains the network')
parser.add_argument('--epochs', type=int, default=5, required=False,
                    help='number of epochs')
parser.add_argument('--epoch_size', type=int, default=1000, required=False,
                    help='size of epoch')
parser.add_argument('--batch_size', type=int, default=16, required=False,
                    help='size of epoch')
parser.add_argument('--validation_steps', type=int, default=-1, required=False,
                    help='number of steps per validation. should be validation sample size/batch_size')



args = parser.parse_args()
print(args)

BATCH_SIZE = args.batch_size
EPOCHS = args.epochs
EPOCH_STEPS = args.epoch_size
VALIDATION_STEPS = 1000 / BATCH_SIZE if args.validation_steps == -1 else args.validation_steps

train_datagen = ImageDataGenerator(rescale=1. / 255)

# Args for the training data generator. Both x and y should be identical,
# so they are put into a tuple
generator_args = dict(
    target_size=(96, 96),
    batch_size=BATCH_SIZE,
    class_mode=None,
    color_mode='rgb',
    seed=1)

train_generator_x = train_datagen.flow_from_directory('bin/train/compressed/',
                                                      **generator_args)

train_generator_y = train_datagen.flow_from_directory(
    'bin/train/uncompressed/', **generator_args)

train_generator = zip(train_generator_x, train_generator_y)

# Validation data generator
validate_generator_x = train_datagen.flow_from_directory(
    'bin/validate/compressed/', **generator_args)

validate_generator_y = train_datagen.flow_from_directory(
    'bin/validate/uncompressed/', **generator_args)

validate_generator = zip(validate_generator_x, validate_generator_y)

if __name__ == "__main__":
    tb_callback = keras.callbacks.TensorBoard(
        log_dir='./tmp', write_graph=True, write_images=True)
    checkpointer = keras.callbacks.ModelCheckpoint(filepath='./weight_checkpoints/weights.hdf5', verbose=1, save_best_only=True)

    model = model.get_model()

    model.fit_generator(
        train_generator,
        steps_per_epoch=EPOCH_STEPS,
        epochs=EPOCHS,
        validation_data=validate_generator,
        validation_steps=VALIDATION_STEPS,
        callbacks=[tb_callback, checkpointer])

    model.save_weights('weights.h5')
    print('Saved weights as weights.h5')
