import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '192.168.1.119:18888'
desired_caps['appPackage'] = 'com.faltenreich.diaguard'
desired_caps['appActivity'] = 'com.faltenreich.diaguard.feature.navigation.MainActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

try:
    el1 = driver.find_element_by_accessibility_id('Open Navigator')
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('com.faltenreich.diaguard:id/design_menu_item_text')[5]
    el2.click()
    time.sleep(3)

    el3 = driver.find_elements_by_id('com.faltenreich.diaguard:id/date_range_button')[0]
    el3.click()
    time.sleep(3)

    el4 = driver.find_elements_by_id('com.faltenreich.diaguard:id/mtrl_picker_header_toggle')[0]
    el4.click()
    time.sleep(3)

    el5 = driver.find_elements_by_id('com.faltenreich.diaguard:id/confirm_button')[0]
    el5.click()

finally:
    time.sleep(3)
    driver.quit()
