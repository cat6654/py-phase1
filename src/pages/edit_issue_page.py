from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from src.locators.locators import EditIssuePageLocators, SearchPageLocators
from src.pages.base_page import BasePage


class EditIssuePage(BasePage):
    def set_summary_field_value(self, value):
        self.driver.find_element(*EditIssuePageLocators.SUMMARY_VALUE).click()
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(EditIssuePageLocators.SUMMARY_EDIT_FORM)
        )
        self.driver.find_element(*EditIssuePageLocators.SUMMARY_EDIT_FORM).clear()
        self.driver.find_element(*EditIssuePageLocators.SUMMARY_EDIT_FORM).send_keys(value)
        self.driver.find_element(*EditIssuePageLocators.SUMMARY_EDIT_FORM_SUBMIT_BUTTON).click()

    def set_priority_field_value(self, value):
        WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(EditIssuePageLocators.PRIORITY_VALUE)
        )
        self.driver.find_element(*EditIssuePageLocators.PRIORITY_VALUE).click()
        self.driver.find_element(*EditIssuePageLocators.PRIORITY_EDIT_FORM).clear()
        self.driver.find_element(*EditIssuePageLocators.PRIORITY_EDIT_FORM).send_keys(value)
        self.driver.find_element(*EditIssuePageLocators.PRIORITY_EDIT_FORM).send_keys(u'\ue007')

    def get_summary_field_value(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(EditIssuePageLocators.SUMMARY_VALUE)
        )
        return str(self.driver.find_element(*EditIssuePageLocators.SUMMARY_VALUE).text.encode("utf-8"))

    def get_priority_field_value(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(EditIssuePageLocators.PRIORITY_VALUE)
        )
        return str(self.driver.find_element(*EditIssuePageLocators.PRIORITY_VALUE).text.encode("utf-8"))

    def get_assignee_field_value(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.staleness_of(self.driver.find_element(*EditIssuePageLocators.ASSIGNEE_VALUE))
        )
        return str(self.driver.find_element(*EditIssuePageLocators.ASSIGNEE_VALUE).text.encode("utf-8"))

    def click_assign_to_me_link(self):
        self.driver.find_element(*EditIssuePageLocators.PEOPLE_MODULE).click()
        WebDriverWait(self.driver, 10).until(
            expected_conditions.staleness_of( self.driver.find_element(*EditIssuePageLocators.ASSIGN_TO_ME_LINK))
        )
        self.driver.find_element(*EditIssuePageLocators.ASSIGN_TO_ME_LINK).click()
