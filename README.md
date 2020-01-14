# Product Image To Data
## Broad Problem Case:
When base data for a product is missing or unavailable but an image is present, we would like to have the ability to determine general product information based only on available image(s).
## Why is problem interesting?
In the world of ecommerce, product images are essential in order to sell products. Hence, the accessibility to quality images may be more than organized and structured product data. Often, depending on the online vender, the same image may be accompanied with inconsistent product data. Or, product data may be missing entirely. 
In other cases, a single manufacturer may produce a product for multiple other companies. The only distinction between the products could be the brands logo, different color themes or how the product is presented in the images. This presents a challenge to mass categorization of products especially when no other product data is available, except an image.
Here, I will define product data as the minimum data needed by the vender to shipping and organize products on their website. In order to ship a product, knowing the length, width, height and weight is necessary. To organize products, we would need to know what the product is, or Part Type, and possibly its brand.
## Data Source
In order to address this problem, I will focused on automotive parts as use case due to immense application and specificity of products. 
Data was provided by an unnamed source which had a large repository of images available along with their pre-labeled brands, part type and dimensions.
### Example Input
accel-0576.jpg (https://github.com/abulhassansheikh/O2_P9_ProductImageToData/blob/master/SampleImageData/accel-0576.jpg)
### Example Output
Brand: Accel
Part Type: Spark Plug
Length: 4.9 inch
Width: 3.6 inch
Height: 1.1 inch
Weight: 0.25 lb
### Data Collection
Two sets of data were collected: image details and product images. Image detail data was acquired by iterating across +200 brand folders to identify appropriate .csv files and retrieved the brand, part type, weight, height, length and width for each image. The product images were acquired by iterating over the image folder nested within each brand folder and images were copy-pasted with the “shutil” package to a target folder. Cumulatively, +300,000 unique product images were pooled from all brand folders. 

## Project Approach 

## Project Strategy Log
December-2019
I can construct ML Model to classify the weight and also the L/W/H:
1. L/W/H -> Weight using multivariable regression
2. Part Type -> L/W/H by either using clustering or finding mean values

What broad classification can I use for Images that will also serve to reduce additional analysis?
- Brand: Some brands may only have a single PT, but I remember, there arn't that many brands, maybe less than 10
- PT is too specific since there are so many
- L1: Won't help narrow down brands/PT that much

I may need to create my own classifier with the following qualities:
- 1 = Products that are very unque and associated to a single brand/PT
- 2 = Products with that come from a single brand with unique multiple PT
- 3 = Products with single PT that multiple brands produce
- 4 = Multiple brands with multiple non-unique part types
### Model Strategy: 
Image -> Class 1/2/3

Class 1
1. Image + Class 1/2/3 -> Brand/PT
2. Image + Brand/PT -> Brand/PT
3. PT -> L/W/H
4. L/W/H -> Weight

Class 2
1. Image + Class 1/2/3 -> Brand
2. Image + Brand -> PT
3. PT -> L/W/H
4. L/W/H -> Weight

Class 3
1. Image + Class 1/2/3 -> PT
2. Image + PT -> Brand & PT -> L/W/H
3. L/W/H -> Weight

### Plan of Attack:
1. L/W/H -> Weight (Done)
2. PT -> L/W/H (Done)
3. Image -> Class 1/2/3 
(Basic, simple NN, Fully Connected, and add logical complexity, CNN is the end)
4. Image + Class 1/2/3 -> PT
5. Image + Class 1/2/3 -> Brand
6. Reevaluate to see if I can incorperate additional models or will need L1/L2/L3 data

January 2020
Class 1/2/3 resulted in too many values in each category. 
Idea: 
I can include a broader level classifier than part type by including L1/L2/L3 categories
This may add additional complexity, But if my results arn't accurate, I can include broader classifiers to improve accuracy.   

As a result, decided to use the L1/l2/L3 categories
L1 has 10 categories
L2 has 84
L3 has 276
When training images using base NN, I had 70% image classification accuracy


