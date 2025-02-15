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
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\DNS66 v0.4.1.apk'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps["appWaitActivity"] = "org.jak_linux.dns66.*"

# test case 6: DNS Servers主界面
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(5)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/bottom_navigation_item_title')[3]
el.click()
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/dns_enabled')
el.click()
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/dns_enabled')
el.click()
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/dns_add')
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/title')[0]
el.send_keys('test')
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/location')[0]
el.send_keys('test')
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/state_switch')
el.click()
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/state_switch')
el.click()
time.sleep(1)

el = driver.find_element_by_id('org.jak_linux.dns66:id/action_save')
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/item_enabled')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/item_enabled')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/item_enabled')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/item_enabled')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/item_enabled')[2]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('org.jak_linux.dns66:id/item_enabled')[2]
el.click()
time.sleep(1)

driver.quit()