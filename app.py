import os
import sys
import DesDecodeToJson, JsonToInfo, InfoToPic
import data


def main():
    if int(sys.argv[2]) == 1:
        if DesDecodeToJson.main(FileName) == -100:
            print("Error-100:未找到存档文件，可能是未上传或命名错误。上传请联系暮心(1248440677)")
            return -100
        userName = JsonToInfo.main()
        PicPath = InfoToPic.main(userName)
    else:
        PicPath = InfoToPic.main(FileName)
    print(os.path.abspath(PicPath))
    data.conn.close()
    return 0


FileName = sys.argv[1]
main()
