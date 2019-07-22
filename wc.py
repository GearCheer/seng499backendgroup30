"""
Written in Python 3.7.3

Requires keras and tensorflow

Install dependencies using:
    pip3 install keras
    pip3 install tensorflow
"""

from keras.applications.resnet50 import ResNet50
from keras.preprocessing.image import img_to_array, load_img, ImageDataGenerator
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model, load_model
import argparse
import time
import os

# CONSTANTS
MODEL_PATH = "models/model.h5"
NUM_CLASSES = 9 # Number of classes (1 for each folder in dataset).

# For full dataset
DATASET_PATH = "reclassified-dataset" # Path to dataset from working directory.
NUM_EPOCHS = 80
BATCH_SIZE = 32  # Number of images in each batch generated by the image generator.
                 # Equals the number of images considered before updating weights when training the model.
VALIDATION_STEPS = 82 # number of testing images divided by the batch size

# For small testing dataset
# DATASET_PATH = "reclassified-dataset-small" # Path to dataset from working directory.
# NUM_EPOCHS = 18
# BATCH_SIZE = 5
# VALIDATION_STEPS = 17

class Classifier:

    def __init__(self, model_path=None, imageset_path=None):

        self.model = None

        if imageset_path:
            self._train_new_model(imageset_path)
        elif model_path:
            self._load_model_weights(model_path)

    def _train_new_model(self, imageset_path):

        datagen = ImageDataGenerator()

        # Create iterator for training images
        train_it = datagen.flow_from_directory(imageset_path + '/Train', target_size=(384, 512), batch_size=BATCH_SIZE)
        test_it  = datagen.flow_from_directory(imageset_path + '/Test', target_size=(384, 512), batch_size=BATCH_SIZE)


        # Create model with ResNet50 weights, but drop top layer
        res_model = ResNet50(input_shape=(384, 512, 3), weights='imagenet', include_top=False)

        # Add new top layer.  This is a fully connected layer with one node for each output class.
        x = res_model.output
        x = GlobalAveragePooling2D()(x)
        predictions = Dense(NUM_CLASSES, activation='softmax')(x)
        self.model = Model(inputs=res_model.input, outputs=predictions)

        # Set all but last layer to be untrainable
        for layer in self.model.layers[:-1]:
            layer.trainable=False

        # Set last layer to be trainable
        for layer in self.model.layers[-1:]:
            layer.trainable=True

        # Compile and fit
        self.model.compile(optimizer='SGD', loss='categorical_crossentropy', metrics=['accuracy']) # old: categorical_crossentropy
        self.model.fit_generator(train_it, epochs=NUM_EPOCHS, steps_per_epoch=BATCH_SIZE, verbose=1, validation_data=test_it, validation_steps=VALIDATION_STEPS)

    def _load_model_weights(self, model_path):
        self.model = load_model(model_path)

    def save_model_weights(self):

        # TODO: YOU ALTERED THIS PATH
        # if os.path.exists('models/model.h5'):
        #     self.model.save('models/model_{}.h5'.format(int(time.time())))
        # else:
        #     self.model.save('models/model.h5')

        self.model.save('models/test_model.h5')

    def classify(self, img):
        #TODO: image preprocessing ( ie. resizing to (384, 512, 3) )
        return self.model.predict(img) #TODO: see what this outputs (should be integer)

    # def test(self):
    #
    #     datagen = ImageDataGenerator()
    #
    #     # Create iterator for training/validation/test images
    #     test_it  = datagen.flow_from_directory(TESTSET_PATH, target_size=(384, 512), batch_size=BATCH_SIZE)
    #

# executes testing code when run as main
if __name__ == "__main__":
    # Generate and save a model
    wc = Classifier(imageset_path=DATASET_PATH)
    wc.save_model_weights()
    #
    # # Load a model
    # #wc2 = Classifier(model_path=MODEL_PATH)
    # args = parser.parse_

    # if --load "/path"

    #

