# -*- coding: utf-8 -*-

import os
import glob
import sys
import pandas as pd
import numpy as np

"""
이동 평균 계산하는 class
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
    def saveFile(self, fileName, folderName="./filterMoveAVG"):
        basePath = os.getcwd()
        # make folder path
        folderPath = os.path.join(basePath, folderName)
        # folder make
        try:
            if not os.path.exists(folderPath):
                os.mkdir(folderPath)
        
        except OSError:
            print("make folder error")
        
        # save file data
        baseName = "filtermoveAVG_" 
        savedName = baseName + fileName


        

        
