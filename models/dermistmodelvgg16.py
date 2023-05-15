import numpy as np
from keras.applications.imagenet_utils import preprocess_input
import cv2
from flask_restful import Resource, request

class Vgg16(Resource):
  
  @staticmethod
  def post():
      try:
        from keras.models import load_model
        names = ['acne_atrofico','acne_comedogenico','acne_noduloquistico','acne_papulopustular','queratosis_pilaris']

        modelt = load_model("/home/pomaalvin/VIC-19-Backend-DS/models/vgg16_dermist.h5")
        #modelt = custom_vgg_model

        imaget_path = "/content/drive/MyDrive/TESTIMGDERMIST/acne_papulopustular/194papulopustular.png"
        imaget=cv2.resize(cv2.imdecode(np.frombuffer(request.files.get('image').read(), np.uint8), -1), (224, 224), interpolation = cv2.INTER_AREA)
        print(cv2.imdecode(np.frombuffer(request.files.get('image').read(), np.uint8), -1))
        print(imaget)
        xt = np.asarray(imaget)
        xt=preprocess_input(xt)
        xt = np.expand_dims(xt,axis=0)
        preds = modelt.predict(xt)

        ipreds = np.argsort(preds)[0]

      except RuntimeError:
          print("No se pudo lograr la proyeccion de datos")

      return [
              {
                "name":names[ipreds[ipreds.size-1]],
                "percentage": preds[0][ipreds[ipreds.size-1]]   
              },
              {
                "name":names[ipreds[ipreds.size-2]],
                "percentage": preds[0][ipreds[ipreds.size-2]]
              }, 
              {
                "name":names[ipreds[ipreds.size-3]],
                "percentage": preds[0][ipreds[ipreds.size-3]]  
              }
          ],200