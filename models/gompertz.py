import pandas as pd
import datetime
import numpy as np
from flask_restful import Api, Resource, reqparse
from lmfit import Model
import json
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
class Gompertz(Resource):
    @staticmethod
    def post():
        parser = reqparse.request.data
        print(parser)
        body=json.loads(parser)
        sumC,sumR,sumD,sumV=0,0,0,0;
        dataC_normal=[]
        dataC=[]
        dataR=[]
        dataD=[]
        dataV=[] 
        dates=[]
        prim=datetime.datetime.strptime(body[0]["dateLocationCovid"],"%Y-%m-%d")
        primDate=datetime.datetime.timestamp(prim)
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
            dates.append((datetime.datetime.timestamp(auxDate)-primDate)/86400)
            dataC_normal.append(d["confirmedCases"])
    
        print(dates)
        print(dataC)
        print(np.exp(1))
        def fun(x,b,r,k):
            return np.exp((x-b)*r)/(1+((np.exp((x-b)*r)-1)/k))
        def funSol(x,b,r,k):
            return (r*k*k*np.exp(r*(x-b))-r*k*np.exp(r*(x-b)))/pow(k+np.exp(r*(x-b))-1,2)
        try:
            resC,var= (curve_fit(fun,dates,dataC,))
            resR,var1= (curve_fit(fun,dates,dataR))
            resD,var2= (curve_fit(fun,dates,dataD))
            resV,var3= (curve_fit(fun,dates,dataV))
            print(var3)
            out = {
                "function": "y=(r*k*k*np.exp(r*(x-b))-r*k*np.exp(r*(x-b)))/pow(k+np.exp(r*(x-b))-1,2)",
                'confirmedCases': {"b":resC[0],"r":resC[1],"k":resC[2]},
                'recuperated': {"b":resR[0],"r":resR[1],"k":resR[2]},
                'deathCases': {"b":resD[0],"r":resD[1],"k":resD[2]},
                'vaccinated': {"b":resV[0],"r":resV[1],"k":resV[2]}
                }
        except RuntimeError:
            print("No se pudo lograr la proyeccion de datos")

        return out,200
