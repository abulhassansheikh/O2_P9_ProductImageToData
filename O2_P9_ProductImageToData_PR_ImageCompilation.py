
###Extract images from +300 brand folders
import pandas as pd
import os, shutil

#Load the list of Main Sheet folder Names
MainFileName =pd.read_csv("//192.168.2.32/Group/Data Team/Brand_Update_Location/5_R_Brand_Reference_Files/Brands_Prefix.csv")
Brand_Folder_List = MainFileName[MainFileName.category_brand_name !='SalesData']["Brand_Folder_Name"]

#For each Brand_Folder_List item, go to brand folder and extract images
#Copy All images to xyz location
for i in range(0,len(Brand_Folder_List)):
    
    Brand = Brand_Folder_List.iloc[i]
    ImageFolder = "images--"+Brand
    print(Brand)

    BrandFolderLocation = "//192.168.2.32/GoogleDrive/Completed Magento Uploads (v 1.0)/" + Brand
    os.chdir(BrandFolderLocation)

    if os.path.exists(ImageFolder) == True:
        ImagePath = BrandFolderLocation+"/images--"+Brand
        os.chdir(ImagePath)
        ImageNames = os.listdir(ImagePath)
        
        for m in range(0,len(ImageNames)):
            fileName = ImageNames[m]
            Extention = fileName.split('.')[-1]
            if any([Extention == "jpg", Extention == "png", Extention == "jpeg"]):
                HomePath = ImagePath+"/"+fileName
                DestPat = "Z:/O2_P9_S1_ImageData/O2_P9_S1_ImageData_PR_ImageFiles/"+fileName
                shutil.copy2(HomePath, DestPat)
            else:
                print("**SKIPPED: "+ fileName + " from " + Brand)

    else:
        print("No Image Folder in: "+Brand)
