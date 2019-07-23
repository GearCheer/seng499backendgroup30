import sys
import os
from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from base64 import decodestring
import base64
import wc
app = Flask(__name__)
CORS(app)

# Install flask, flask_cors
#UPLOAD_FOLDER = 'C:\Users\Andrew\Desktop\University\SENG499\seng499backendgroup30\waste_images'
UPLOAD_FOLDER = 'waste_images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['CORS_HEADERS'] = 'Content-Type'
classifier = None


def valid_request(request):
    valid = False

    if request.content_type == 'multipart/form-data':
        if 'picture' in request.files:
            valid = True

    return valid

def valid_picture_file(picture_file):
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

    if not valid_request:
        return make_response("Invalid request.", 400)

    picture_file = request.files['picture']

    if valid_picture_file(picture_file):
        # Save image
        filename = secure_filename(picture_file.filename)
        data = picture_file.read()
        # being sent as base64 image, don't ask me why, 
        # the ionic app camera extension automatically does 
        # base64 encoding/
        imgdata = base64.b64decode(data)
        filename = 'waste_images/{}'.format(filename)  
        # I assume you have a way of picking unique filenames
        # uses filename from front end
        with open(filename, 'wb') as f:
            f.write(imgdata)
        # picture_file.save()
        # redirect to application
        bin = get_bin_from_image(picture_file)
        json = {'type': bin}
        return make_response(jsonify(json), 200)

    else:
        return make_response("Invalid request", 400)

def get_bin_from_image(picture):
    print(classifier.classify(picture))
    #return classifier.classify(picture)

if __name__ == "__main__":
    classifier = wc.Classifier(model_path="models/model.h5")
    app.run()