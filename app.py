import os
import sys
import DesDecodeToJson, JsonToInfo, InfoToPic
import data


def main():
    if int(sys.argv[2]) == 1:
    # if 1 == 1:
        coodde = DesDecodeToJson.main(FileName)
        if coodde == -100:
            print("Error-100:未找到存档文件，可能是未上传或命名错误。请重试上传或/feedback进行反馈。")
            return -100
        if coodde == -10:
            print("Error-10:存档文件无效，请检查文件内容后重试上传或/feedback进行反馈。")
            return -10
        userName = JsonToInfo.main()
        PicPath = InfoToPic.main(userName)
    else:
        PicPath = InfoToPic.main(FileName)
    print(os.path.abspath(PicPath))
    data.conn.close()
    return 0


FileName = sys.argv[1]
# FileName = "Tyrant"
# print(sys.argv)
main()
