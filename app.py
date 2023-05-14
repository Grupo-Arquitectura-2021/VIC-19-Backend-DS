from flask import Flask
from flask_restful import Api, Resource, reqparse
from models.dermistmodelvgg16 import Vgg16

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
APP = Flask(__name__)
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
API = Api(APP)

API.add_resource(Vgg16, '/vgg')

if __name__ == '__main__':
    APP.run( port='1080',host="localhost",debug=True)