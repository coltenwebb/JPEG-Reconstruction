from keras.layers import Input, Dense, Reshape, Flatten
from keras.models import Model, Sequential

def get_model():
    model = Sequential()

    model.add(Flatten(input_shape=(256,256,1)))
    model.add(Dense(256, input_shape=(65536,), activation='relu'))
    model.add(Dense(65536, input_shape=(256,), activation='sigmoid'))
    model.add(Reshape((256,256,1), input_shape=(65536,)))
    # model.output_shape => (None, 256, 256, 1)

    model.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])

    return model
