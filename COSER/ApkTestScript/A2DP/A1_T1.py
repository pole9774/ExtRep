# -*- coding:utf8 -*-
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\A2DP v2.13.0.4.apk'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True

# test case1: 更多选项，apps for Notifications
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)

time.sleep(2)

el = driver.find_elements_by_class_name("android.widget.ImageButton")[0]
el.click()
time.sleep(1)

# in-state
el = driver.find_elements_by_id("android:id/title")[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("a2dp.Vol:id/checkBox1")[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_class_name("android.widget.ImageButton")[0]
el.click()
time.sleep(1)

time.sleep(2)

el = driver.find_elements_by_class_name("android.widget.ImageButton")[0]
el.click()
time.sleep(1)

# in-state
el = driver.find_elements_by_id("android:id/title")[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('android:id/title')[0]
el.click()
time.sleep(1)

driver.back()

driver.quit()
