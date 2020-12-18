import tensorflow as tf
import tensorflow_hub as hub
import time
import time

import tensorflow as tf
import tensorflow_hub as hub


start_time = time.time()
with open('../../resources/preprocessed.txt') as f:
    lines = f.readlines()
print("lead file time => {}".format(time.time() - start_time))
# addresses = list(map(preprocess_address, lines))
print(lines[0:10])

model = hub.load("../4")  # Create function for using model training


#
#
def embed(input):
    return model(input)

def train_model():
    start_time = time.time()
    Model_USE = embed(lines[0:200000])
    exported = tf.train.Checkpoint(v=tf.Variable(Model_USE))
    exported.f = tf.function(lambda x: exported.v * x, input_signature=[tf.TensorSpec(shape=None, dtype=tf.float32)])
    tf.saved_model.save(exported, '../../resources/trained_USE')
