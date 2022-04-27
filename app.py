import os
import sys
import DesDecodeToJson, JsonToInfo, InfoToPic

FileName = sys.argv[1]


def main():
    if sys.argv[2] == 1:
        if DesDecodeToJson.main(FileName) == -100:
            print("Error-100:未找到存档文件，可能是未上传或命名错误。上传请联系暮心(1248440677)")
            return -100
        userName = JsonToInfo.main()
    else:
        userName = FileName
    PicPath = InfoToPic.main(userName)
    print(os.path.abspath(PicPath))
    return 0


main()
