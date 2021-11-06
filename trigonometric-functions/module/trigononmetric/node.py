from matplotlib.pyplot import grid
import numpy as np

"""
grid를 위한 class
"""
class model_world:
    def __init__(self):
        self.initValue = {}
        speed = input("속도를 입력하세요:")
        x = input("전체 크기의 x 값을 입력 하세요:")
        y = input("전체 크기의 y 값을 입력 하세요:")
        gridX = input("나눌 X 좌표의 크기를 입력하세요:")
        gridY = input("나눌 Y 좌표의 크기를 입력하세요:")
        self.initValue = {"x":int(x), "y":int(y), "gridX":int(gridX), "gridY":int(gridY), "speed":int(speed)}

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
        pos = {}
        for index, gridPos in enumerate(self.grid):
            x = (gridPos["pos"][0][0] + gridPos["pos"][3][0]) / 2
            y = (gridPos["pos"][0][1] + gridPos["pos"][3][1]) / 2
            pos = {"index":gridPos["index"], "middlePos":[x, y]}
            self.middlePos.append(pos)
        
        return self.middlePos


"""
수신기 좌표를 만들어주기 위한 class
"""
# 수신기 좌표를 가지고 있는 class            
class receiver:
    def __init__(self):
        pass

    def makeReceiverPoint(self):
        receiverX = input("수신기의 x 좌표를 입력하세요:")
        receiverY = input("수신기의 y 좌표를 입력하세요:")