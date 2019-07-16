import sys
import os
from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

#UPLOAD_FOLDER = 'C:\Users\Andrew\Desktop\University\SENG499\seng499backendgroup30\waste_images'
UPLOAD_FOLDER = 'waste_images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['CORS_HEADERS'] = 'Content-Type'


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

    if not valid_request:
        return make_response("Invalid request.", 400)

    picture_file = request.files['picture']

    if valid_picture_file(picture_file):
        # Save image
        filename = secure_filename(picture_file.filename)
        picture_file.save('waste_images/{}'.format(filename))

        # redirect to application
        bin = get_bin_from_image(picture_file)
        json = {'type': bin}
        return make_response(jsonify(json), 200)

    else:
        return make_response("Invalid request", 400)

def get_bin_from_image(picture):
    return "Not implemented yet"
