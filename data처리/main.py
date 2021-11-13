# -*- coding: utf-8 -*-
"""
자료 처리 
-------------------------------------------------------------
전처리 과정에서 이동 평균으로 특정 값 제거
-------------------------------------------------------------
이동 평균 값을 5개의 데이터로 구하고 이동 평균 값으로 그래프를 
그리고, 거기에서 너무 많이 벗어난 값을 제거(기본 제거 차이 - 10, 추후 - 표준 편차를 구해서 0.5 넘는 것 삭제)
-------------------------------------------------------------

-------------------------------------------------------------
1. 전처리 과정 - 필터링
이동 평균으로 필터링하여, 데이터 자동으로 처리

-------------------------------------------------------------
2. 필터링된 데이터를 가지고, 학습 진행
 - 목적은 필터링을 학습을 통해 자동화 하기 위해서 트랜드 확인을 위한 것?
-------------------------------------------------------------

"""
import numpy as np
import pandas as pd
import sys
import csv 
import os

from module.makeNode import makeNode
from module.filter import moveAvg


def moveAvg():
    return

#input_file = sys.argv[1]
basePath = os.getcwd()
sampmle_file = basePath + "\\sampleData\\20180101.a2d"
re_sample_file = basePath + "\\sampleData\\re20180101.a2d"
# 수신기 갯수
node_number = 0
# 수신기가 최대 거리
all_range = 0
# 수신기간의 간격  interval
node_distance_interval = 0
# data number
data_number = 0
datas = []
# 파일 경로를 넣어주기
newNode = makeNode()

# file의 경로를 가지고 데이터 structure 생성
getFirstData = newNode.makeNodeStructure(sampmle_file)

# 가져온 값 확인
print("read node number : {}, max distance : {}, node distance interval : {}, all data count : {}".format(node_number, all_range, node_distance_interval, data_number))

# print("mapping data ::: {}".format(datas))

#
#print("data is {}".format(getFirstData["datas"]))

# get send voltage list
getSendVoltage = []
# get receive voltage list
getReceiveVoltage = []
# get difference voltage 
getdifVoltage = []
# get change array list
for index, data in enumerate(getFirstData["datas"]):
    getSendVoltage.append(data['voltage_data']['send_voltage'])
    getReceiveVoltage.append(data['voltage_data']['reception_voltage'])
    getdifVoltage.append(data['voltage_data']['send_voltage'] - data['voltage_data']['reception_voltage'])


pandasData = pd.DataFrame({"voltageSend":getSendVoltage, "voltageReceive":getReceiveVoltage, "difVoltage":getdifVoltage})

getSendVoltage = np.array(getSendVoltage)
getReceiveVoltage = np.array(getReceiveVoltage)
getdifVoltage = np.array(getdifVoltage)
# print('voltage send : {}'.format(getSendVoltage))
# print("voltage send : {send} \nreceive voltage : {reception} \ndiffernce voltage : {dif}".format(send=getSendVoltage, reception=getReceiveVoltage, dif=getdifVoltage))

print("\nPandas Data Frame : {}".format(pandasData))