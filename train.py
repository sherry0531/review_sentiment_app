import numpy as np
from tensorflow import keras
from keras import models
from keras import layers
from keras.datasets import imdb

# load data
(training_data, training_targets), (testing_data, testing_targets) = imdb.load_data(num_words=10000)
data = np.concatenate((training_data, testing_data), axis=0)
targets = np.concatenate((training_targets, testing_targets), axis=0)
index = imdb.get_word_index()


# data prep
def w_to_index(text, index):
    lst = []
    non_exist = 9999999
    for w in text.split(" "):
        try:
            w_indx = index[w.lower()]
        except:
            w_indx = non_exist
        lst += [w_indx]
    return([lst])

def vectorize(sequences, dimension = 10000):
    non_exist = 9999999
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        sequence = [w for w in sequence if w != non_exist]
        results[i, sequence] = 1
    return results

data = w_to_index(data, index)
data = vectorize(data)
targets = np.array(targets).astype("float32")

# 90/10 train test split
test_x = data[:9000]
test_y = targets[:9000]
train_x = data[1000:]
train_y = targets[1000:]


# model training
model = keras.models.Sequential([
    layers.Dense(50, activation = "relu", input_shape=(10000, )),
    layers.Dropout(0.3, noise_shape=None, seed=None),
    layers.Dense(50, activation = "relu"),
    layers.Dropout(0.2, noise_shape=None, seed=None),
    layers.Dense(50, activation = "relu"),
    layers.Dense(1, activation = "sigmoid")

])

model.compile(
 optimizer = "adam",
 loss = "binary_crossentropy",
 metrics = ["accuracy"]
)

results = model.fit(
 train_x, train_y,
 epochs= 2,
 batch_size = 500,
 validation_data = (test_x, test_y)
)

print(np.mean(results.history["val_accuracy"]))

# save
model.save('my_model')



