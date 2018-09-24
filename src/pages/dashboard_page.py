from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from src.locators.locators import DashBoardPageLocators
from src.pages.base_page import BasePage


class DashboardPage(BasePage):
    def logout(self):
        try:
            if self.is_user_options_menu_visible():
                self.open_user_options_menu()
                self.driver.find_element(*DashBoardPageLocators.LOGOUT).click()
        except WebDriverException:
            print('WebDriverException occurred. Logout was not successful')

    def open_user_options_menu(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(DashBoardPageLocators.USER_OPTIONS))
        self.driver.find_element(*DashBoardPageLocators.USER_OPTIONS).click()

    def open_issues_menu(self):
        self.driver.find_element(*DashBoardPageLocators.ISSUES_MENU).click()

    def go_to_search_issues_page(self):
        self.open_issues_menu()
        self.driver.find_element(*DashBoardPageLocators.SEARCH_ISSUES_LINK).click()

    def is_user_options_menu_visible(self):
        return self.driver.find_element(*DashBoardPageLocators.USER_OPTIONS).is_displayed()

