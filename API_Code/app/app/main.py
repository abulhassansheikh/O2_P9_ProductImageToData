from PIL import Image #pip install --upgrade Pillow if not work
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import tensorflow as tf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        file = request.files['query_img']
        TargetSize = 28
        
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/"  + file.filename
        img.save(uploaded_img_path)

        #Process new image into numpy array
        img_new = img
        img_new.thumbnail((TargetSize, TargetSize))
        img_new = img.convert('L') # convert image to black and white
        x_center = int((TargetSize - img_new.size[0]) / 2)
        y_center = int((TargetSize - img_new.size[1]) / 2)

        WhiteBox = Image.new(mode = "L", 
                         size = (TargetSize, TargetSize), 
                         color = 255)
        WhiteBox.paste(img_new, (x_center ,y_center))
        img_new = WhiteBox
        
        uploaded_img_path_new = "static/uploaded/" + "new_" +file.filename
        img_new.save(uploaded_img_path_new)
        
        #Create numpy array from 28 by 28 image
        New_Image = (np.array(img_new)/255.0)
        New_Image = (np.expand_dims(New_Image,0))
        
        #Load Models
        PTRef = (pd.read_csv(r"Pt2LWH_model.csv",encoding='utf-8'))
        PTnumref = (pd.read_csv(r"PTref.csv",encoding='utf-8')) 
        Dim_model = (pd.read_csv(r"Dim_model.csv",encoding='utf-8')) 
        PTmodel_filename = "C:/Users/abulh/Sync/Documents/O2_P9_ProductImageToData/API_Code/API_Dev/StartingPoint_1/imagemodel.h5"
        PTmodel = tf.keras.models.load_model(PTmodel_filename)
        
        
        #Determine Part type        
        PTpredictVal = np.argmax(PTmodel.predict(New_Image)) 
        ptpred = PTnumref[PTnumref["PT_num"]==PTpredictVal].reset_index().iloc[0,2]
                
        #Determine L/W/H
        dim = (PTRef[PTRef["part_type"]==ptpred][['height_max', 'height_min',
                                             'length_max', 'length_min',
                                             'width_max', 'width_min']])
        
        
        uHeight = dim.iloc[0,0]
        bHeight = dim.iloc[0,1]
        uLength = dim.iloc[0,2]
        bLength = dim.iloc[0,3]
        uWidth = dim.iloc[0,4]
        bWidth = dim.iloc[0,5]
        uVolume = uHeight * uLength * uWidth
        bVolume = bHeight * bLength * bWidth
    
        #Run Weight Model
        intercept = Dim_model.coef[0]
        heightCoef = Dim_model.coef[1]
        lenghtCoef = Dim_model.coef[2]
        widthCoef = Dim_model.coef[3]
        volumeCoef = Dim_model.coef[4]
        
        uWeight = (intercept + heightCoef*uHeight + lenghtCoef*uLength + 
                              widthCoef*uWidth + volumeCoef*uVolume) 
        bWeight = (intercept + heightCoef*bHeight + lenghtCoef*bLength + 
                              widthCoef*bWidth + volumeCoef*bVolume)

        #output results
        value1 = file.filename
        value2 = ptpred
        value3 = round(uHeight, 2).astype(str)+" to "+round(bHeight, 2).astype(str)
        value4 = round(uLength, 2).astype(str)+" to "+round(bLength, 2).astype(str)
        value5 = round(uWidth, 2).astype(str)+" to "+round(bWidth, 2).astype(str)
        value6 = round(uWeight, 2).astype(str)+" to "+round(bWeight, 2).astype(str)
        
        Data = [["File Name", value1],
                ["Part Type", value2],
                ["Height Range", value3], 
                ["Length Range", value4],
                ["Width Range", value5],
                ["Weight Range", value6]]

        return render_template('index.html',
                               query_path=uploaded_img_path_new,
                               Data=Data)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
#