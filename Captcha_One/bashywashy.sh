#!/bin/bash

python3 ImageGet.py -s domain.local -v --debug

python3 ImageSplit.py --image_path image.png

python3 ImageDetermine.py --split_images_folder ~/Captcha_One --data_folder Images/
