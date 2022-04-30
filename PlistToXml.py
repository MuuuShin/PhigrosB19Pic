import os
import plistlib
import DesDecodeToJson

inputFilePathOrigin = "..\\content\\input\\"


def main(userName):
    inputFilePath = inputFilePathOrigin + userName + ".plist"
    if not os.path.exists(inputFilePath):
        return -100
    aaa = plistlib.load(open(inputFilePath, "rb"))
    # print(aaa)
    # print(list(dict.items(aaa))[0])
    try:
        originList = list(dict.items(aaa))
    except:
        os.remove(inputFilePath)
        return -10
    #print(originList)
    coodde = DesDecodeToJson.process(originList)
    return coodde
