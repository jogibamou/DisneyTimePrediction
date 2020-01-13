from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import numpy as np
from DatasetAPI.thundermountain_wait_dataset import Dataset
batch_size = 5 
shuffle_size = 600

print("Getting wait data")
data = Dataset("public", "filtered_thundermountain_weather2", dataset_limit=10000000)
vals = data.get_data_raw()
vals = data.prune_data_hours(vals)
vals = data.get_data_averaged_hour(vals)
vals = data.get_data_encoded(vals)
vals = data.univariate_data(vals[0], vals[1], 0, None, 5, 1)
train_x, train_y, test_x, test_y, val_x, val_y = data.return_dataset_from_all(vals[0], vals[1])
#train_y = np.reshape(train_y, (1,2))
print("Got data from server")
train= tf.data.Dataset.from_tensor_slices((train_x, train_y))
train = train.shuffle(shuffle_size).batch(batch_size).cache().repeat()
test= tf.data.Dataset.from_tensor_slices((test_x, test_y))
test = test.shuffle(shuffle_size).batch(batch_size).cache().repeat()
val= tf.data.Dataset.from_tensor_slices((test_x, test_y))
val = val.shuffle(shuffle_size).batch(batch_size).cache().repeat()
input_length = train_x[0].shape # Need to actually get the length int from the tuple
print('yeey')
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(input_length), 
    tf.keras.layers.LSTM(256, input_shape = input_length,name="l1"),
	tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(11, activation= 'softmax')
])

model.compile(optimizer = 'adam', loss='sparse_categorical_crossentropy', metrics=['BinaryCrossentropy'])
model.fit(train, epochs=1, steps_per_epoch=10000, validation_data=val, validation_steps=5000)

for i in range(1000):
	d = np.array([train_x[i]])
	predicted = model.predict(d)
	predicted_val = 1 if predicted[0][0] < predicted[0][1] else 0

print("Making manual tests of test data")
correct = 0
incorrect = 0
almost_correct = 0
two_correct = 0
three_correct = 0
times_guessed_zero_wrong =0
wrong_off = []
test_data = []
actual_correct_values = []
actual_correct_values_cat =  np.zeros((11,))
model.evaluate(test, steps=1000)
for i in range(len(test_x)):
	test_data.append((np.array([test_x[i]]), test_y[i]))
for x, y in test_data:
	predicted = model.predict(x)
	predicted_val = np.argmax(predicted)
	if predicted_val == y:
		correct = correct + 1
	else:
		incorrect = incorrect + 1
		if abs(predicted_val - y) < 1.5:
			almost_correct += 1
		elif abs(predicted_val - y) < 2.5:
			two_correct += 1
		elif  abs(predicted_val - y) < 3.5:
			three_correct += 1
		wrong_off.append(abs(predicted_val -y))
		if(predicted_val == 0):
			times_guessed_zero_wrong += 1
		actual_correct_values.append(y)
		actual_correct_values_cat[y] += 1
print(correct)
print(incorrect)
print(f"Correct guesses: {correct}\nIncorrect guesses: {incorrect}\n Percent correct: {correct/(correct + incorrect)}")
print(f"Almost correct {almost_correct}")
print(f"Two correct off {two_correct}")
print(f"Three off {three_correct}")
print(f"Test data {sum(wrong_off)/len(wrong_off)}")
print(f"Times guessed 0 {times_guessed_zero_wrong}")
avg = sum(actual_correct_values) / len(actual_correct_values)
print(f"Average correct value {avg}")
print(f"Actual correct values category {actual_correct_values_cat}")
