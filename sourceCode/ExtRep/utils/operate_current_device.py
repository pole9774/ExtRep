import os
import time

from uiautomator import device


def open_app(package_name):
    cmd = 'adb shell monkey -p ' + package_name + ' -c android.intent.category.LAUNCHER 1'
    os.system(cmd)
    time.sleep(2)
    register_watchers()
    time.sleep(2)


def close_app(package_name):
    cmd = "adb shell am force-stop " + package_name
    os.system(cmd)


def reopen_app(package_name):
    """
    :return:
    """

    close_app(package_name)
    open_app(package_name)

    # device(text="Me").click()

    # trigger the listener
    device.watchers.run()


def action_click(node):
    x, y = node.get_click_position()
    device.click(x, y)

    print('currently clicked element: ')
    print(node.attrib)
    print(node.idx)


def register_watchers():
    device.watcher('CANCEL').when(text='取消').click(text='取消')
    device.watcher('CLOSE').when(text='关闭').click(text='关闭')
    device.watcher('LATER').when(text='Later').click(text='Later')
    device.watcher('UNDERSTOOD').when(text='Understood').click(text='Understood')
    device.watcher('CANSEL1').when(text='cancel').click(text='cancel')
    device.watcher('CANSEL2').when(text='Cancel').click(text='Cancel')
    device.watcher('CANSEL3').when(text='CANCEL').click(text='CANCEL')
