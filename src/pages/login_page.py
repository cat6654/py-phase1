from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from src.locators.locators import LoginPageLocators
from src.pages.base_page import BasePage


class LoginPage(BasePage):
    def set_user_name(self, user_name):
        self.driver.find_element(*LoginPageLocators.USER_NAME).send_keys(user_name)

    def set_password(self, password):
        self.driver.find_element(*LoginPageLocators.PASSWORD).send_keys(password)

    def click_login_button(self):
        self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

    def get_error_text(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(LoginPageLocators.ERROR_TEXT))
        return str(self.driver.find_element(*LoginPageLocators.ERROR_TEXT).text.encode("utf-8"))
