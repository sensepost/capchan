import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image

model = keras.models.load_model("model.h5")

image_paths = [
#"Data/G/W0KSM693.png"
    "split_image_1.png",
    "split_image_2.png",
    "split_image_3.png",
    "split_image_4.png"
]

images = []
for image_path in image_paths:
    image = Image.open(image_path)
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    images.append(image)

images = np.array(images)

predictions = model.predict(images)
predicted_classes = np.argmax(predictions, axis=1)

class_to_letter = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
    12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W',
    23: 'X', 24: 'Y', 25: 'Z'
}

predicted_letters = [class_to_letter.get(predicted_class, "Unknown") for predicted_class in predicted_classes]
all_letters = ''.join(predicted_letters)

print("All Letters:", all_letters)

output_file = "output.txt"
with open(output_file, "w") as file:
    file.write(all_letters)

