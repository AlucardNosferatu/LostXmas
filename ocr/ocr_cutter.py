import os

import cv2
from tqdm import tqdm

files = os.listdir('pics')
for file in tqdm(files):
    filepath = os.path.join('pics', file)
    cv2.imread('')

    with open(os.path.join('texts', file + '.txt'), mode='w', encoding='utf-8') as text_file:
        pass
