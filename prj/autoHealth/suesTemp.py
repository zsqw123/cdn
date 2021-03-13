import sys
import time
import random
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Test():
    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()


def log(s: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]\t{s}")


if __name__ == '__main__':
    person = {
        "name": sys.argv[1],  # 其实这里你可以填你自己的, 但别上传git
        "pwd": sys.argv[2],  # 其实这里你可以填你自己的, 但别上传git
    }
    test = Test()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    test.driver = webdriver.Chrome(
        options=options, executable_path=chromedriver)
    # test.driver = webdriver.Chrome()
    test.driver.get("https://web-vpn.sues.edu.cn/")
    test.driver.find_element(By.ID, "username").send_keys(person["name"])
    test.driver.find_element(By.ID, "password").send_keys(person["pwd"])
    test.driver.find_element(By.ID, "passbutton").click()
    test.vars = {}
    test.vars["window_handles"] = test.driver.window_handles
    test.driver.find_element(
        By.CSS_SELECTOR, "#group-4 > .layui-col-xs12:nth-child(2) p:nth-child(1)").click()
    log("Login Success! "+person["name"])
    test.vars["win4613"] = test.wait_for_window(2000)
    test.driver.switch_to.window(test.vars["win4613"])
    test.driver.find_element(
        By.CSS_SELECTOR, ".input-group > .form-control").click()
    temp = str(round(random.uniform(36.1, 36.7), 1))
    test.driver.find_element(
        By.CSS_SELECTOR, ".input-group > .form-control").send_keys(temp)
    test.driver.find_element(By.ID, "post").click()
    test.driver.find_element(By.LINK_TEXT, "确定").click()
    log("Report Success! "+temp)
