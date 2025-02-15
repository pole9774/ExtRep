# -*- coding:utf8 -*-
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

# 每次测试要恢复初始状态
# 系统ofm第一个文件夹中存放init01.png和init02.csv(第二个文件格式随意)
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\OIFileManager v2.0.5.apk'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps['waitActivity'] = 'org.openintents.filemanager.FileManagerActivity'

# 注:
# 1、首次启动，手工跳过前导页
# 2、为进行测试，在第一个文件夹下，放入了两个文件，其中第一个为图片
# 3、执行完成后，将文件恢复初始状态以便下次执行

# test case18: 当前文件夹，更多选项，捐赠
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)

el = driver.find_elements_by_id("org.openintents.filemanager:id/primary_info")[0]
el.click()
time.sleep(1)

el = driver.find_element_by_class_name("android.widget.ImageButton")
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/title")[0]
el.click()
time.sleep(1)

time.sleep(5)

driver.back()

time.sleep(2)
driver.quit()
