import tensorflow as tf
import numpy as np
from enum import Enum

def average_diff(eval):
    diffs = []
    predict = []
    grounds = []
    for item in eval:
        grounds.append(item[2])
        predict.append(item[1])
        diffs.append(abs(item[1] - item[2]))
    # for g,p,d in zip(grounds, predict, diffs):
    #     print(f"Ground {g} Predict {p} Diffs {d}")
    return np.average(diffs), np.max(diffs), np.min(diffs), np.std(diffs) 


class NetworkType(Enum):
    FEED_CAT = 0,
    TIME_SERIES_CAT = 1,
    FEED_ANALOG = 2,
    TIME_SERIES_ANALOG = 3


def right_wrong(eval):
    correct = 0
    incorrect = 0
    wrong_buckets = np.zeros(len(eval[0][2]))
    right_buckets = np.zeros(len(eval[0][2]))
    for val in eval:
        if(np.argmax(val[1]) == np.argmax(val[2])):
            correct += 1
            right_buckets[np.argmax(val[1])] += 1
        else:
            incorrect += 1
            wrong_buckets[np.argmax(val[1])] += 1
    return {"Correct" : correct, "Wrong" : incorrect, "MostRight" :  np.argmax(right_buckets), "MostWrong" : np.argmax(wrong_buckets)}


def get_feed_model_default(input_length, output_length):
    model = tf.keras.models.Sequential([
    tf.keras.layers.Input(input_length, name="begin"), 
	tf.keras.layers.Dense(256, activation='relu'),
   	tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(output_length, activation= 'softmax')
    ])
    return model

def get_lstm_model_default(input_length, output_length):
    model = tf.keras.models.Sequential([
    tf.keras.layers.Input(input_length), 
    tf.keras.layers.LSTM(256, input_shape = input_length,name="l1"),
	tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(output_length, activation= 'softmax')
    ])
    return model

def get_feed_model_an(input_length):
    model = tf.keras.models.Sequential([
    tf.keras.layers.Input(input_length, name="begin"), 
	tf.keras.layers.Dense(256, activation='relu'),
   	tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(1, activation= 'sigmoid')
    ])
    return model

def get_lstm_model_an(input_length):
    model = tf.keras.models.Sequential([
    tf.keras.layers.Input(input_length), 
    tf.keras.layers.LSTM(256, input_shape = input_length,name="l1"),
	tf.keras.layers.Dense(128, activation='relu'),
  	tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation= 'sigmoid')
    ])
    return model

class WaitModel(object):
    def __init__(self, data, model=None, is_uni = NetworkType.FEED_CAT, history_size = 5, future_size = 1, optimizer_ = 'adam', 
    loss_ = 'sparse_categorical_crossentropy',  metrics_=['BinaryCrossentropy'], shuffle_size = 600, batch_size = 5):
        vals = data.get_data_raw()
        vals = data.get_data_averaged_hour(vals)
        vals = data.prune_data_hours(vals)
        vals = data.get_data_by_day(vals)
        vals = data.prune_data_empty_days(vals)
        vals = data.transform_from_lists_to_list(vals)
        is_an = False
        if is_uni == NetworkType.FEED_ANALOG or is_uni == NetworkType.TIME_SERIES_ANALOG:
            is_an=True

        if is_an:
            vals = data.get_data_encoded_std(vals)
        else:
            vals = data.get_data_encoded(vals)

        if(is_uni == NetworkType.TIME_SERIES_ANALOG or is_uni == NetworkType.TIME_SERIES_CAT):
            vals = data.univariate_data(vals[0], vals[1], 0, None, history_size, future_size)
        trainx, trainy, self.__testx, self.__testy, valx, valy = data.return_dataset_from_all(vals[0], vals[1])
        self.__train_size = len(trainx)
        self.__val_size = len(valx)
        self.__test_size = len(self.__testx)
        self.__train= tf.data.Dataset.from_tensor_slices((trainx, trainy))
        self.__train = self.__train.shuffle(shuffle_size).batch(batch_size).cache().repeat()
        self.__test= tf.data.Dataset.from_tensor_slices((self.__testx, self.__testy))
        self.__test = self.__test.shuffle(shuffle_size).batch(batch_size).cache().repeat()
        self.__val= tf.data.Dataset.from_tensor_slices((valx, valy))
        self.__val = self.__val.shuffle(shuffle_size).batch(batch_size).cache().repeat()
        if model == None:
            if is_uni == NetworkType.TIME_SERIES_CAT:
                self.__model = get_lstm_model_default(self.__testx[0].shape, max(trainy) + 1)
            elif is_uni == NetworkType.FEED_CAT:
                self.__model = get_feed_model_default(self.__testx[0].shape, max(trainy+1)) 
            elif is_uni == NetworkType.TIME_SERIES_ANALOG:
                self.__model = get_lstm_model_an(self.__testx[0].shape)
            elif is_uni == NetworkType.FEED_ANALOG:
                self.__model = get_feed_model_an(self.__testx[0].shape)
        else:
            self.__model = model
        self.__model.compile(optimizer = optimizer_, loss = loss_ , metrics = metrics_)


    def fit(self, epochs, steps_per_epoch = None, steps_per_epoch_val = None):
        if steps_per_epoch == None:
            steps_per_epoch = self.__train_size
        if steps_per_epoch_val == None:
            steps_per_epoch_val = self.__val_size
        self.__model.fit(self.__train, epochs=epochs, steps_per_epoch=steps_per_epoch, validation_data = self.__val, validation_steps = steps_per_epoch_val)

    def test(self, test_size = None):
        if test_size == None:
            test_size = self.__test_size
        self.__model.evaluate(self.__test, steps=test_size)

    # Will not work for non buckets
    def thorough_evaluation_buckets(self, test_size = None, lambdas = None):
        if test_size == None:
            test_size = self.__test_size
        elif test_size > self.__test_size:
            test_size = self.__test_size
        predictions = []
        for index in range(test_size):
            temp = np.zeros(len(self.__testx[0]))
            temp[self.__testy[index]] = 1
            predictions.append((self.__testx[index], self.__model.predict(np.array([self.__testx[index]])), temp))
        if lambdas == None:
            lambdas = [right_wrong]
        results = []
        for func in lambdas:
            results.append(func(predictions))
        print(results)
        return results

    def thorough_evaluation_analog(self,max_val, test_size = None, lambdas=None):
        if test_size == None:
            test_size = self.__test_size
        elif test_size > self.__test_size:
            test_size = self.__test_size
        predictions = []
        for index in range(test_size):
            print(np.array([self.__testx[index]]))
            predictions.append((self.__testx[index], self.__model.predict(np.array([self.__testx[index]]))*max_val, self.__testy[index]*max_val))
        if lambdas == None:
            lambdas = [average_diff]
        results = []
        for func in lambdas:
            results.append(func(predictions))
        print(results)
        return results       

    def get_model(self):
        return self.__model




