from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
import keras
import io
import numpy as np
import keras
from keras.utils import img_to_array
from keras.utils import load_img
from keras.layers import Dense, Flatten
from keras.models import Model
from keras.applications.vgg19 import VGG19
import keras 
from keras.applications.resnet import ResNet50
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg19 import VGG19, preprocess_input ,decode_predictions
from keras.layers import Dropout
from keras.regularizers import l2
import base64


app = Flask(__name__)

model = tf.keras.models.load_model('bestmodel4.h5', compile=False)

@app.route('/predict', methods=['POST'])
def predict():
    try:

        image = request.files['image'].read()
        img = Image.open(io.BytesIO(image)).convert('RGB')
        img = img.resize((256, 256))
        i= img_to_array(img)
        im= preprocess_input(i)
        img=np.expand_dims(im , axis= 0)

        classes = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight',
                   'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
                   'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
                   'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
                   'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']

        prediction = model.predict(img)[0]
        class_idx = np.argmax(prediction)
        class_name = classes[class_idx]
        # create a base64 encoded string of the image
        img_base64 = base64.b64encode(image).decode('utf-8')
        response = {'disease': class_name, 'image': img_base64}
        
        return jsonify(response)
    
    except Exception as e:
        response = {'error': str(e)}
        return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

