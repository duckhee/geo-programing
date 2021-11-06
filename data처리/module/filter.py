# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np

"""
이동 평균 계사하는 class
"""


class moveAvg:
    def __init__(self, avgMax=5):
        # 이동 평균을 할 갯수 입력 값 저장
        self.avgMax = 5
        # 이동 평균 값을 저장하기 위한 list
        self.avgData = []
        return
    
    # 이동 평균의 값을 저장한 리스트 초기화
    def cleanSet(self):
        self.avgData.clear();
    
    # file save make folder
    def saveFile(self, fileName, folderName="./filteringDone"):
        basePath = os.getcwd()
        folderPath = basePath + folderName
        # folder make
        try:
            if not os.path.exists(folderPath):
                os.mkdir(folderPath)
        
        except OSError:
            print("make folder error")
        
        # save file data 

        

        
