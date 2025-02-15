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

# test case 4: Hosts主界面
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(15)

# in-state
el = driver.find_elements_by_id('org.jak_linux.dns66:id/bottom_navigation_item_title')[1]
el.click()
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/host_enabled')
el.click()
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/host_enabled')
el.click()
time.sleep(1)

# in-state
el = driver.find_elements_by_id('org.jak_linux.dns66:id/item_title')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/title')[0]
el.clear()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/title')[0]
el.send_keys('test')
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/action_save')
el.click()
time.sleep(10)

# in-state
el = driver.find_element_by_id('org.jak_linux.dns66:id/host_add')
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/title')[0]
el.send_keys('test')
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/location')
el.send_keys('test')
time.sleep(1)

el = driver.find_element_by_id('android:id/text1')
el.click()
time.sleep(1)

el = driver.find_elements_by_id('android:id/text1')[0]
el.click()
time.sleep(1)

el = driver.find_element_by_id('android:id/text1')
el.click()
time.sleep(1)

el = driver.find_elements_by_id('android:id/text1')[1]
el.click()
time.sleep(1)

el = driver.find_element_by_id('android:id/text1')
el.click()
time.sleep(1)

el = driver.find_elements_by_id('android:id/text1')[2]
el.click()
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/action_save')
el.click()
time.sleep(1)
