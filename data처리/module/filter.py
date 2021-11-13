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
        # 데이터 값을 저장
        self.data = []
        # 이동 평균의 값을 구한 위치 저장하는 값
        self.index = 0
        return
    
    # 이동 평균의 값을 저장한 리스트 초기화
    def cleanSet(self):
        self.avgData.clear();
        self.data.clear();

    # 데이터 형태를 구조화 하는 함수
    def dataSetting(self, datas):
        pass

    # 이동 평균 구하기
    def getAllMoveAvg(self, datas):
        max = len(datas)
        # 초기화 진행
        self.avgData.clear()
        self.data.clear()
        moveAvgData = []
        # temp buffer
        temp = 0
        for index, data in enumerate(datas):
            if index <= self.avgMax:
                # 데이터 값 확인을 위한 저장
                self.data.append(data)
                # 평균을 구하기 위한 최소값이 되기 전까지 평균 값을 이용
                temp += data
                moveAvgData.append(temp / index)
                # 위치를 저장하기위한 index 값 저장
                self.index = index
            else:
                # 이동 평균 값을 구하는 공식
                tempMoveAvg = self.data[index - 5:]
                moveAvgData.append(tempMoveAvg / self.avgMax)
        # 이동 평균 값 저장
        self.avgData = moveAvgData
        return moveAvgData
    
    # 이동평균을 구하는 함수
    def getMoveAvg(self, lastValue):
        
        pass
    
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


        

        
