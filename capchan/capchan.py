#!/usr/bin/python3

import questionary
from yaml import safe_load
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #lol
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense
from PIL import Image

import random
from some import model_layout 
from some import neural_network
from some import weights_biases
from some import RS_function 

start_list = [model_layout, neural_network, weights_biases, RS_function]
chosen_one = random.choice(start_list)
chosen_one()

def get_config():
    with open('c_config.yaml', 'r') as file:
        content = file.read()
    config = safe_load(content)
    return config

def s_project():
    config = get_config()
    projects = questionary.select('Choose the type of project below', choices=config['projects']).ask()
    if projects == "New Model":
        proj_name = questionary.text('Name of project to save').ask()
        classes = questionary.select('Choose how you would need to set up the classes', choices=config['classes']).ask()
        if classes == "Pre-Defined":
            classes_PreDef = questionary.checkbox('Choose the type of classes you need', choices=config['classes_PreDef']).ask()
            custom_class_tot  = 0
            if 'Numbers' in classes_PreDef:
                custom_class_tot += 10
            if 'Uppercase Letters' in classes_PreDef:
                custom_class_tot += 26
            if 'Lowercase Letters' in classes_PreDef:
                custom_class_tot += 26
            custom_class_train = questionary.path('Set location to training data folder').ask()
            custom_class_val = questionary.path('Set location to validation data folder').ask()

            output_file = proj_name + ".cmapp"
            with open(output_file, "w") as file:
                if os.path.exists(custom_class_train):
                    classes_in_train = len([f for f in os.listdir(custom_class_train) if os.path.isdir(os.path.join(custom_class_train, f))])
                    file.write("Class Mapping:\n")
                    for class_num, folder_name in enumerate(sorted(os.listdir(custom_class_train))):
                        if os.path.isdir(os.path.join(custom_class_train, folder_name)):
                            file.write(f"Class {class_num}: {folder_name}\n")
                else:
                    classes_in_train = 0
                if os.path.exists(custom_class_val):
                    classes_in_val = len([f for f in os.listdir(custom_class_val) if os.path.isdir(os.path.join(custom_class_val, f))])
                else:
                    classes_in_val = 0
                if classes_in_train == classes_in_val == int(custom_class_tot):
                    file.write('Check Pass\n')
                else:
                    print('Issue with either folder existence or non-matching class amounts ' + 'Train:' + str(classes_in_train) + ' Val:' + str(classes_in_val) + ' Amt:' + str(custom_class_tot) + '\n')
                    os._exit(1)
        else:
            custom_class_tot = questionary.text('Set amount of classes').ask()
            custom_class_train = questionary.path('Set location to training data folder').ask()
            custom_class_val = questionary.path('Set location to validation data folder').ask()

            output_file = proj_name + ".cmapp"
            with open(output_file, "w") as file:
                if os.path.exists(custom_class_train):
                    classes_in_train = len([f for f in os.listdir(custom_class_train) if os.path.isdir(os.path.join(custom_class_train, f))])
                    file.write("Class Mapping:\n")
                    for class_num, folder_name in enumerate(sorted(os.listdir(custom_class_train))):
                        if os.path.isdir(os.path.join(custom_class_train, folder_name)):
                            file.write(f"Class {class_num}: {folder_name}\n")
                else:
                    classes_in_train = 0
                if os.path.exists(custom_class_val):
                    classes_in_val = len([f for f in os.listdir(custom_class_val) if os.path.isdir(os.path.join(custom_class_val, f))])
                else:
                    classes_in_val = 0
                if classes_in_train == classes_in_val == int(custom_class_tot):
                    file.write('Check Pass\n')
                else:
                    print('Issue with either folder existence or non-matching class amounts ' + 'Train:' + str(classes_in_train) + ' Val:' + str(classes_in_val) + ' Amt:' + str(custom_class_tot) + '\n')
                    os._exit(1)
 
        adv_mode = questionary.confirm('Enter Advanced Mode?').ask()
        if adv_mode == False:
            print('Setting default hyperparameters')
            epoch_tot = 10 
            batch_tot = 32  
        else:
            #Batch_Size
            #ie 100 images = 1 full epoch
            #ie 1000 images / 10 Batche = 100 Epochs
        
            #images 3000
            #batch size 32 - smaller = less accurate/ larger = overfitting
            #epoch 500
            #A: 3000/32 = 94 = 1 epoch

            epoch_tot = questionary.text('Set amount of network iterations').ask()
            batch_tot = questionary.text('Set batch size (recommended 32)').ask()
        
        np.random.seed(42)
        tf.random.set_seed(42)

        image_size = (224, 224)
        #The below might cause issue later
        input_shape = (224, 224, 1)  
        #batch_size=None # 32
        #Small Batch = More Epochs / Big Batch = Less Epoch
        batch_size = int(batch_tot) #16, 32, 64, 128, 256, 512 and 1024 
        num_classes = int(custom_class_tot)
        epochs = int(epoch_tot)
        train_data_dir = custom_class_train
        val_data_dir = custom_class_val

        train_data = keras.preprocessing.image.ImageDataGenerator(
            rescale=1.0 / 255,
            rotation_range=1,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=False
        )

        val_data = keras.preprocessing.image.ImageDataGenerator(
            rescale=1.0 / 255
        )

        train_generator = train_data.flow_from_directory(
            train_data_dir,
            target_size=image_size,
            color_mode="grayscale",  
            batch_size=batch_size,
            class_mode="sparse",
            shuffle=True
        )

        val_generator = val_data.flow_from_directory(
            val_data_dir,
            target_size=image_size,
            color_mode="grayscale",  
            batch_size=batch_size,
            class_mode="sparse"
        )

        model = keras.Sequential([
            #below input may also cause issue with other images
            Input(shape=input_shape),  
            Conv2D(32, kernel_size=(3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(64, kernel_size=(3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dense(128, activation="relu"),
            Dense(num_classes, activation="softmax")
        ])
        
        model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

        model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // batch_size,
            epochs=epochs,
            validation_data=val_generator,
            validation_steps=val_generator.samples // batch_size
        )

        model.save(proj_name + ".h5")
        print('\nModel created on: ' + proj_name + ".h5")
        print(f"Mappings saved to {output_file}")
        
    elif projects == 'Start PoC':
        import_path = questionary.path('Provide Path to model (.h5 format)').ask()
        import_mapping = questionary.path('Provide Path to model mapping (.cmapp format)').ask()
        image_Spaths = questionary.select('Choose the following image provisions', choices=config['image_SPath']).ask()
        if image_Spaths == "Test against folder of images":
            image_Sone = questionary.path('Define Folder Path').ask()
            image_paths = [os.path.join(image_Sone, filename) for filename in os.listdir(image_Sone) if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
        else:
            image_Sone = questionary.path('Define Image Path').ask()
            image_paths = [image_Sone]

        model = keras.models.load_model(import_path)

        images = []
        for image_path in image_paths:
            image = Image.open(image_path)
            image = image.resize((224, 224))
            image = np.array(image) / 255.0
            images.append(image)

        images = np.array(images)

        predictions = model.predict(images)
        predicted_classes = np.argmax(predictions, axis=1)

        class_mapping = {}
        with open(import_mapping, 'r') as cmapp_file:
            for line in cmapp_file:
                if line.startswith('Class'):
                    parts = line.split(': ')
                    if len(parts) == 2:
                        class_num, class_name = parts[0].split(' ')[-1], parts[1].strip()
                        class_mapping[class_num] = class_name

        predicted_letters = [class_mapping.get(str(predicted_class), "Unknown") for predicted_class in predicted_classes]
        class_tot = ' '.join(predicted_letters)

        print("capchan says: ", class_tot)

    elif projects == 'Help Page':
        print('https://sensepost.com/blog/2025/capchan-solving-captcha-with-image-classification/')
    else:
        print('bye bye')

if __name__ == "__main__":
    s_project()
