from flask import Flask
from flask_restful import Api, Resource, reqparse
from models.gompertz import Gompertz

APP = Flask(__name__)
API = Api(APP)

API.add_resource(Gompertz, '/predict')

if __name__ == '__main__':
    APP.run(debug=True, port='1080')