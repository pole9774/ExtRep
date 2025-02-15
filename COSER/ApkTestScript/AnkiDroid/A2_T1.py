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

# test case1: 主页面，添加按钮，创建牌组，并在新创建的牌组中添加一张卡片
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)

time.sleep(2)

el = driver.find_element_by_id("com.ichi2.anki:id/fab_expand_menu_button")
el.click()
time.sleep(1)

el = driver.find_element_by_id("com.ichi2.anki:id/add_deck_action")
el.click()
time.sleep(1)

# in-state
el = driver.find_element_by_id("com.ichi2.anki:id/buttonDefaultNegative")
el.click()
time.sleep(1)

el = driver.find_element_by_id("com.ichi2.anki:id/fab_expand_menu_button")
el.click()
time.sleep(1)

el = driver.find_element_by_id("com.ichi2.anki:id/add_deck_action")
el.click()
time.sleep(1)

el = driver.find_elements_by_class_name("android.widget.EditText")[0]
el.clear()

el = driver.find_elements_by_class_name("android.widget.EditText")[0]
el.send_keys("Test")

# in-state
el = driver.find_element_by_id("com.ichi2.anki:id/buttonDefaultPositive")
el.click()
time.sleep(1)

time.sleep(2)

el = driver.find_element_by_id("com.ichi2.anki:id/fab_expand_menu_button")
el.click()
time.sleep(1)

# csh修改
el = driver.find_element_by_id("com.ichi2.anki:id/add_note_action")
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/text1")[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/text1")[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("com.ichi2.anki:id/id_note_editText")[0]
el.clear()

el = driver.find_elements_by_id("com.ichi2.anki:id/id_note_editText")[0]
el.clear()

el = driver.find_elements_by_id("com.ichi2.anki:id/id_note_editText")[0]
el.send_keys("TestFront")

el = driver.find_elements_by_id("com.ichi2.anki:id/id_note_editText")[1]
el.clear()

el = driver.find_elements_by_id("com.ichi2.anki:id/id_note_editText")[1]
el.send_keys("TestBack")

el = driver.find_element_by_id("com.ichi2.anki:id/action_save")
el.click()
time.sleep(1)

el = driver.find_elements_by_class_name("android.widget.ImageButton")[0]
el.click()
time.sleep(1)

driver.quit()