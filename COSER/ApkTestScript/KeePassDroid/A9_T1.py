# -*- coding:utf8 -*-
import os
import time

# import os
from appium import webdriver

# 记得每次要删除文件

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\KeePassDroid v2.2.0.9.apk'
desired_caps['appWaitActivity'] = 'com.keepassdroid.*'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True

# test case1: 开始页面,捐赠
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(5)

el = driver.find_element_by_id("com.android.keepass:id/menu_donate")
el.click()

time.sleep(5)

driver.back()

time.sleep(1)

driver.quit()