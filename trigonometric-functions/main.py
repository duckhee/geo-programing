# -*- coding: utf-8 -*-
import numpy as np
import math
import sys
import os
# 그래프를 그리기 위한 import
import matplotlib.pyplot as plt

# 탄성파 파일을 읽기 위한 import
import segyio
import obspy
from obspy.io.segy.segy import _read_segy
from obspy.signal.trigger import classic_sta_lta, plot_trigger
from astropy.io import ascii
from obspy import read

# custom module
import module.trigononmetric.node as customModule


"""
#수신기 거리 = 속도 X 시간
빗변 길이의 제곱은 나머지 두변의 길이의 제곱과 같다.
----------------------------------------
수신기 간격 입력

수신기 처음 위치, 끝 위치(x, y)

z - 고정 값
----------------------------------------
고장점은 중점 = 속도 x sgy 시간 
----------------------------------------

그리드 중점 c 값 구하는 것

실제 c' 값을 입력 받아서 비교 - 차이 값 (적은 값 리스트로 보여주기)
* 실제 c' 값이 수신기 좌표가 입력 값으로 필요하지 않을까?
 - real world 에서 virtual world 로 전환하기 위해서 필요한 것인가?

-------------------------------------------------------------
* 추후 진행할 상황 데이터를 구조화하여, 정리 pandas module을 이용해서 
data set 만들기
-------------------------------------------------------------
TODO
그리드의 중점이 아니라 원형의 접점을 이용해서 가장 많은 접점을 가지는 원의 
중점 좌표와 값을 구하기

-------------------------------------------------------------



error - 실제 입력된 값과 구한 값의 차이

-------------------------------------------------------------
"""

    


#sample_file = os.getcwd() + "\\sampleData\\Ulsan_2015\\RefMS16161442_IEEESEGY.sgy"
# os.path.join(os.getcwd(), "sampleData", "Ulsan_2015", "RefMS16161442_IEEESEGY.sgy")
# save_basePath = os.getcwd() + "\\saved\\"

# grid 생성 입력을 받아서 처리
world = customModule.model_world()
# receiver 위치 만들기
receiver_pos = customModule.receiver()
# get receiver position
re_positions = receiver_pos.getReceiverPos()
# get array list
get_receiverPostionArray = receiver_pos.getReceiverPosArray()
#print("get receiver pos : {}".format(re_positions))
#receiver_pos.saveFile()
# grid로 나누어진 값을 가져오기
get_gridSet = world.makeGrid()

#print("grid list : {}".format(get_gridSet))

# grid의 중점 값 리스트
get_middlePos = world.getGridMiddlePos()
# get array list
get_gridList = world.getArrayMiddlePos()
# world.saveFile(fileName="test.csv")
#print("get middle pos : {}".format(get_middlePos))

# data change numpy array
np_grid = np.array(get_gridList)
np_receiverPos = np.array(get_receiverPostionArray)

# save data pos
savedAll = []


# operation get middle pos and receiver scalar x, y
for i in range(0, len(np_grid)):
    for j in range(0, len(np_receiverPos)):
        savedDic = {}
        dotValue = np_receiverPos[j].dot(np_grid[i])
        savedDic = {"middlePos":np_grid[i], "receiverPos":np_receiverPos[j], "length":dotValue}
        savedAll.append(savedDic)

sortData = sorted(savedAll, key=lambda data: data["length"])
#sortData = set(sortData)
print("result saved all : {}".format(sortData))


baseDir = os.path.join(os.getcwd(), "result")

try:
    if not os.path.exists(baseDir):
        os.mkdir(baseDir)
except Exception:
    print("make result folder make error")
output_file = os.path.join(baseDir, "result.csv")
with open(output_file, 'w', newline="\n") as filewriter:
    filewriter.write("middlePos\treceiverPos\terror\r\n")
    for i in range(0, len(sortData)):
        filewriter.write(str(sortData[i]["middlePos"]))
        filewriter.write("\t")
        filewriter.write(str(sortData[i]["receiverPos"]))
        filewriter.write("\t")
        filewriter.write(str(sortData[i]["length"]))
        filewriter.write('\n')

