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

# test case5: 生成密码并复制
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)

time.sleep(10)

el = driver.find_element_by_id("info.staticfree.SuperGenPass:id/domain_edit")
el.send_keys("192.168.1.100")

el = driver.find_element_by_id("info.staticfree.SuperGenPass:id/password_edit")
el.send_keys("000000")

el = driver.find_element_by_id("info.staticfree.SuperGenPass:id/show_gen_password")
el.click()
time.sleep(1)

el = driver.find_element_by_id("info.staticfree.SuperGenPass:id/show_gen_password")
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/title")[1]
el.click()
time.sleep(1)

el = driver.find_element_by_id("android:id/text1")
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/text1")[2]
el.click()
time.sleep(1)

el = driver.find_elements_by_id("android:id/title")[0]
el.click()
time.sleep(1)

el = driver.find_element_by_id("info.staticfree.SuperGenPass:id/copy")
el.click()
time.sleep(1)

driver.quit()
