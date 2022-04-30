import base64
import json
import os
import re
import pyDes
import data

# -*- coding: UTF-8 -*-

inputFilePathOrigin = "..\\content\\input\\"
outputFilePathOrigin = "..\\content\\temp_input\\"
outputFilePath1 = outputFilePathOrigin + "decode.json"
outputFilePath2 = outputFilePathOrigin + "err.txt"


# 预处理，先传入存档路径
def main(userName):
    # os.makedirs(path)
    inputFilePath = inputFilePathOrigin + userName + ".xml"
    if not os.path.exists(inputFilePath):
        return -100
    coode = main1(inputFilePath)
    if coode == -10:
        os.remove(inputFilePath)
        return -10


"""
:param base64_str: 要解密的base64字符串
:return: 解密后的字符串
"""


def base64ToDesToStr(base64_str):
    base64_str = base64_str.replace("%2B", "+")
    base64_str = base64_str.replace("%2F", "/")
    base64_str = base64_str.replace("%3D", "=")
    """ 初始化一个des对象，参数是秘钥，加密方式，偏移， 填充方式 """
    des_obj = pyDes.des(data.DES_SECRET_KEY, pyDes.CBC, data.DES_SECRET_KEY, padmode=pyDes.PAD_PKCS5)
    """ 把base64先解成byte后再解密 """
    base64_types = base64_str.encode()
    secret_bytes = base64.b64decode(base64_types)
    # print(binascii.b2a_hex(secret_bytes))
    """ 用对象的decrypt方法解密 """
    s = des_obj.decrypt(secret_bytes)
    # print(s.decode("utf-16"))
    return s.decode("utf-16")


def main1(inputFilePath):
    fi = open(inputFilePath, "r", encoding='utf-8')
    originStr = fi.read()
    # print("当前文件位置 : ", position)
    fi.close()
    originList = re.findall('<string name="(.+)">(.+)</string>', originStr)
    # print(originList)
    process(originList)


def process(originList):
    fo2 = open(outputFilePath2, "w+", encoding='utf-8')
    songName = []
    info = []
    ans = []
    err = []
    j = 0
    for i in range(len(originList) - 1):
        # if (i + 1) % 10 == 0:
        # print("execute:" + str(i + 1) + "/" + str(len(originList)))
        try:
            cs = base64ToDesToStr(originList[i][0])
            di = base64ToDesToStr(originList[i][1])
        except:
            fo2.write(str(i) + "\n")
            fo2.write(originList[i][0] + "\n")
            fo2.write(str(originList[i][1]) + "\n")
            err.append("\"line\":" + str(i) + ", \"" + originList[i][0] + "\":\"" + str(originList[i][1]) + "\"")
        else:
            try:
                di2 = json.loads(di)
            except:
                di = "\"" + di + "\""
            # print(f"line {i}:", originList[i][0], originList[i][1])
            fo2.write(str(i) + "\n")
            fo2.write(str(cs) + "\n")
            fo2.write(di + "\n")
            songName.append(cs)
            info.append(di)
            ans.append("{\"songid\":\"" + str(songName[j]) + "\",\"info\":" + str(info[j]) + "}")
            j = j + 1
    if not ans:
        return -10
    find = 0
    for j in range(len(songName)):
        if songName[j] == 'playerID':
            find = 1
            break
    if find == 0:
        fname = open(outputFilePathOrigin + "NeedName.txt", "r", encoding='utf-8')
        tempPlayer = fname.read()
        fname.close()
        fname = open(outputFilePathOrigin + "NeedName.txt", "w+", encoding='utf-8')
        fname.write(
            re.match('(player)(.+)', tempPlayer).group(1) + str(1 + int(re.match('(player)(.+)', tempPlayer).group(2))))
        fname.close()
        ans.append("{\"songid\":\"" + 'playerID' + "\",\"info\":\"" + tempPlayer + "\"}")
    fo2.write('[%s]' % ', '.join(map(str, err)))
    fo2.close()
    fo1 = open(outputFilePath1, "w+", encoding='utf-8')
    strInfo = '[%s]' % ', '.join(map(str, ans))
    fo1.write("{\"player\":" + strInfo.replace("//", "\/\/").replace("\n", "\\n").replace("\r", "\\n") + "}")
    fo1.close()
    return 0
