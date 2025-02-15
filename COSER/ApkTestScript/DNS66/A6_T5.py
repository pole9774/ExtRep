import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

# 装好之后进去先长按启动然后关掉

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = False
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\DNS66 v0.6.8.apk'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps["appWaitActivity"] = "org.jak_linux.dns66.*"

# test case 5: Apps主界面
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(5)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/bottom_navigation_item_title')[2]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[2]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[2]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[3]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[3]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[4]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[4]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[5]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[5]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[6]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/checkbox')[6]
el.click()
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/switch_show_system_apps')
el.click()
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/switch_show_system_apps')
el.click()
time.sleep(1)
