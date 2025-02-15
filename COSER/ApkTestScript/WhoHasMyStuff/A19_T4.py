# -*- coding:utf8 -*-
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
# todo 是不是说可以不要删掉备份文件？
# 先进去点一下backup，让备份文件处于已经存在的状态，然后关闭再进入，是否恢复点击否
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['unicodeKeyboard'] = True
desired_caps['resetKeyboard'] = True
desired_caps['newCommandTimeout'] = 10000
desired_caps['noReset'] = True

desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\WhoHasMyStuff v1.0.38.apk'

time.sleep(5)

# test case4: 进入第一项，mark as returned
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)

el = driver.find_elements_by_id("de.freewarepoint.whohasmystuff:id/toptext")[0]
el.click()
time.sleep(2)

el = driver.find_element_by_id("de.freewarepoint.whohasmystuff:id/returned_button")
el.click()
time.sleep(2)

driver.quit()
