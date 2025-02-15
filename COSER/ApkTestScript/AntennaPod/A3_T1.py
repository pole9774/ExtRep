import time

from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['newCommandTimeout'] = 8000
desired_caps['noReset'] = True
desired_caps['app'] = 'D:\\lab\\ExtRep\\ASEJour\\app\\AntennaPod v2.5.0.apk'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps["appWaitActivity"] = "de.danoeh.antennapod.*"

# 侧边栏在第一次启动应用时会自动打开,所以启动之前先打开应用关一下侧边栏,并且把主页面开queue 230415现在不用了，应该是之前改好了

# test case 1: 侧边栏点击queue
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(10)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/txtvTitle')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('Open menu')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/txtvTitle')[0]
el.click()
time.sleep(1)

el = driver.find_element_by_id('de.danoeh.antennapod:id/queue_lock')
el.click()
time.sleep(1)

el = driver.find_element_by_id('android:id/button2')
el.click()
time.sleep(1)

el = driver.find_element_by_id('de.danoeh.antennapod:id/queue_lock')
el.click()
time.sleep(1)

el = driver.find_element_by_id('android:id/button1')
el.click()
time.sleep(1)

el = driver.find_element_by_id('de.danoeh.antennapod:id/refresh_item')
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[0]
el.click()
time.sleep(1)

el = driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text')
el.send_keys('test')
time.sleep(1)

driver.press_keycode(66)
time.sleep(1)

el = driver.find_elements_by_accessibility_id('Collapse')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[2]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[2]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[3]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[3]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[4]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[5]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[5]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[1]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[6]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[5]
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[2]
el.click()
time.sleep(1)

el = driver.find_element_by_id('android:id/button2')
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[2]
el.click()
time.sleep(1)

el = driver.find_element_by_id('android:id/button1')
el.click()
time.sleep(1)

el = driver.find_elements_by_accessibility_id('More options')[0]
el.click()
time.sleep(1)

el = driver.find_elements_by_id('de.danoeh.antennapod:id/title')[3]
el.click()
time.sleep(1)

driver.back()
time.sleep(1)

driver.quit()
