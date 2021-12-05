# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import pandas as pd

"""
grid를 위한 class
시간 값 입력 받기
"""
class model_world:
    def __init__(self):
        self.initValue = {}
        print("----------------------------------------------------------------------------")
        
        speed = input("속도를 입력하세요:")
        x = input("전체 크기의 x 값을 입력 하세요:")
        y = input("전체 크기의 y 값을 입력 하세요:")
#        z = input("전체 크기의 z(h) 값을 입력 하세요:")

        gridX = input("나눌 X 좌표의 크기를 입력하세요:")
        gridY = input("나눌 Y 좌표의 크기를 입력하세요:")
        self.initValue = {"x":int(x), "y":int(y), "gridX":int(gridX), "gridY":int(gridY), "speed":int(speed)}
        print("----------------------------------------------------------------------------")

    def getSpeed(self):
        return self.initValue["speed"];    

    def makeGrid(self):
        maxX = self.initValue["x"]
        maxY = self.initValue["y"]
        gridX = self.initValue["gridX"]
        gridY = self.initValue["gridY"]
        self.grid = []
        count = 0
        for i in range(0, maxX- 1):
            for j in range(0, maxY - 1):
                if(i % gridX == 0):
                    if(j % gridY == 0):
                        count += 1
                        self.grid.append({"index":count,"pos":[[i,  j], [i, j + gridY], [i + gridX, j], [i + gridX, j + gridY]]})
                        
        return self.grid;

    def getGrid(self):
        return self.grid;

    def getGridMiddlePos(self):
        total = len(self.grid)
        self.middlePos = []
        self.middlePosArray = []
        pos = {}
        for index, gridPos in enumerate(self.grid):
            x = (gridPos["pos"][0][0] + gridPos["pos"][3][0]) / 2
            y = (gridPos["pos"][0][1] + gridPos["pos"][3][1]) / 2
            pos = {"index":gridPos["index"], "middlePosX":x, "middlePosY":y}
            self.middlePos.append(pos)
            self.middlePosArray.append([x, y])
        # return middel position
        return self.middlePos


    def getArrayMiddlePos(self):
        return self.middlePosArray


    def saveMiddlePosFile(self, fileName="sample.csv", folderPath="sampleGridMiddlePos"):
        baseFolder = os.path.join(os.getcwd(), folderPath)
        try:
            if not os.path.exists(baseFolder):
                os.mkdir(baseFolder)
        except OSError:
            print("error occured make save folder path")

        # make pandas data frame 
        pdFrame = pd.DataFrame(self.middlePos)
        # make file name
        filePath = os.path.join(baseFolder, fileName)
        # save csv file
        pdFrame.to_csv(filePath, sep="\t", na_rep='NaN', index=False)


"""
수신기 좌표를 만들어주기 위한 class
[{index:, position:[x, y, z]}]
"""
# 수신기 좌표를 가지고 있는 class            
class receiver:
    def __init__(self):
        self.receiverPos = []
        self.receiverPosArray = []
        print("----------------------------------------------------------------------------")
        receiverX = input("수신기의 초기 x 좌표를 입력하세요:")
        receiverY = input("수신기의 초기 y 좌표를 입력하세요:")
        receiverZ = input("수신기의 z 값을 입력하세요:")
        receiverX_interval = input("수신기의 x 간격을 입력하세요:")
        receiverY_interval = input("수신기의 y 간격을 입력하세요:")
        receiverMaxX = input("수신기의 최대 x 값을 입력하세요:")
        receiverMaxY = input('수신기의 최대 y 값을 입력하세요:')
        print("----------------------------------------------------------------------------")
        # init pos value
        initX = float(receiverX)
        initY = float(receiverY)
        initZ = float(receiverZ)
        # save pos
        x = initX
        receiverX_interval = int(receiverX_interval)
        receiverY_interval = int(receiverY_interval)
        count = 1
        # make receiver position
        # x pos max
        for i in range(0, int(receiverMaxX)):
            y = initY
            # y pos max
            for j in range(0, int(receiverMaxY)):
                
                if y >= float(receiverMaxY):
                    break;
                
                # j 0, 1, 2, 3, 4, 5, 6 ....
                # initY * j * interval
                if j != 0:
                    y = float(initY) * (float(receiverY_interval) ** (j))
                
                if(initY <= float(receiverMaxY)):
                    pos = {"index":count, "posX":float(x), "posY":float(y), "posZ":float(initZ)}
                    self.receiverPos.append(pos)
                    # not save z position
                    self.receiverPosArray.append([float(x), float(y)])
                    # numbering
                    count += 1
            # x pos set
            # i 0, 1, 2, 3, 4, 5, 6 .....
            # initX * i * interval
            if i != 0:
                x = float(initX) * ( float(receiverX_interval)** (i))
            #
            if x > float(receiverMaxX):
                break;
            
            
        
    # return receiver position
    def getReceiverPos(self):
        if len(self.receiverPos) == 0:
            # make exception
            raise Exception("need to setting receiver class")
        # get receiver position
        return self.receiverPos

    def getReceiverPosArray(self):
        return self.receiverPosArray

    # save receiver position
    def saveFile(self, fileName="sample.csv", folderPath="sampleReceiverPos"):
        baseDir = os.path.join(os.getcwd(), folderPath)

        try:
            if not os.path.exists(baseDir):
                os.mkdir(baseDir)
            
        except OSError:
            print("save receiver folder make error")
        # save file name set
        fileName = os.path.join(baseDir, fileName)
        # make pandas data frame
        pdFrame = pd.DataFrame(self.receiverPos)
        pdFrame.to_csv(fileName, sep="\t", na_rep='NaN', index=False)

