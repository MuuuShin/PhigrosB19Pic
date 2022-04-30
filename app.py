import os
import sys
import DesDecodeToJson, JsonToInfo, InfoToPic
import PlistToXml
import data


def main():
    FileName = sys.argv[1]
    if int(sys.argv[2]) == 1:
        if sys.argv[3] == "xml":
            # if 1 == 1:
            coodde = DesDecodeToJson.main(FileName)
        elif sys.argv[3] == "plist":
            coodde = PlistToXml.main(FileName)
        else:
            print("Error-108:后缀名无效，请输入xml(安卓)或plist(IOS)。")
            return -108
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


'''
sys.argv = []
sys.argv.append("0")
sys.argv.append("Typ")
sys.argv.append(1)
sys.argv.append("plist")
'''
main()
