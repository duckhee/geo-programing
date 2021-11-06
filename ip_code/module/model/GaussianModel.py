# -*- coding: utf-8 -*-

import numpy as np
import math
import pandas as pd
import seaborn as sns
from scipy.stats import beta, norm
from numpy import histogram
import pylab

class GaussianModel:
    def __init__(self, saveFile=".\\gaussianModelLearing.txt"):
        self.saveFile = saveFile
        pass

    def __new__(cls):
        print('new model')
        return super().__new__(cls)

    @property
    def saveFile(self, saveFile):
        self.saveFile = saveFile
    
    @property
    def saveFile(self):
        return self.saveFile

    def gaussian_random(self, min_val = np.log10(10), max_val = np.log10(100), amount = 50):
        mu = min_val + ((max_val - min_val) / 2)
        sigma = abs(mu / 3)
        s = np.random.normal(mu, sigma, amount)
        return s
    
    def gaussian_random_2(self, min_val, max_val, amount, mulitplier):
        mu = min_val + ((max_val - min_val) / 2)
        sigma = abs(mu * mulitplier)
        s = np.random.normal(mu, sigma, amount)
        return s
    
    def gaussian_random_3(self, a, b, min_val, max_val, amount):
        dist = beta(a, b)
        result = min_val + dist.rvs(size=amount) * (max_val - min_val)
        return result
    
    def plot_gaussian_random(self, s, x_axis= 'log Rho_b'):
        ax = sns.distplot(s)
        ax.set(xlabel=x_axis)
        return ax