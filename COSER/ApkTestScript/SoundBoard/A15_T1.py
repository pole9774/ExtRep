# -*- coding:utf8 -*-
import time

from appium import webdriver

desired_caps = {}
desired_caps['appium-version'] = '1.7.2'
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\SoundBoard v0.92.apk'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True

# test case1: 添加
# 注意：这里我自己添加了一个音频文件在第一个文件夹中
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(5)

el = driver.find_element_by_id("de.meonwax.soundboard:id/action_new")
el.click()

el = driver.find_element_by_id("android:id/button2")
el.click()

el = driver.find_element_by_id("de.meonwax.soundboard:id/action_new")
el.click()

el = driver.find_elements_by_id("de.meonwax.soundboard:id/directory_entry_name")[0]
el.click()

el = driver.find_elements_by_id("de.meonwax.soundboard:id/directory_entry_name")[1]
el.click()
