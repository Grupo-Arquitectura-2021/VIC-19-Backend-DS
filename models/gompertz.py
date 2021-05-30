import pandas as pd
import datetime
import numpy as np
from flask_restful import Api, Resource, reqparse
from scipy.optimize import curve_fit
import json
class Gompertz(Resource):
    @staticmethod
    def post():
        parser = reqparse.request.data
        body=json.loads(parser)
        sumC,sumR,sumD,sumV=0,0,0,0;
        dataC=[]
        dataR=[]
        dataD=[]
        dataV=[]
        dates=[]
        for d in body:
            sumC+=d["confirmedCases"]
            sumR+=d["recuperated"]
            sumD+=d["deathCases"]
            sumV+=d["vaccinated"]
            dataC.append(sumC)
            dataR.append(sumR)
            dataD.append(sumD)
            dataV.append(sumV)
            auxDate=datetime.datetime.strptime(d["dateLocationCovid"],"%Y-%m-%d")
            dates.append(datetime.datetime.timestamp(auxDate))
        def fun(x,a,b,c):
            return a*np.exp(-b*np.exp(-c*x))
        resC,var= (curve_fit(fun,dates,dataC))
        resR,var= (curve_fit(fun,dates,dataR))
        resD,var= (curve_fit(fun,dates,dataD))
        resV,var= (curve_fit(fun,dates,dataV))
        
        out = {
            "function": "y=a*e^(-b*e^(-c*x))",
            'confirmedCases': {"a":resC[0],"b":resC[1],"c":resC[2]},
            'recuperated': {"a":resR[0],"b":resR[1],"c":resR[2]},
            'deathCases': {"a":resD[0],"b":resD[1],"c":resD[2]},
            'vaccinated': {"a":resV[0],"b":resV[1],"c":resV[2]}
            }
        return out,200
