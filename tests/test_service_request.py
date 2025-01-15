import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.hvac import HvacPage
from pages.thank_you import ThankYouPage

BASE_URL = "https://hb-autotests.stage.sirenltd.dev/hvac"
ZIP_CODE = 10001

test_data = [
    {
        "project_type": HvacPage.REPAIR,
        "equipment": HvacPage.AC,
        "power_source": None,
        "equipment_age": HvacPage.LESS_THAN_5,
        "property_type": HvacPage.DETACHED,
        "house_square": 60,
        "is_owner": True
    },
    {
        "project_type": HvacPage.REPLACEMENT_OR_INSTALLATION,
        "equipment": HvacPage.CENTRAL_HEATING,
        "power_source": HvacPage.GAS,
        "equipment_age": HvacPage.FROM_5_TO_10,
        "property_type": HvacPage.MODULAR,
        "house_square": 120,
        "is_owner": False
    },
    {
        "project_type": HvacPage.REPLACEMENT_OR_INSTALLATION,
        "equipment": HvacPage.BOILER_RADIATOR,
        "power_source": HvacPage.GAS,
        "equipment_age": HvacPage.MORE_THAN_10,
        "property_type": HvacPage.MODULAR,
        "house_square": 20,
        "is_owner": False
    }
]

zip_code_test_data = [
    {"value": 1000, "is_valid": False},
    {"value": "qwert", "is_valid": False},
    {"value": 65001, "is_valid": True}
]


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.close()


@pytest.mark.parametrize("test_case", test_data)
def test_service_request_end_to_end(driver, test_case):
    hvac = HvacPage(driver)
    hvac.open(BASE_URL)

    hvac.enter_zip_code_and_get_estimate(zip_code=ZIP_CODE)
    hvac.set_project_type(test_case["project_type"])
    hvac.set_equipment(test_case["equipment"])
    hvac.set_power_source(test_case["power_source"])
    hvac.set_equipment_age(test_case["equipment_age"])
    hvac.set_property_type(test_case["property_type"])
    hvac.set_house_square(test_case["house_square"])
    hvac.set_ownership(test_case["is_owner"])
    hvac.set_name_and_email("Stas B", "blastan@qamad.net")
    hvac.set_phone_and_submit(2234567890)

    ty = ThankYouPage(driver)
    ty.assert_thank_you_page()


@pytest.mark.parametrize("zip_code", zip_code_test_data)
def test_zip_code_validation(driver, zip_code):
    hvac = HvacPage(driver)
    hvac.open(BASE_URL)

    hvac.enter_zip_code_and_get_estimate(zip_code=zip_code["value"])
    hvac.assert_zip_code_validation(is_valid=zip_code["is_valid"])


def test_cancel_project(driver):
    hvac = HvacPage(driver)
    hvac.open(BASE_URL)

    hvac.enter_zip_code_and_get_estimate(zip_code=ZIP_CODE)
    hvac.cancel_project()
    zip_code_input = hvac.get_element_by_xpath(hvac.build_xpath(hvac.ZIP_CODE))
    assert zip_code_input, "User is not redirected to Hvac page after cancelling the project!"
