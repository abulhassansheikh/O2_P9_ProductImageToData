# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:30:25 2020

@author: AHS
"""

## Model: L/W/H -> Weight

#Import packages
import pandas as pd
import numpy as np
import scipy.stats as st
import statsmodels.formula.api as smf

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

#Compile Dimentional Data to construct model
DimData = ImageRef.merge(Image2Height, on= "image_name", how="left") 
DimData = DimData[~DimData["image_name"].duplicated(keep=False)] 

DimData = DimData.merge(Image2Length, on= "image_name", how="left") 
DimData = DimData[~DimData["image_name"].duplicated(keep=False)] 

DimData = DimData.merge(Image2Width, on= "image_name", how="left") 
DimData = DimData[~DimData["image_name"].duplicated(keep=False)] 

DimData = DimData.merge(Image2Weight, on= "image_name", how="left") 
DimData = DimData[~DimData["image_name"].duplicated(keep=False)] 

#Decleare Height, Width, length, Weight as numeric columns and remove any text
DimData["height"] = pd.to_numeric(DimData["height"], errors='coerce')
DimData["length"] = pd.to_numeric(DimData["length"], errors='coerce')
DimData["width"] = pd.to_numeric(DimData["width"], errors='coerce')
DimData["weight"] = pd.to_numeric(DimData["weight"], errors='coerce')

#Remove any NaN values 
DimData = DimData[
             ~DimData["height"].isna() &
             ~DimData["length"].isna() &
             ~DimData["width"].isna() &
             ~DimData["weight"].isna()]

#Lets create volume column also
DimData["volume"] = DimData["height"] * DimData["length"] * DimData["width"] 

# Multivariable Regression
#Switch to scikitlearn
Dim_model = smf.ols(formula = 'weight ~ height+ length+ width + volume', data=DimData)
Dim_model = Dim_model.fit()
Dim_model.summary()

Dim_model = pd.DataFrame(Dim_model.params[0:5].reset_index())
Dim_model.columns = ["coefName", "coef"]

CorePath = "C:/Users/abulh/Sync/O2_P9_S1_ImageFiles/O2_P9_ProductImageToData_PR_Models"
(Dim_model.to_csv(
        CorePath+"/Dim_model.csv"
        ,index = None, header=True,  encoding='utf-8'))


# Create model prediction function
def PTweightPred(PTdimPre):
    CorePath = "C:/Users/abulh/Sync/O2_P9_S1_ImageFiles/O2_P9_ProductImageToData_PR_Models"
    Dim_model = (pd.read_csv(
            CorePath+"/Dim_model.csv"
            ,encoding='utf-8'))
    
    intercept = Dim_model.coef[0]
    heightCoef = Dim_model.coef[1]
    lenghtCoef = Dim_model.coef[2]
    widthCoef = Dim_model.coef[3]
    volumeCoef = Dim_model.coef[4]
    
    uHeight, bHeight = PTdimPre[0, 0:2]
    uLength, bLength = PTdimPre[0, 2:4]
    uWidth, bWidth = PTdimPre[0, 4:6]
    uVolume = uHeight * uLength * uWidth
    bVolume = bHeight * bLength * bWidth

    uWeight = (intercept + heightCoef*uHeight + lenghtCoef*uLength + 
                          widthCoef*uWidth + volumeCoef*uVolume) 
    bWeight = (intercept + heightCoef*bHeight + lenghtCoef*bLength + 
                          widthCoef*bWidth + volumeCoef*bVolume)
    
    return (np.array([uWeight, bWeight]))




