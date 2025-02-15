import time

from appium import webdriver

# todo 进入的时候提前选好一个network，需要多等待一会

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\openBikeSharing v1.0.apk'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps["appWaitActivity"] = "be.brunoparmentier.openbikesharing.app.*"

# test case 5: More options---About
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(5)

el = driver.find_element_by_accessibility_id('More options')
el.click()
time.sleep(1)

el = driver.find_elements_by_id('android:id/title')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('android:id/title')[3]
el.click()
time.sleep(1)

el = driver.find_element_by_id('android:id/button1')
el.click()
time.sleep(1)

