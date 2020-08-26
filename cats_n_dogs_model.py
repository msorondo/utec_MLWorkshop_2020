import tensorflow as tf
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.training.rmsprop import RMSPropOptimizer

def keras_model_fn(hyperparameters):
    model = Sequential()

    model.add(Conv2D(32, kernel_size=(3, 3), input_shape=(128, 128, 3), activation="relu", name="inputs"))
    model.add(MaxPooling2D(pool_size = (2,2)))
              
    model.add(Conv2D(64, kernel_size=(3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size = (2,2)))
    model.add(Dropout(0.4))

    model.add(Conv2D(128, kernel_size=(3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size = (2,2)))
    model.add(Dropout(0.4))
              
    model.add(Conv2D(256, kernel_size=(3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size = (2,2)))
    model.add(Dropout(0.4))

    model.add(Conv2D(512, kernel_size=(1, 1), activation="relu"))
    
    model.add(Flatten())
    model.add(Dropout(0.4))


    model.add(Dense(units=120, activation="relu"))
    model.add(Dense(units=2, activation="sigmoid"))
              

    opt = RMSPropOptimizer(learning_rate=hyperparameters['learning_rate'], decay=hyperparameters['decay'])

    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=["accuracy"])
    #model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    #model.summary()
              
    return model

def serving_input_fn(hyperparameters):
    tensor = tf.placeholder(tf.float32, shape=[None, 128, 128, 3])
    inputs = {"inputs_input": tensor}
    return tf.estimator.export.ServingInputReceiver(inputs, inputs)

def train_input_fn(training_dir, hyperparameters):
    return _input(tf.estimator.ModeKeys.TRAIN, batch_size=64, data_dir=training_dir)

def eval_input_fn(training_dir, hyperparameters):
    return _input(tf.estimator.ModeKeys.EVAL, batch_size=64, data_dir=training_dir)

def _input(mode, batch_size, data_dir):

    if mode == tf.estimator.ModeKeys.TRAIN:
        datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True
        )
    else:
        datagen = ImageDataGenerator(rescale=1. / 255)

    generator = datagen.flow_from_directory(data_dir, target_size=(128, 128), batch_size=batch_size)
    images, labels = generator.next()

    return {"inputs_input": images}, labels