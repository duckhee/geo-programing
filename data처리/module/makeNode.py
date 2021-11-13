# -*- coding: utf-8 -*-

import csv
import sys
import os
import numpy as np
import pandas as pd

class  makeNode:
    def __init__(self, filePath=""):
        self.filePath = ""
        self.initData = {}
        
    
    def makeNodeStructure(self, filePath=""):
        path = "";
        if(filePath == "" or filePath == None):
            path = self.filePath
        else:
            path = filePath
        datas = []
        init = {}
        print("read file path : {}".format(path))
        with open(path, mode="r", newline="\n", encoding="utf-8") as fileReader:
            csvReader = csv.reader(fileReader, delimiter="\t")
            # 사용하지 않을 세줄 삭제를 위한 읽기
            fileReader.readline().strip()
            fileReader.readline().strip()
            # 수신기 간의 간격 가져오기
            node_distance_interval = fileReader.readline().strip()
            init["distance_interval"] = node_distance_interval
            # 수신기 갯수를 가져오기 4번째 라인
            node_number = int(fileReader.readline().strip())
            init["node_number"] = node_number
            # 전체 수신기 갯수 출력
            print("read node number ::: {}".format(node_number))
            # 파일 한줄씩 읽기
            for index, row_list in enumerate(csvReader):
                # print("{} testing :::{}".format(index, str(row_list[0].strip())))
                # 전체 거리를 가져오기 위한 if문
                if index == (int(node_number) - 1):
                    all_range = float(row_list[0].split()[1])
                    print("get all range ::: {}".format(all_range))
                    init["max_distance"] = all_range
                # 전체 데이터 갯수를 가져오기 위한 if문
                if(index == (int(node_number) + 1)):
                    data_number = row_list[0].split()[0]
                    print("current line : {}, all data number is {}".format(index+5, data_number))
                    init["all_data"] = data_number
                # 데이터를 가져오기 위한 if 문
                if(index >= (int(node_number)+2)):
                    # 데이터 분리
                    data = row_list[0].split();
                    # 송신 노드의 번호 
                    send_node = {"x":int(data[0]), "y":int(data[1])}
                    # print("get voltage send node : {}".format(send_node))
                    # 수신 노드의 번호
                    reception_node = {"x":int(data[2]), "y":int(data[3])}
                    # print("get reception voltage node : {}".format(reception_node))
                    # 송신 전압 과 수신 전압
                    voltage = {"voltageMeasurement":float(data[4]), "registeMeasurment":float(data[5])}
                    # print("get voltage send and reception : {}".format(voltage))
                    data = {"send_node_pos":send_node, "reception_node_pos":reception_node, "voltage_data":voltage}
                    # data 구조화 리스트 삽입
                    datas.append(data)
                    
        self.initData = {"init_val":init, "datas":datas}
        return {"init_val":init, "datas":datas};

    # pandas data set change
    def dataFrame(self):
        getSendNodePos = []
        getRecNodePos = []
        getVoltages = []
        getReceiveVoltage = []
        
        for index, data in enumerate(self.initData["datas"]):
            getVoltages.append(data['voltage_data']['voltageMeasurement'])
            getReceiveVoltage.append(data['voltage_data']['registeMeasurment'])
            getSendNodePos.append(data['send_node_pos'])
            getRecNodePos.append(data["reception_node_pos"])
        
        pandasData = pd.DataFrame({"voltageMeasurement":getVoltages, "registeMeasurment":getReceiveVoltage, "sendNodePos":getSendNodePos, "receiveNodePos":getRecNodePos})
        self.pandasData = pandasData;
        return pandasData;
