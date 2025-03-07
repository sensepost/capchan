import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from graphviz import Digraph

np.random.seed(42)
tf.random.set_seed(42)

image_size = (224, 224)
num_classes = 26

test_data_dir = "Data"

test_images = []
test_labels = []

for class_name in sorted(os.listdir(test_data_dir)):
    class_dir = os.path.join(test_data_dir, class_name)
    if os.path.isdir(class_dir):
        for image_name in os.listdir(class_dir):
            image_path = os.path.join(class_dir, image_name)
            image = keras.preprocessing.image.load_img(image_path, target_size=image_size)
            image_array = keras.preprocessing.image.img_to_array(image) / 255.0
            test_images.append(image_array)
            test_labels.append(ord(class_name) - ord('A'))

test_images = np.array(test_images)
test_labels = np.array(test_labels)

model = keras.models.load_model("model.h5")

model.summary()
tf.keras.utils.plot_model(model, to_file='model_graph.png', show_shapes=True, show_layer_names=True)

#img = plt.imread('model_graph.png')
#plt.imshow(img)
#plt.axis('off')
#plt.show()
#network_layers = model.layers
#for layer in network_layers:
#    print(layer.name, layer.input_shape, layer.output_shape)

tf.config.run_functions_eagerly(True)

predictions = model.predict(test_images)

tf.config.run_functions_eagerly(False)

predicted_classes = np.argmax(predictions, axis=1)

correct_guesses = 0
wrong_guesses = 0
for i in range(len(test_images)):
    predicted_class = chr(ord('A') + predicted_classes[i])
    true_class = chr(ord('A') + test_labels[i])
    
    if predicted_class == true_class:
        print(f"Predicted: {predicted_class}, True: {true_class}")
        correct_guesses += 1
    else:
        print(f"\033[91mPredicted: {predicted_class}, True: {true_class}\033[0m")
        wrong_guesses += 1

total_guesses = correct_guesses + wrong_guesses

accuracy = correct_guesses / total_guesses
print(f"\nCorrect Guesses: {correct_guesses}/{total_guesses}")
print(f"Wrong Guesses: {wrong_guesses}/{total_guesses}")
print(f"Accuracy: {accuracy}")

