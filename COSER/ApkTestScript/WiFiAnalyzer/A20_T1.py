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

# test case 1: 主界面
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(5)

# in-state
el = driver.find_elements_by_id('com.vrem.wifianalyzer:id/ssid')[1]
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/action_scanner')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/action_scanner')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/action_filter')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSSIDtext')
el.send_keys('111111111111111')
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterWifiBand2')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterWifiBand2')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterStrength0')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterStrength1')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterStrength2')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterStrength3')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterStrength4')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterStrength0')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterStrength1')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterStrength2')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterStrength3')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterStrength4')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSecurityNone')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSecurityWPS')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSecurityWEP')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSecurityWPA')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSecurityWPA2')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSecurityNone')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSecurityWPS')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSecurityWEP')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSecurityWPA')
el.click()
time.sleep(1)

el = driver.find_element_by_id('com.vrem.wifianalyzer:id/filterSecurityWPA2')
el.click()
time.sleep(1)

el = driver.find_element_by_id('android:id/button1')
el.click()
time.sleep(1)
