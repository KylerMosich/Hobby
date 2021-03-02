from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from time import sleep
import os


def connect(headless=True):
    # Connect to Foundry in Firefox.
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(executable_path=os.environ["GECKO_PATH"], options=options)
    driver.get(os.environ["FOUNDRY_IP"])

    # Join as Mae.
    Select(driver.find_element_by_name("userid")).select_by_visible_text("Mae")
    driver.find_element_by_name("submit").click()

    # Sleep until data is ready to be accessed.
    while True:
        sleep(5)
        try:
            driver.execute_script("return game.users._source")
            break
        except JavascriptException as e:
            continue

    print("Driver Initialized.")
    return driver
