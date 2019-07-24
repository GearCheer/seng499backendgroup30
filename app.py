import sys
import os
from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from base64 import decodestring
from keras.preprocessing import image
import numpy as np
import base64
import wc
app = Flask(__name__)
CORS(app)

# Install flask, flask_cors
UPLOAD_FOLDER = 'waste_images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['CORS_HEADERS'] = 'Content-Type'
BIN_LABELS = ['Cardboard', 'Compost', 'Food', 'Glass', 'Landfill', 'Plastic, metal, and paper containers', 'Recycle', 'Soft Plastics', 'Styrofoam']
global classifier

def _valid_request(request):
    return request.content_type == 'multipart/form-data' and 'picture' in request.files

def _valid_picture_file(picture_file):
    valid = False
    if picture_file:
        filename = picture_file.filename

        if '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS:
            valid = True

    return valid

@app.route('/get_type', methods=['POST'])
def get_type():
    ''' takes base64 uploaded file from front-end
        decodes it and saves it as a png to be read for classification
    '''

    if not _valid_request:
        return make_response("Invalid request.", 400)

    picture_file = request.files['picture']

    if _valid_picture_file(picture_file):
        # Save image
        filename = secure_filename(picture_file.filename)
        filepath = 'waste_images/{}'.format(filename)  
        data = picture_file.read()

        # being sent as base64 image, don't ask me why, 
        # the ionic app camera extension automatically does 
        # base64 encoding/
        #imgdata = base64.b64decode(data)
        imgdata = data

        # I assume you have a way of picking unique filenames
        # uses filename from front end

        # Save image
        with open(filepath, 'wb') as file:
            file.write(imgdata)

        #redirect to classifier
        bin = _get_bin_from_image(filepath)

        # picture_file.save()
        json = {'type': bin}

        return make_response(jsonify(json), 200)

    else:
        return make_response("Invalid request", 400)

def _get_bin_from_image(filepath):
    picture = _load_and_format_image(filepath)

    classifier_output = classifier.classify(picture)
    return _get_type_from_classifier(classifier_output)

def _load_and_format_image(filepath):
    picture = image.load_img(filepath, target_size=(384, 512, 3))
    picture_tensor = image.img_to_array(picture)
    picture_tensor = np.expand_dims(picture_tensor, axis=0)

    return picture_tensor

def _get_type_from_classifier(classifier_output):
    index = np.argmax(classifier_output)
    return sorted(BIN_LABELS)[index]

if __name__ == "__main__":
    classifier = wc.Classifier(model_path="models/model.h5")
    app.run()