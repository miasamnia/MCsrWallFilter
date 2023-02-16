import os
import keras
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras import layers, models, datasets
from keras.callbacks import EarlyStopping


def read_image(paths):
    os.listdir(paths)
    filelist = []
    for root, dirs, files in os.walk(paths):
        for file in files:
            if os.path.splitext(file)[1] == ".png":
                filelist.append(os.path.join(root, file))
    return filelist


def im_array(paths):
    M = []
    for filename in paths:
        im = Image.open(filename)
        Core = im.getdata()
        arr1 = np.array(Core, dtype='float32') / 255.0
        list_img = arr1.tolist()
        M.extend(list_img)
    return M


images = []
path = 'D:\.desktop\Image\\'
filelist = os.listdir(path)
dic = {}

for type in filelist:
    dic[type] = read_image((path + type))
    images = images + dic[type]

M = []
M = im_array(images)
keys = list(dic.keys())
print(keys)

train_images = np.array(M).reshape(len(images), 480, 216, 3)
train_labels = []
for i in range(len(keys)):
    for j in range(len(dic[keys[i]])):
        train_labels.append(i)
train_labels = np.array(train_labels)
train_images = train_images[..., np.newaxis]

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(480, 216, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(16, activation='softmax'))
model.summary()
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
# EarlyStop = EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='auto')
# test_images = train_images
# test_labels = train_labels
model.fit(train_images, train_labels,epochs=20)
model.save('cher3.h5')
# tf.keras.models.save_model(model,"F:\python\moxing\model")#pb
print("saved.")
