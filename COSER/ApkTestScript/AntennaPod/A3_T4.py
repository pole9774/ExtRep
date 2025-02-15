import time

from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\AntennaPod v2.1.3.apk'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps["appWaitActivity"] = "de.danoeh.antennapod.*"

# 侧边栏在第一次启动应用时会自动打开,所以启动之前先打开应用关一下侧边栏,并且把主页面开queue 230415现在不用了，应该是之前改好了

# test case 4: 侧边栏点击Downloads
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(5)

el = driver.find_elements_by_accessibility_id('Open menu')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/txtvTitle')[3]
el.click()
time.sleep(1)

el = driver.find_element_by_id('de.danoeh.antennapod:id/refresh_item')
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('Running')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('Completed')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('Log')[0]
el.click()
time.sleep(1)

driver.quit()

