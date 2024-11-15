import os
import sys
import time
import pickle
import warnings

from extender.extender import Extender
from repairer.repairer import Repairer
from scripting.collector import read_test_scripts
from utils.get_current_device_info import get_package_name
from utils.logging import init_logger


def ext_rep(ext_w, rep_w, script_path, log_record_path, result_save_path):
    # save intermediate files created while running the program
    if not os.path.exists("tmp/"):
        os.makedirs("tmp/")

    if not os.path.exists(log_record_path):
        with open(log_record_path, 'w'):
            pass
    logging = init_logger("logger1", log_record_path)

    # install and open the base application
    package_name = get_package_name()
    # package_name = ""
    print("Current application's package name: " + package_name)
    logging.info("Current application's package name: " + package_name)

    print("Collect information about the script being tested ...")
    logging.info("Collect information about the script being tested ...")
    if not os.path.exists(script_path):
        warnings.warn("Specify the correct test script path.")
        sys.exit()
    locators, caps, ori_code_line = read_test_scripts(script_path)

    print("Perform the test extension ...")
    logging.info("Perform the test extension ...")
    extender = Extender(package_name, locators, ext_w)
    extended_model, extended_edge_bounds, ori_screens_order, ori_edges_order, ori_edge_bounds_order = extender.work()
    print("Extension ends.")
    print("Please install the updated app ...")

    # time.sleep(60)

    print("Perform the test repair ...")
    logging.info("Perform the test repair ...")
    repairer = Repairer(package_name, rep_w, caps, result_save_path, extended_model, extended_edge_bounds, ori_screens_order, ori_edges_order, ori_edge_bounds_order)
    repairer.work()
    print("Repair ends.")


def demo():
    ext_w = 2 # test extended event search depth
    rep_w = 2 # test repair event search depth
    current_dir = os.getcwd()
    script_path = os.path.join(current_dir, "demo", "test-26-SoundRecorder-14.py")
    log_record_path = os.path.join(current_dir, "demo", "log.txt")
    result_save_path = os.path.join(current_dir, "demo")
    ext_rep(ext_w, rep_w, script_path, log_record_path, result_save_path)


if __name__ == '__main__':
    demo()


