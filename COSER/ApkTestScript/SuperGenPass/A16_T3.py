# -*- coding:utf8 -*-
import time

from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = False
desired_caps['appPackage'] = 'info.staticfree.SuperGenPass'
desired_caps['appActivity'] = 'info.staticfree.SuperGenPass.Super_Gen_Pass'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)

# test case3: 更多选项，settings 过时了
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)

el = driver.find_elements_by_class_name("android.widget.ImageButton")[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/title")[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/checkbox")[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/checkbox")[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/checkbox")[2]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/checkbox")[3]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/title")[3]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/title")[5]
el.click()
time.sleep(1)

el = driver.find_element_by_id("android:id/edit")
el.send_keys("3")

el = driver.find_element_by_id("android:id/button1")
el.click()
time.sleep(1)

driver.back()
