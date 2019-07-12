###From Every Mainsheet, extract the following columns: 
#Output = "sku", "attribute_set", "part_type_filter", "upc_code", "na_weight", "na_length", "na_width", "na_height", 
#Input = "image1", "image2", "image3", "image4"

#Load dplyr to manipulate data.frames
install.packages("dplyr")
library(dplyr)

#Load the list of Main Sheet folder Names
MainFileName =read.csv("//192.168.2.32/Group/Data Team/Brand_Update_Location/5_R_Brand_Reference_Files/Brands_Prefix.csv", header = TRUE)
Brand_Folder_List =data.frame(MainFileName %>% filter(Category.Brand.Name != "SalesData") %>% select(Brand_Folder_Name))


PooledMainData = data.frame()

pb <- txtProgressBar(min = 1, max = nrow(Brand_Folder_List), style = 3)
for (i in 1:nrow(Brand_Folder_List)){
	message(i, " ", Brand_Folder_List[i,])

	BrandFolderLocation = paste("//192.168.2.32/GoogleDrive/Completed Magento Uploads (v 1.0)/",as.character(Brand_Folder_List[i,]), sep = "", collapse = NULL)
	setwd(BrandFolderLocation)

	#Identify the Main--sheet and pull it
	x <- Sys.glob("main--*.csv")
	PulledMain=read.csv(x , header = TRUE)

	MainSubset <- subset(PulledMain, type=="simple", select=c("sku", "attribute_set", "part_type_filter", 
                           "upc_code", "na_weight", "na_length", "na_width", "na_height", 
                           "image1", "image2", "image3", "image4"))


	#Add Brand name and # of attribute sets to BrandAttributeSet df
	PooledMainData = rbind(PooledMainData ,MainSubset )

	setTxtProgressBar(pb, i)
}

#Seperate image1-4 data for ever sku
PooledMainData =  tbl_df(PooledMainData)
Image1_Data = PooledMainData %>% select(-c("image2", "image3", "image4")); names(Image1_Data)[9]="image_name"
Image2_Data = PooledMainData %>% select(-c("image1", "image3", "image4")); names(Image2_Data)[9]="image_name"
Image3_Data = PooledMainData %>% select(-c("image1", "image2", "image4")); names(Image3_Data)[9]="image_name"
Image4_Data = PooledMainData %>% select(-c("image1", "image2", "image3")); names(Image4_Data)[9]="image_name"

#Compile seperate image data into single df
ImageData = rbind(Image1_Data, Image2_Data)
ImageData = rbind(ImageData, Image3_Data)
ImageData = rbind(ImageData, Image4_Data)

#Extract different output data sets for every image
Image2PT = ImageData %>% filter(image_name != "", part_type_filter != "", part_type_filter != "Discontinued") %>% select(image_name, part_type_filter); names(Image2PT)[2]="part_type"
Image2Brand = ImageData %>% filter(image_name != "", attribute_set != "") %>% select(image_name, attribute_set); names(Image2Brand )[2]="brand"
Image2Sku = ImageData %>% filter(image_name != "", sku != "") %>% select(image_name, sku); names(Image2Sku )[2]="sku"
Image2UPC = ImageData %>% filter(image_name != "", upc_code != "") %>% select(image_name, upc_code); names(Image2UPC )[2]="upc"
Image2Weight = ImageData %>% filter(image_name != "", na_weight != "") %>% select(image_name, na_weight); names(Image2Weight )[2]="weight"
Image2Length = ImageData %>% filter(image_name != "", na_length != "") %>% select(image_name, na_length); names(Image2Length )[2]="length"
Image2Width = ImageData %>% filter(image_name != "", na_width != "") %>% select(image_name, na_width); names(Image2Width )[2]="width"
Image2Height = ImageData %>% filter(image_name != "", na_height != "") %>% select(image_name, na_height); names(Image2Height )[2]="height"

#Export Image2x files locally
FINAL(Image2Brand) #830,781 rows
FINAL(Image2Sku)	 #830,073 rows
FINAL(Image2UPC)	 #762,569 rows
FINAL(Image2PT)	 #827,241 rows
FINAL(Image2Width) #737,949 rows
FINAL(Image2Height)#737,487 rows
FINAL(Image2Weight)#764,985 rows
FINAL(Image2Length)#736,352 rows

##Move images from multiple brand folders to a single folder
#Check if image folder present in each brand folder and if absent, rename manually
#Every image folder should be called "



