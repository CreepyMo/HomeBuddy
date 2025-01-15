from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class HvacPage(BasePage):

    ZIP_CODE = "data-autotest-input-0"
    GET_ESTIMATE = "data-autotest-zip-submit-0"
    NEXT = "data-autotest-next"
    YES = "data-autotest-yes"

    REPLACEMENT_OR_INSTALLATION = "data-autotest-projecttype-replacementorinstallation"
    REPAIR = "data-autotest-projecttype-repair"
    PROJECT_TYPE_NOT_SURE = "data-autotest-projecttype-replacementorinstallation-notsure"

    AC = "data-autotest-equipment-airconditioner"
    CENTRAL_HEATING = "data-autotest-equipment-heatingorfurnace"
    BOILER_RADIATOR = "data-autotest-equipment-boilerorradiator"
    HEAT_PUMP = "data-autotest-equipment-heatpump"
    WATER_HEATER = "data-autotest-equipment-waterheater"
    EQUIPMENT_NOT_SURE = "data-autotest-equipment-notsure"

    GAS = "data-autotest-energysource-gas"
    ELECTRICITY = "data-autotest-energysource-electricity"
    PROPANE = "data-autotest-energysource-propane"
    OIL = "data-autotest-energysource-oil"
    ENERGY_SOURCE_NOT_SURE = "data-autotest-energysource-notsure"

    LESS_THAN_5 = "data-autotest-equipmentage-5"
    FROM_5_TO_10 = "data-autotest-equipmentage-10"
    MORE_THAN_10 = "data-autotest-equipmentage-10plus"
    EQUIPMENT_AGE_NOT_SURE = "data-autotest-equipmentage-notsure"

    DETACHED = "data-autotest-propertytype-detached"
    MODULAR = "data-autotest-propertytype-mobile"
    COMMERCIAL = "data-autotest-propertytype-commercial"
    APARTMENT = "data-autotest-propertytype-apartment"

    HOUSE_AREA = "data-autotest-squarefeet-tel"

    OWNER_YES = "data-autotest-owner-yes"
    OWNER_NO = "data-autotest-owner-no"

    ADDRESS = "data-autotest-address-text"

    FULL_NAME = "data-autotest-fullname-text"
    EMAIL = "data-autotest-email-email"
    PHONE_NUMBER = "data-autotest-phonenumber-tel"
    SUBMIT_REQUEST = "data-autotest-submit-my-request"

    CLOSE = "data-autotest-close"
    RETURN = "data-autotest-return-to-project"
    CANCEL_PROJECT = "data-autotest-cancel-project"

    ZIP_CODE_ERROR_MESSAGE = (By.XPATH, "//div[text()='The ZIP Code must be 5 digits with no spaces']")

    def build_xpath(self, data_autotest):
        return f"//*[@{data_autotest}]"

    def enter_zip_code_and_get_estimate(self, zip_code):
        self.get_element_by_xpath(self.build_xpath(self.ZIP_CODE)).send_keys(zip_code)
        self.get_element_by_xpath(self.build_xpath(self.GET_ESTIMATE)).click()

    def set_project_type(self, project_type):
        self.get_element_by_xpath(f"{self.build_xpath(project_type)}/..").click()
        self.get_element_by_xpath(self.build_xpath(self.YES if project_type == self.REPAIR else self.NEXT)).click()

    def set_equipment(self, equipment):
        self.get_element_by_xpath(f"{self.build_xpath(equipment)}/..").click()
        self.get_element_by_xpath(self.build_xpath(self.NEXT)).click()

    def set_power_source(self, source):
        if source is not None:
            self.get_element_by_xpath(f"{self.build_xpath(source)}/..").click()
            self.get_element_by_xpath(self.build_xpath(self.NEXT)).click()

    def set_equipment_age(self, age):
        self.get_element_by_xpath(f"{self.build_xpath(age)}/..").click()
        self.get_element_by_xpath(self.build_xpath(self.NEXT)).click()

    def set_property_type(self, property_type):
        self.get_element_by_xpath(f"{self.build_xpath(property_type)}/..").click()
        self.get_element_by_xpath(self.build_xpath(self.NEXT)).click()

    def set_house_square(self, house_square):
        self.get_element_by_xpath(self.build_xpath(self.HOUSE_AREA)).send_keys(str(house_square))
        self.get_element_by_xpath(self.build_xpath(self.NEXT)).click()

    def set_ownership(self, is_owner):
        self.get_element_by_xpath(f"{self.build_xpath(self.OWNER_YES if is_owner else self.OWNER_NO)}/..").click()
        self.get_element_by_xpath(self.build_xpath(self.NEXT if is_owner else self.YES)).click()

    def set_project_address(self, address):
        self.get_element_by_xpath(self.build_xpath(self.ADDRESS)).send_keys(address)
        self.get_element_by_xpath(self.build_xpath(self.NEXT)).click()

    def set_name_and_email(self, full_name, email):
        self.get_element_by_xpath(self.build_xpath(self.FULL_NAME)).send_keys(full_name)
        self.get_element_by_xpath(self.build_xpath(self.EMAIL)).send_keys(email)
        self.get_element_by_xpath(self.build_xpath(self.NEXT)).click()

    def set_phone_and_submit(self, phone_number):
        self.get_element_by_xpath(self.build_xpath(self.PHONE_NUMBER)).send_keys(str(phone_number))
        self.get_element_by_xpath(self.build_xpath(self.SUBMIT_REQUEST)).click()

    def assert_zip_code_validation(self, is_valid):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ZIP_CODE_ERROR_MESSAGE))
            element_found = True
        except:
            element_found = False

        if is_valid:
            assert not element_found, "Element should not be present but was found."
        else:
            assert element_found, "Element should be present but was not found."

    def cancel_project(self):
        self.get_element_by_xpath(self.build_xpath(self.CLOSE)).click()
        self.assert_cancel_project_confirmation_page()
        self.get_element_by_xpath(self.build_xpath(self.CANCEL_PROJECT)).click()

    def assert_cancel_project_confirmation_page(self):
        cancel_xpath = self.build_xpath(self.CANCEL_PROJECT)
        self.get_element_by_xpath(cancel_xpath, additional_condition=EC.element_to_be_clickable((By.XPATH, cancel_xpath)))
        return_xpath = self.build_xpath(self.RETURN)
        self.get_element_by_xpath(return_xpath, additional_condition=EC.element_to_be_clickable((By.XPATH, return_xpath)))
