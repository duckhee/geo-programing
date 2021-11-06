#-*- coding: utf-8 -*-

from .GaussianModel import GaussianModel


class ModelFactory:
    # init function
    def __init__(self, model_name="gaussian"):
        self.model_name = model_name;
        
    def __new__(cls):
        print('new factory')
        return super().__new__(cls)

    # model create function
    def createModel(self, model_name=""):
        name = ""
        if(model_name == "" or model_name == None):
            name = self.model_name;
        # gaussian model return
        if(name.lower() == "gaussian"):
            return GaussianModel();

