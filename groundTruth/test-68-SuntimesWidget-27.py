import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '192.168.1.119:18888'
desired_caps['appPackage'] = 'com.forrestguice.suntimeswidget'
desired_caps['appActivity'] = 'com.forrestguice.suntimeswidget.SuntimesActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

try:
    el1 = driver.find_element_by_accessibility_id('More options')
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('com.forrestguice.suntimeswidget:id/title')[2]
    el2.click()
    time.sleep(3)

    el3 = driver.find_element_by_android_uiautomator('new UiSelector().text("Event")')
    el3.click()
    time.sleep(3)

    el4 = driver.find_elements_by_id('com.forrestguice.suntimeswidget:id/appwidget_schedalarm_mode')[0]
    el4.click()
    time.sleep(3)

    el5 = driver.find_elements_by_id('android:id/text1')[2]
    el5.click()

finally:
    time.sleep(3)
    driver.quit()
