# Product Image To Data

## Data Collection
# Method
Two sets of data were collected: image details and product images. 
Image detail data was acquired by iterating across +200 brand folders to identify appropriate .csv files and retrieved the sku, brand, part type, UPC, weight, height, length and width for each image using the O2_P9_ProductImageToData_PR_ProductProfileDataCompilation.r script. 
The product images were acquired by iterating over the image folder nested within each brand folder and images were copy-pasted with the “shutil” package to a target folder using the O2_P9_ProductImageToData_PR_ImageCompilation.py script.

# Composition
Cumulatively, +300,000 unique product images were pooled from all brand folders. This set of images will be used to train the Product Image To Data engine.  



