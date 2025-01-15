from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def find_element(self, locator, timeout=10, additional_condition=None):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

            if additional_condition:
                element = WebDriverWait(self.driver, timeout).until(additional_condition)

            return element

        except TimeoutException:
            raise Exception(f"Element with locator {locator} not found or condition failed.")

    def get_element_by_xpath(self, xpath, additional_condition=None):
        return self.find_element(locator=(By.XPATH, xpath), additional_condition=additional_condition)
