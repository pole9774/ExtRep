import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\Mgit v1.6.1.apk'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps["appWaitActivity"] = "com.manichord.mgit.*"

# 提前在文件系统导入一个github仓库，并且改名为A

# test case 2: Clone
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(15)

el = driver.find_element_by_id('com.manichord.mgit:id/action_new')
el.click()
time.sleep(1)

# in-state
el = driver.find_element_by_id('com.manichord.mgit:id/remoteURL')
el.send_keys('https://github.com/Vallxy/Vallxy.github.io.git')
time.sleep(1)

el = driver.find_element_by_id('com.manichord.mgit:id/localPath')
el.send_keys('Vallxy')
time.sleep(1)

# in-state
el = driver.find_element_by_id('android:id/button1')
el.click()
time.sleep(60)
