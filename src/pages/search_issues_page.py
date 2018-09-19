from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from src.locators.locators import SearchPageLocators
from src.pages.base_page import BasePage


class SearchPage(BasePage):
    def set_assignee_to_current_user(self):
        self.open_assignee_search_menu()
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(SearchPageLocators.CURRENT_USER))
        self.driver.find_element(*SearchPageLocators.CURRENT_USER).click()

    def open_assignee_search_menu(self):
        self.driver.find_element(*SearchPageLocators.ASSIGNEE_MENU).click()

    def open_status_search_menu(self):
        self.driver.find_element(*SearchPageLocators.STATUS_MENU).click()

    def set_given_search_status(self, status_to_search):
        self.open_status_search_menu()
        self.driver.find_element(*SearchPageLocators.STATUS_SEARCH_INPUT).send_keys(status_to_search)

    def get_search_results_showing_text(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(SearchPageLocators.SHOWING_TEXT))
        return str(self.driver.find_element(*SearchPageLocators.SHOWING_TEXT).text.encode("utf-8"))

    def get_search_results_issue_list(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(SearchPageLocators.ISSUE_LIST))
        return self.driver.find_elements(*SearchPageLocators.ISSUE_LIST)

    def get_search_no_results_text(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(SearchPageLocators.NO_RESULTS_TEXT))
        return str(self.driver.find_element(*SearchPageLocators.NO_RESULTS_TEXT).text.encode("utf-8"))

    def switch_to_advanced_search_mode(self):
        try:
            if self.driver.find_element(*SearchPageLocators.SEARCH_MODE_SWITCH_LINK).is_displayed():
                self.driver.find_element(*SearchPageLocators.SEARCH_MODE_SWITCH_LINK).click()
        except NoSuchElementException:
            print('Advanced search link is not displayed')

    def set_advanced_search_text_input(self, text):
        self.switch_to_advanced_search_mode()
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(SearchPageLocators.ADVANCED_SEARCH_INPUT))
        self.driver.find_element(*SearchPageLocators.ADVANCED_SEARCH_INPUT).send_keys(text)

    def click_search_button(self):
        self.driver.find_element(*SearchPageLocators.SEARCH_BUTTON).click()

    def wait_for_edit_view_to_reload(self):
        try:
            WebDriverWait(self.driver, 10).until(
                expected_conditions.staleness_of(self.driver.find_element(*SearchPageLocators.ISSUE_EDIT_VIEW_HEADER)))
            if self.driver.find_element(*SearchPageLocators.ISSUE_EDIT_VIEW_HEADER).is_enabled():
                pass
        except NoSuchElementException:
            print('Edit Issue view is not displayed. There might be no search results.')

    def search_for_issue_using_advanced_search(self, text):
        self.set_advanced_search_text_input(text)
        self.click_search_button()
        self.wait_for_edit_view_to_reload()
