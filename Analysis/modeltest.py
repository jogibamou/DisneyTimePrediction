from DatasetAPI.thundermountain_wait_dataset import Dataset
from DatasetAPI.ride_dic import rides
from Model.wait_model import WaitModel, get_feed_model_default, get_lstm_model_default, NetworkType
import tensorflow as tf


models = []
for ride in list(rides.keys()):
    data = Dataset(rides[ride], 100000000)

    waitmodel = WaitModel(data, None, NetworkType.FEED_ANALOG,
    loss_=tf.keras.losses.Poisson())

    #waitmodel = WaitModel(data, None, NetworkType.FEED_ANALOG)

    waitmodel.fit(1)

    waitmodel.test()

    #waitmodel.thorough_evaluation_buckets()
    print(ride)
    waitmodel.thorough_evaluation_analog(rides[ride]["max"])
    waitmodel.get_model().save(f"model_data/{ride}.h5")









