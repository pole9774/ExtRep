import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'ryey.easer'
desired_caps['appActivity'] = 'ryey.easer.core.ui.MainActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

try:
    el1 = driver.find_element_by_accessibility_id('Open navigation drawer')
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('ryey.easer:id/design_menu_item_text')[0]
    el2.click()
    time.sleep(3)

    el3 = driver.find_element_by_accessibility_id('Open navigation drawer')
    el3.click()
    time.sleep(3)

    el4 = driver.find_elements_by_id('ryey.easer:id/design_menu_item_text')[0]
    el4.click()

finally:
    time.sleep(3)
    driver.quit()
