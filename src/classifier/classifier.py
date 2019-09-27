from __future__ import absolute_import, division, print_function, unicode_literals

import pandas
import subprocess

import tensorflow as tf
from tensorflow import keras
import numpy

from Dictionary import Encoder


class Classifier:
    labels = {
        "unrelated": 0,
        "savings": 1,
        "investment": 2,
        "insurance": 3,
        "health": 4,
        "mortgages": 5,
        "loan": 6,
        "retirement": 7
    }

    def __init__(self, model_path: str = "model/model.h5", data_path: str = "resources/data.csv",
                 labels_path: str = "resources/labels.csv", checkpoint_dir: str = "checkpoints/",
                 retrain: bool = False):
        self.model_path = model_path
        # If model does not exist or told to retrain, recreate model
        if retrain or not self.reload():
            self.create()
            self.train(data_path, labels_path, checkpoint_dir)
        self.encoder = Encoder()

    def create(self):
        vocab_size = self.getvocabsize()
        self.model = keras.models.Sequential([
            keras.layers.Embedding(vocab_size, 64, input_length=250),
            keras.layers.Conv1D(64, 5, activation=keras.activations.relu),
            keras.layers.GlobalMaxPooling1D(),
            keras.layers.Dense(20, activation=keras.activations.relu),
            keras.layers.Dense(8, activation=keras.activations.sigmoid)
        ])
        self.model.compile(
            optimizer=keras.optimizers.Adam(),
            loss="binary_crossentropy",
            metrics=["accuracy"]
        )
        self.model.summary()
        return

    def predict(self, text):
        encoded = self.encoder.encode(text)
        np_arr = numpy.array(encoded)
        predictions = self.model.predict(np_arr)

        max_value = predictions.max()
        highest = 0
        for i in range(len(predictions)):
            if predictions[i] == max_value:
                highest = i

        return Classifier.labels.keys()[highest], max_value  # Returns (str, int) representing the label and confidence

    def save(self):
        self.model.save(self.model_path)
        return

    def reload(self):
        try:
            self.model = keras.models.load_model(self.model_path)
            self.model.summary()
        except Exception as e:
            print("ERROR!\n", e)
            return False
        return True

    def train(self, data_path: str, label_path: str, checkpoint_dir: str):
        dataset = self.getdataset(data_path, label_path)
        checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(checkpoint_dir,
                                                           save_weights_only=True,
                                                           verbose=1)
        tensorboard_cb = keras.callbacks.TensorBoard(log_dir='logs/')

        history = self.model.fit(dataset.batch(1), epochs=1, callbacks=[checkpoint_cb, tensorboard_cb])

        self.save()
        return history

    def getdataset(self, data_path: str, label_path: str):
        data = pandas.read_csv(data_path)
        labels = pandas.read_csv(label_path)

        return tf.data.Dataset.from_tensor_slices((data.values, labels.values)).shuffle(labels.size)

    def getvocabsize(self, path: str = "resources/dataset/dictionary"):
        command = "wc -l " + path
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return int(output.decode("utf-8").split(" ")[0])
