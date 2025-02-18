from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
from PIL import Image
app = Flask(__name__)
model = tf.keras.models.load_model("wheat_disease_sa.h5")
class_labels = ['Wheat___Healthy', 'Wheat___Yellow_Rust', 'Wheat___Brown_Rust']

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('prediction.html', error='No file uploaded')
        file = request.files['file']
        if file.filename == '':
            return render_template('prediction.html', error='No file selected')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        prediction = model.predict(img_array)
        predicted_class = class_labels[np.argmax(prediction)]
        
        return render_template('prediction.html', prediction=predicted_class, img_path=filepath)
    
    return render_template('prediction.html')

@app.route('/resource')
def resource():
    return render_template('resource.html')

if __name__ == '__main__':
    app.run(debug=True)