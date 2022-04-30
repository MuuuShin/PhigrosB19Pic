import json
import re
import data

# -*- coding: UTF-8 -*-

cur = data.conn.cursor()
overflow = 5
inputFilePath = "..\\content\\temp_input\\decode.json"
outputFilePath = "..\\content\\save\\"


# 基本数据处理，分离player
def processOrigin(origin):
    #print(origin)
    # print(re.search('{"player":(.+)}', origin).group(1))
    originJson = json.loads(re.search('{"player":(.+)}', origin).group(1))
    # print(originJson)
    return originJson


# 数据处理，去除杂项只留info
def processInfo(info):
    ansInfo = []
    for i in range(len(info)):
        songName = info[i]['songid']
        if not (re.match('[0-3]key.+', songName) or re.match('.+(IN|EZ|LE|AT|HD)', songName) or re.search('TextOpened',
                                                                                                          songName)):
            ansInfo.append(info[i])
    return ansInfo


# 数据处理，将songid与type拆分
def processData(data):
    ansData = []
    for k in range(len(data)):
        # print(data[k]['songid'])
        pp0 = re.search('(.+\..+\..+)\..+\.(.+)', data[k]['songid'])
        songName = pp0.group(1)
        songType = pp0.group(2)
        ansData.append((songName, songType, data[k]['info']))
    # print(ansData)
    return ansData


# 获取玩家名字
def getName(originList):
    for i in range(len(originList)):
        if originList[i]['songid'] == 'playerID':
            user = originList[i]['info']
            return user


# 找定数
def findDiff(songName, songType):
    if songType == 'SP' or songType == 'Legacy':
        return -1
    sql = 'select difficulty' + songType + ' from songs2nex WHERE id=\'' + songName + '\''
    cur.execute(sql)
    try:
        res = cur.fetchone()[0]
    except:
        return -1
    else:
        if not (res is None):
            return res
        else:
            return -1


# 找位置(b19)
def findPos(posList, pos):
    for k in range(len(posList)):
        if posList[k]['rating'] < pos:
            return k


# a1
def findA1(playerData):
    ans = 0.0
    pos = 0
    apNum = 0
    apNumIN = 0
    for k in range(len(playerData)):
        if playerData[k][2]['a'] == 100:
            apNum += 1
            if (playerData[k][1] == 'IN'):
                apNumIN += 1
            rr = findDiff(playerData[k][0], playerData[k][1])
            if float(rr) > ans:
                ans = float(rr)
                pos = k
                # res=pow(((playerData[k][3]['a']-55)/45),2)*findDiff(playerData[k][0], playerData[k][1])
    # print((playerData[pos][0], playerData[pos][1], ans), apNum, apNumIN)
    if ans != 0.0:
        return [{'songId': playerData[pos][0], 'songType': playerData[pos][1], 'rating': ans}, apNum, apNumIN]  # ansA1
    else:
        return [-1, -1, -1]  # noA1


# b19+overflow,可调数量
def findB19(playerData):
    ansList = []
    for k in range(len(playerData)):
        diff = findDiff(playerData[k][0], playerData[k][1])
        acc = playerData[k][2]['a']
        if acc < 70:
            continue
        # print(playerData[k][0], playerData[k][1],diff)
        if diff == -1:
            continue
        res = pow(((acc - 55) / 45), 2) * float(diff)
        # ansList.sort()
        if len(ansList) == 0:
            ansList.append(
                {'songId': playerData[k][0], 'songType': playerData[k][1], 'songDiff': diff, 'rating': res, 'acc': acc})
        elif ansList[-1]['rating'] < res:
            ansList.insert(findPos(ansList, res),
                           {'songId': playerData[k][0], 'songType': playerData[k][1], 'songDiff': diff, 'rating': res,
                            'acc': acc})
            if len(ansList) > 20 + overflow:
                ansList.pop()
        elif len(ansList) < 20 + overflow:
            ansList.append(
                {'songId': playerData[k][0], 'songType': playerData[k][1], 'songDiff': diff, 'rating': res, 'acc': acc})
    if len(ansList) < 20 + overflow:
        ansList.append(-1)
    return ansList


# rks计算
def calcRks(a1, b19list):
    ans = a1[0]['rating']
    # print(ans)
    for j in range(19):
        ans += b19list[j]['rating']
        # print(b19list[j])
    return ans / 20


# 保存玩家信息
def saveInfo(playerInfo, userName):
    fo = open(outputFilePath + userName + "Info.json", "w+", encoding='utf-8')
    fo.write(json.dumps(playerInfo))
    fo.close()


# 保存玩家数据
def saveData(a1, b19List, userName, rks):
    fo = open(outputFilePath + userName + "Data.json", "w+", encoding='utf-8')
    strq = '{"userName":"' + userName + '","rks":' + str(rks) + ',"apNum":' + json.dumps(
        a1[1]) + ',"apNumIN":' + json.dumps(
        a1[2]) + ',"a1":' + json.dumps(a1[0]) + ',"b23":' + json.dumps(b19List) + '}'
    # print(strq)
    fo.write(strq)
    fo.close()


# 主程序
def main():
    fi = open(inputFilePath, "r", encoding='utf-8')
    originStr = fi.read()
    originList = processOrigin(originStr)
    userName = getName(originList)
    playerInfo = []
    playerData = []
    for i in range(len(originList)):
        if re.match('.+\..+\..+\..+\..+', originList[i]['songid']):
            playerData.append(originList[i])
        else:
            playerInfo.append(originList[i])
    # print(playerData)
    playerInfo = processInfo(playerInfo)
    # print(playerInfo)
    playerData = processData(playerData)
    a1 = findA1(playerData)
    b19List = findB19(playerData)
    rks = calcRks(a1, b19List)
    # print(rks, a1, b19List)
    saveInfo(playerInfo, userName)
    saveData(a1, b19List, userName, rks)
    cur.close()
    return userName
