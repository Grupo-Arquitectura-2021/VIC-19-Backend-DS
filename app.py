from flask import Flask
from flask_restful import Api, Resource, reqparse
from models.gompertz import Gompertz

APP = Flask(__name__)
API = Api(APP)

API.add_resource(Gompertz, '/gompertz')

if __name__ == '__main__':
    APP.run( port='1080',host="0.0.0.0",debug=True)