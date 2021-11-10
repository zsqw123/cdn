# way1 web-vpn

import math
import time
import random
import requests
from datetime import datetime, timedelta

from requests.sessions import Session
from bs4 import BeautifulSoup

rsa_e = "010001"
rsa_m = "008aed7e057fe8f14c73550b0e6467b023616ddc8fa91846d2613cdb7f7621e3cada4cd5d812d627af6b87727ade4e26d26208b7326815941492b2204c3167ab2d53df1e3a2c9153bdb7c8c2e968df97a5e7e01cc410f92c4c2c2fba529b3ee988ebc1fca99ff5119e036d732c368acf8beba01aa2fdafa45b21e4de4928d0d403"

origin = "https://web-vpn.sues.edu.cn"
vpnPath = "/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1"
tempPath = "/default/work/shgcd/jkxxcj"
tempMainPagePath = "/jkxxcj.jsp"

tempHeader = origin+vpnPath+tempPath
reportUrl = tempHeader+tempPath
debugMode = True


def timeGen():  # 上午下午, 2020-01-01, 2020-01-01 10:01
    time_utc = datetime.utcnow()
    time_peking = (time_utc + timedelta(hours=8))

    if time_peking.hour % 24 < 12:
        timeType = "上午"
    else:
        timeType = "下午"
    tjsj = time_peking.strftime("%Y-%m-%d")
    return timeType, tjsj


class Person:
    __lastData = {}

    def __init__(self, name: str, pwd: str):
        self.name = name
        self.pwd = pwd

    def __genRSAPasswd(self, passwd: str, e: str, m: str):
        # 别问我为啥rsa加密要这么写，傻逼cas
        # 参考https://www.cnblogs.com/himax/p/python_rsa_no_padding.html
        m = int.from_bytes(bytearray.fromhex(m), byteorder='big')
        e = int.from_bytes(bytearray.fromhex(e), byteorder='big')
        plaintext = passwd[::-1].encode("utf-8")
        input_nr = int.from_bytes(plaintext, byteorder='big')
        crypted_nr = pow(input_nr, e, m)
        keylength = math.ceil(m.bit_length() / 8)
        crypted_data = crypted_nr.to_bytes(keylength, byteorder='big')
        return crypted_data.hex()

    def __login(self) -> Session:
        sess = requests.Session()
        sess.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
            "origin": origin
        })
        res = sess.get(origin, verify=False)
        history = res.history
        realUrl = origin + history[len(history)-1].headers["location"]

        soup = BeautifulSoup(res.content, "lxml")
        res = sess.get(realUrl, verify=False)
        execution = soup.find("input", {"name": "execution"}).attrs["value"]
        postTarget = origin+soup.find("form")["action"]
        data = {
            "username": self.name,
            "password": self.__genRSAPasswd(self.pwd, rsa_e, rsa_m),
            "execution": execution,
            "encrypted": "true",
            "_eventId": "submit",
            "loginType": "1",
            "submit": "登 录"
        }

        res = sess.post(postTarget, data, verify=False)
        time.sleep(5)
        return sess

    def __queryNear(self, sess: Session) -> bool:  # 上次填写记录
        sess.headers.update({"referer": reportUrl})

        res = sess.post(
            url=tempHeader+"/com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryNear.biz.ext?vpn-12-o2-workflow.sues.edu.cn",
            verify=False
        )
        near_list = res.json()["resultData"]
        if len(near_list) == 0:
            return False
        else:
            self.__lastData = near_list[0]
            lower_json(self.__lastData)
            return True

    def __queryToday(self, sess: Session) -> bool:  # 是否已经填过
        sess.headers.update({"referer": reportUrl})
        ampm, tjsj = timeGen()
        queryTodayJson = {"params": {'sd': ampm, 'tjsj': tjsj}}

        res = sess.post(
            url=tempHeader+"/com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryToday.biz.ext?vpn-12-o2-workflow.sues.edu.cn",
            json=queryTodayJson, verify=False
        )
        today_list = res.json()["resultData"]
        if len(today_list) == 0:
            return False
        else:
            self.__lastData = today_list[0]
            lower_json(self.__lastData)
            self.__lastData.pop('id')
            return True

    def __submit(self, sess: Session) -> bool:  # 本次是否填报成功
        data = self.__lastData
        data["tw"] = str(round(random.uniform(36.3, 36.7), 1))
        updateData = {"params": data}
        log(data["gh"] + ",gentemp:" + data["tw"])
        finalRes = sess.post(tempHeader+"/com.sudytech.work.shgcd.jkxxcj.jkxxcj.saveOrUpdate.biz.ext?vpn-12-o2-workflow.sues.edu.cn",
                             json=updateData, verify=False)
        json = finalRes.json()

        if 'result' not in json:
            log("No result:"+str(json))
            return False
        if json['result']["success"]:
            return True
        else:
            log("Already reported or sever down:"+str(json))
            return False

    def report(self):  # 是否已经填过, 本次是否成功, 错误信息
        todayOk = False
        try:
            requests.packages.urllib3.disable_warnings()
            requests.adapters.DEFAULT_RETRIES = 40
            session = self.__login()
            todayOk = self.__queryToday(session)
            if not todayOk:
                if not self.__queryNear(session):
                    return False, False, "self.name"+"没填过"
            submitRes = self.__submit(session)
            return todayOk, submitRes, ""

        except Exception as e:
            if debugMode:
                raise e
            return todayOk, False, str(e)


def log(s: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]\t{s}")


def lower_json(json_info):
    if isinstance(json_info, dict):
        for key in list(json_info.keys()):
            if key.islower():
                lower_json(json_info[key])
            else:
                key_lower = key.lower()
                json_info[key_lower] = json_info[key]
                del json_info[key]
                lower_json(json_info[key_lower])

    elif isinstance(json_info, list):
        for item in json_info:
            lower_json(item)


if __name__ == '__main__':
    import sys

    person = Person(name=sys.argv[1], pwd=sys.argv[2])
    todayOk, res, err = person.report()
    log("res:"+str(todayOk or res)+",err:"+err)
