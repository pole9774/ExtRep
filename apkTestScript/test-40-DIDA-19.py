import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '127.0.0.1:7555'
desired_caps['appPackage'] = 'cn.ticktick.task'
desired_caps['appActivity'] = 'com.ticktick.task.activity.MeTaskActivity'
desired_caps['newCommandTimeout'] = '1000'
desired_caps['noReset'] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

# home page
try:

    el1 = driver.find_elements_by_class_name('android.widget.ImageButton')[0]
    el1.click()
    time.sleep(3)

    el2 = driver.find_elements_by_id('cn.ticktick.task:id/settings_btn')[0]
    el2.click()
    time.sleep(3)

    el3 = driver.find_element_by_android_uiautomator('new UiSelector().text("General")')
    el3.click()
    time.sleep(3)

    el4 = driver.find_element_by_android_uiautomator('new UiSelector().text("Template")')
    el4.click()

finally:
    time.sleep(5)
    driver.quit()

'''
{
  "platformName": "Android",
  "platformVersion": "6.0.1",
  "deviceName": "127.0.0.1:7555",
  "noReset": true,
  "appPackage": "cn.ticktick.task",
  "appActivity": "com.ticktick.task.activity.MeTaskActivity"
}
'''
