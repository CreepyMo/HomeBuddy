from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class ThankYouPage(BasePage):

    WE_ARE_SORRY = (By.XPATH, "//*[text()=\"We're sorry, but we couldn't find any contractors \"]")
    GO_TO_HOMEPAGE_LINK = (By.XPATH, "//a[//span[text()='Go to homepage']]")

    def assert_thank_you_page(self):
        we_are_sorry = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located(self.WE_ARE_SORRY))
        assert we_are_sorry is not None, "We are Sorry H2 is not present on the page!"

        homepage_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.GO_TO_HOMEPAGE_LINK))
        assert homepage_link is not None, "Homepage link is not present on the page!"
