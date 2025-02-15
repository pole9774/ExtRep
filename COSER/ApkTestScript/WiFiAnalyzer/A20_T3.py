import time

from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\WiFiAnalyzer v2.1.2.apk'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps["appWaitActivity"] = "com.vrem.wifianalyzer.*"

# test case 3: SideBar ---- Channel Rating
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(5)

el = driver.find_element_by_accessibility_id('Open navigation drawer')
el.click()
time.sleep(1)

el = driver.find_elements_by_id('com.vrem.wifianalyzer:id/design_menu_item_text')[1]
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/action_scanner')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/action_scanner')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/action_wifi_band')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/action_wifi_band')
el.click()
time.sleep(1)