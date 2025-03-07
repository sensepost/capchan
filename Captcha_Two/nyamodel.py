import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

np.random.seed(42)
tf.random.set_seed(42)

image_size = (224, 224)
batch_size = 32
num_classes = 26
epochs = 25

train_data_dir = "Captcha_Two/Data"
val_data_dir = "Captcha_Two/Val"

train_data = keras.preprocessing.image.ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=1,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=False
)

val_data = keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)

train_generator = train_data.flow_from_directory(
    train_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode="sparse",
    shuffle=True
)

val_generator = val_data.flow_from_directory(
    val_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode="sparse"
)

model = keras.Sequential([
    layers.Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=(image_size[0], image_size[1], 3)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dense(num_classes, activation="softmax")
])

model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=val_generator,
    validation_steps=val_generator.samples // batch_size
)

model.save("model.h5")
