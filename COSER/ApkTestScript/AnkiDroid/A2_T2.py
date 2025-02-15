# -*- coding:utf8 -*-
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

# 每次运行都要删除所有文件
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\AnkiDroid v2.13.0.apk'
desired_caps['noReset'] = True
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps["appWaitActivity"] = "com.ichi2.anki.DeckPicker"

# test case2: 主页面，添加按钮，获取共享牌组
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)

time.sleep(2)

el = driver.find_element_by_id("com.ichi2.anki:id/fab_expand_menu_button")
el.click()
time.sleep(1)
# csh修改
time.sleep(2)

el = driver.find_elements_by_class_name("android.widget.ImageButton")[2]
el.click()
time.sleep(1)

time.sleep(2)

driver.back()

time.sleep(2)

driver.quit()