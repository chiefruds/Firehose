from __future__ import absolute_import, division, print_function, unicode_literals

import pandas
import os
import subprocess

import tensorflow as tf
from tensorflow import keras


class Classifier:
    def __init__(self, model_path: str = "model/model.h5", data_path: str = "resources/data.csv", labels_path: str = "resources/labels.csv", checkpoint_dir: str = "checkpoints/", retrain: bool = False):
        self.model_path = model_path
        # If model does not exist or told to retrain, recreate model
        if retrain or not self.reload():
            self.create()
            self.train(data_path, labels_path, checkpoint_dir)

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

        return

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
        callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_dir,
                                                      save_weights_only=True,
                                                      verbose=1)

        history = self.model.fit(dataset.batch(1), epochs=1, callbacks=[callback])

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
