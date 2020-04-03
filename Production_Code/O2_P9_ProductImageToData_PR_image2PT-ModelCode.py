# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 19:13:58 2020

@author: AHS
"""

#load packages
import pandas as pd
import numpy as np
from numpy import save
from numpy import load
import os
from PIL import Image
from sklearn.model_selection import train_test_split
import tensorflow as tf
import pickle


#Set input and output Paths
inputPath = "C:/Users/abulh/Sync/O2_P9_S1_ImageFiles/O2_P9_S1_ImageFiles"
outputPath = "C:/Users/abulh/Sync/O2_P9_S1_ImageFiles/O2_P9_S1_ImageFiles28"

#Load data
Image2Brand = pd.read_csv("C:/Users/abulh/Sync/Documents/O2_P9_S1_ImageData/O2_P9_S1_ImageData_PR_Image2Brand.csv")
Image2PT = pd.read_csv("C:/Users/abulh/Sync/Documents/O2_P9_S1_ImageData/O2_P9_S1_ImageData_PR_Image2PT.csv")
Image2Category = pd.read_csv("C:/Users/abulh/Sync/Documents/O2_P9_S1_ImageData/O2_P9_S1_ImageData_PR_Image2Category.csv")
Image2Weight = pd.read_csv("C:/Users/abulh/Sync/Documents/O2_P9_S1_ImageData/O2_P9_S1_ImageData_PR_Image2Weight.csv")
Image2Width = pd.read_csv("C:/Users/abulh/Sync/Documents/O2_P9_S1_ImageData/O2_P9_S1_ImageData_PR_Image2Width.csv")
Image2Height = pd.read_csv("C:/Users/abulh/Sync/Documents/O2_P9_S1_ImageData/O2_P9_S1_ImageData_PR_Image2Height.csv")
Image2Length = pd.read_csv("C:/Users/abulh/Sync/Documents/O2_P9_S1_ImageData/O2_P9_S1_ImageData_PR_Image2Length.csv")

Image2Category.columns = ['image_name', 'categories', 'count', 'levCount', 'L1', 'L3', 'L2']

#Clean data
ilst = Image2Brand["image_name"].unique()
ilst = np.append(ilst, Image2PT["image_name"].unique())
ilst = np.append(ilst, Image2Height["image_name"].unique())
ilst = np.append(ilst, Image2Length["image_name"].unique())
ilst = np.append(ilst, Image2Width["image_name"].unique())
ilst = np.append(ilst, Image2Weight["image_name"].unique())
ilst = np.append(ilst, Image2Category["image_name"].unique())

ImageRef = pd.DataFrame({"image_name":list(set(ilst))})
ImageRef = ImageRef[~ImageRef["image_name"].isna()] #297308


#Identify which images present in folder and Part Type Referenc
Image2PT.columns = ["image", "part_type"]
PTImages = set(Image2PT["image"])
ImageFiles28_set = set(os.listdir(outputPath))
len(PTImages)
len(ImageFiles28_set)
UsablePTImages = ImageFiles28_set.intersection(PTImages)

PTNNdf = Image2PT[["image", "part_type"]][Image2PT["image"].isin(UsablePTImages)]
PTNNdf["part_type"] = [s.strip() for s in PTNNdf["part_type"]]
PTNNdf["PT_num"] =PTNNdf["part_type"].astype('category').cat.codes

#Load and save image file & File PT Classification reference
ImageFiles28 = np.array(PTNNdf["image"])
ImageFiles28Ref = ImageFiles28
save(outputPath+"/ImageFiles28Ref_PT.npy", ImageFiles28)
ImageFiles28Ref = load(outputPath+"/ImageFiles28Ref_PT.npy", allow_pickle=True)

Image28_PT = np.array(PTNNdf["PT_num"])
save(outputPath+"/Image28_PT.npy", Image28_PT)
Image28_PT = load(outputPath+"/Image28_PT.npy", allow_pickle=True)

#Turn Images into array and save
All28ImagePath = [outputPath+"/"+i for i in ImageFiles28]
All_images = [np.array(Image.open(i)) for i in All28ImagePath]
All_images = np.array(All_images)
save(outputPath+"/ImageFiles28_PT.npy", All_images)
Image28data_PT = load(outputPath+"/ImageFiles28_PT.npy")

Image28data_PT.shape
Image.fromarray(All_images[1])

#Set model parameters
kI = "VarianceScaling"
bI = "VarianceScaling"
kR = tf.keras.regularizers.l2(0.01)

X_train, X_test, y_train, y_test = train_test_split(
    Image28data_PT, Image28_PT, test_size=0.33, random_state=42)

x_train = X_train / 255.0
X_test = X_test / 255.0

# Build the model including the custom layer
PTmodel = tf.keras.Sequential([
                                                                   
    tf.keras.layers.Flatten(),

                                  
    tf.keras.layers.Dense(1000, activation='relu',kernel_initializer=kI ,
                          kernel_regularizer =kR, 
                          bias_initializer = bI),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Dense((3000), activation='relu', kernel_initializer=kI ,
                          kernel_regularizer =kR, 
                          bias_initializer = bI),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Dense(2584, activation='softmax')
])

PTmodel.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

PTmodel.summary()

PTmodel.fit(x_train, y_train, epochs=2)
PTmodel.evaluate(X_test,  y_test, verbose=10)


#Turn Images into array and save
All_images_test = np.array(Image.open(All28ImagePath[0]))


PTmodel.predict(X_test[:1])
                                  




