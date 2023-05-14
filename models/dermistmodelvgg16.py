import numpy as np
from keras.applications.imagenet_utils import preprocess_input
import cv2
from flask_restful import Resource, request

class Vgg16(Resource):
  
  @staticmethod
  def post():
      
      print(request.files.get('image').read());
      return "ok",200
      try:
        from keras.models import load_model
        names = ['acne_atrofico','acne_comedogenico','acne_noduloquistico','acne_papulopustular','queratosis_pilaris']

        modelt = load_model("/content/vgg16_dermist.h5")
        #modelt = custom_vgg_model

        imaget_path = "/content/drive/MyDrive/TESTIMGDERMIST/acne_papulopustular/194papulopustular.png"
        imaget=cv2.resize(cv2.imread(imaget_path), (224, 224), interpolation = cv2.INTER_AREA)
        xt = np.asarray(imaget)
        xt=preprocess_input(xt)
        xt = np.expand_dims(xt,axis=0)
        preds = modelt.predict(xt)

        #print(preds)

        #print(names[np.argmax(preds)])

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