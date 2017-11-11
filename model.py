from keras.layers import Input, Dense, Reshape, Flatten, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model, Sequential


def get_model():
    return get_conv()


def get_ddn():
    model = Sequential()

    model.add(Flatten(input_shape=(256, 256, 1)))
    model.add(Dense(512, input_shape=(65536, ), activation='relu'))
    model.add(Dense(256, input_shape=(512, ), activation='relu'))
    model.add(Dense(512, input_shape=(256, ), activation='relu'))
    model.add(Dense(65536, input_shape=(512, ), activation='sigmoid'))
    model.add(Reshape((256, 256, 1), input_shape=(65536, )))
    # model.output_shape => (None, 256, 256, 1)

    model.compile(
        optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])

    return model


def get_conv():
    model = Sequential()
    
    # encode
    model.add(
        Conv2D(
            256, (3, 3),
            input_shape=(96, 96, 1),
            activation='relu',
            padding='same'))

    # model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
    # model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(128, (5, 5), activation='relu', padding='same'))
    # model.add(MaxPooling2D((2, 2)))
    
    # decode
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    # model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
    # model.add(UpSampling2D((2, 2)))

    model.add(Conv2D(1, (3, 3), activation='sigmoid', padding='same'))

    model.add(Reshape((96, 96, 1), input_shape=(9216, )))
    # model.output_shape => (None, 256, 256, 1)

    model.compile(
        optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])
     # model.compile(
     #    optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])


    return model


if __name__ == '__main__':
    print(get_model().output_shape)
