import time

from appium import webdriver

# todo 进入的时候提前选好一个network，需要多等待一会

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\openBikeSharing v1.10.0.apk'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps["appWaitActivity"] = "be.brunoparmentier.openbikesharing.app.*"

# test case 1: 主界面
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(5)

# el = driver.find_element_by_id('be.brunoparmentier.openbikesharing.app:id/action_refresh')
# el.click()
# time.sleep(1)

el = driver.find_element_by_id('be.brunoparmentier.openbikesharing.app:id/action_map')
el.click()
time.sleep(1)
