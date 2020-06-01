# Product Image To Data
## Broad Problem Case:
When base data for a product is missing or unavailable but an image is present, we would like to have the ability to determine general product information based only on available image(s).
## Why is problem interesting?
In the world of ecommerce, product images are essential in order to sell products. Hence, the accessibility to quality images may be more than organized and structured product data. Often, depending on the online vender, the same image may be accompanied with inconsistent product data. Or, product data may be missing entirely. 

<br> In other cases, a single manufacturer may produce a product for multiple other companies. The only distinction between the products could be the brands logo, different color themes or how the product is presented in the images. This presents a challenge to mass categorization of products especially when no other product data is available, except an image.

<br> Here, I will define product data as the minimum data needed by the vender to shipping and organize products on their website. In order to ship a product, knowing the length, width, height and weight is necessary. To organize products, we would need to know what the product is, or Part Type, and possibly its brand.
## Data Source
In order to address this problem, I will focused on automotive parts as use case due to immense application and specificity of products. 
<br> Data was provided by an unnamed source which had a large repository of images available along with their pre-labeled brands, part type and dimensions.
### Example Input
accel-0576.jpg (https://github.com/abulhassansheikh/O2_P9_ProductImageToData/blob/master/SampleImageData/accel-0576.jpg)
### Example Output
- Brand: Accel
- Part Type: Spark Plug
- Length: 4.9 to 5.0 inch
- Width: 3.6 to 4.1 inch
- Height: 1.1 to 2.2 inch
- Weight: 0.25 to 1.0 lb
### Data Collection
Two sets of data were collected: image details and product images. Image detail data was acquired by iterating across +200 brand folders to identify appropriate .csv files and retrieved the brand, part type, weight, height, length and width for each image. The product images were acquired by iterating over the image folder nested within each brand folder and images were copy-pasted with the “shutil” package to a target folder. Cumulatively, +300,000 unique product images were pooled from all brand folders. 

## Project Approach 
This problem required the use of both classification and regression supervised algorithms. For the classification component, an image needs to be classified into a part type that fits the function of the product. Then, once we know if the part type, we require regression analysis to predict the dimentions of the product. 

<br> To tackle the classification problem, a convolutional neural network was constructed with three layers with the following nodes in each layer: 1000, 3000, 2584, respectively. In order to improve the generalization of the model, both 20% random dropout layers and L2 regularization were used. This yielded a approximate 25% accuracy in the model. 

<br> Secondly, for each part type's width, length and height, its mean and standard deviation were determined. This max and min dimensional range for each part type group were used as features in a multivariable regression model to predict the weight. An additional feature of Volume was also included. As expected, there was multicollinearity present since the dimension and weight of products would be expected to be correlated. 

<br> In conjunction with the CNN and regression model, for a given image, we can both classify and predict it's dimensions and weight. 

## Project API
Once both models had been integrated the back-end of a simple html website using the Flask framework, Heroku was used to deploy the application. 

<br> To make the process of deployment easy, pipenv was used to capture and freeze the required package versions. 

<br> The live application can be viewed at: https://imagetodata.herokuapp.com. 
<br> All that is required to use the application is to upload an image and press submit. Doing this will provide the end user predicted data on the image.
