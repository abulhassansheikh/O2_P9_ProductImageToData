# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 10:44:53 2020

@author: AHS
"""
## Model: PT -> L/W/H
#Import packages
import pandas as pd
import numpy as np
import scipy.stats as st

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

#  Compute Mean and Standard Deviation 
#Compile Dimentional Data to construct model
PTRef = pd.DataFrame({"part_type":Image2PT["part_type"].dropna().unique()})

PTDimData = ImageRef.merge(Image2PT, on= "image_name", how="left") 
PTDimData = PTDimData[~PTDimData["image_name"].duplicated(keep=False)] 

PTDimData = PTDimData.merge(Image2Height, on= "image_name", how="left") 
PTDimData = PTDimData[~PTDimData["image_name"].duplicated(keep=False)] 

PTDimData = PTDimData.merge(Image2Length, on= "image_name", how="left") 
PTDimData = PTDimData[~PTDimData["image_name"].duplicated(keep=False)] 

PTDimData = PTDimData.merge(Image2Width, on= "image_name", how="left") 
PTDimData = PTDimData[~PTDimData["image_name"].duplicated(keep=False)] 

#Decleare Height, Width, length, Weight as numeric columns and remove any text
PTDimData["height"] = pd.to_numeric(PTDimData["height"], errors='coerce')
PTDimData["length"] = pd.to_numeric(PTDimData["length"], errors='coerce')
PTDimData["width"] = pd.to_numeric(PTDimData["width"], errors='coerce')

#Remove any NaN values from Part Type
PTDimData = PTDimData[~PTDimData["part_type"].isna()]
alldim = ["height", "length", "width"]

#Parameters for controling dimentional confidence interval
error = 0.1
interval = st.norm.ppf(1-(error)/2)

#Mean & STD of all three dimentions per PT
for d in range(len(alldim)):
    value = alldim[d]

    SingDimData = pd.DataFrame(PTDimData.groupby("part_type")[value].agg(["count", "mean", np.std])).reset_index()    
    SingDimData["interval"]  = interval* (SingDimData["std"] /np.sqrt(SingDimData["count"]))
    SingDimData[value+"_max"] = SingDimData["mean"] + SingDimData["interval"] 
    SingDimData[value+"_min"] = SingDimData["mean"] - SingDimData["interval"] 
    SingDimData = SingDimData[["part_type", "mean", value+"_max", value+"_min"]]
    SingDimData.columns = ["part_type", value+"_mean", value+"_max", value+"_min"]

    PTRef = PTRef.merge(SingDimData, on ="part_type", how = "outer")


CorePath = "C:/Users/abulh/Sync/O2_P9_S1_ImageFiles/O2_P9_ProductImageToData_PR_Models"
(PTRef.to_csv(
        CorePath+"/Pt2LWH_model.csv"
        ,index = None, header=True,  encoding='utf-8'))

# Create model prediction function
def PTdefPred(pt):
    CorePath = "C:/Users/abulh/Sync/O2_P9_S1_ImageFiles/O2_P9_ProductImageToData_PR_Models"
    PTRef = (pd.read_csv(
            CorePath+"/Pt2LWH_model.csv"
            ,encoding='utf-8'))
    
    dim = (PTRef[PTRef["part_type"]==pt][['height_max', 'height_min',
                                         'length_max', 'length_min',
                                         'width_max', 'width_min']])
    return (np.array(dim))
     
#Make preduction

PTweightPred(PTdefPred(pt))




