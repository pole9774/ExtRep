import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'org.connectbot'
desired_caps['appActivity'] = 'org.connectbot.HostListActivity'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
# desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\ConnectBot v1.9.8.apk'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
# desired_caps["appWaitActivity"] = "org.connectbot.*"

# test case 1: More options ---- Sort by name
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(5)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('android:id/title')[0]
el.click()
time.sleep(1)
