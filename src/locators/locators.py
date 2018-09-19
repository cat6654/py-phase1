from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    USER_NAME = (By.ID, 'login-form-username')
    PASSWORD = (By.ID, 'login-form-password')
    LOGIN_BUTTON = (By.ID, 'login-form-submit')
    ERROR_TEXT = (By.XPATH, "//div[@class='aui-message error']//p")


class DashBoardPageLocators(object):
    USER_OPTIONS = (By.ID, 'user-options')
    LOGOUT = (By.ID, 'log_out')
    ISSUES_MENU = (By.ID, 'find_link')
    SEARCH_ISSUES_LINK = (By.ID, 'issues_new_search_link_lnk')


class SearchPageLocators(object):
    ASSIGNEE_MENU = (By.XPATH, "//ul[@class='criteria-list']//li[@data-id='assignee']")
    CURRENT_USER = (By.XPATH, "//div[@id='assignee-suggestions']//li")
    STATUS_MENU = (By.XPATH, "//ul[@class='criteria-list']//li[@data-id='status']")
    STATUS_SEARCH_INPUT = (By.XPATH, "//div[@id='searcher-status-multi-select']//input")
    FIRST_STATUS_IN_SEARCH_LIST = (By.XPATH, "//div[@id='searcher-status-suggestions']//input[@type='checkbox']")
    SEARCH_MODE_SWITCH_LINK = (By.XPATH, "//div[@class='mode-switcher']//a")
    ADVANCED_SEARCH_INPUT = (By.ID, 'advanced-search')
    ISSUE_LIST = (By.XPATH, "//div[@class='search-results']//ol[@class ='issue-list']//li")
    SHOWING_TEXT = (By.XPATH, "//div[@class='issue-tools']//ul[@class='pager']//li[@class='showing']")
    SEARCH_BUTTON = (By.XPATH, "//div[@class='search-options-container']//button")
    NO_RESULTS_TEXT = (By.XPATH, "//div[@class='navigator-content empty-results']//h3")
    ISSUE_EDIT_VIEW_HEADER = (By.ID, 'stalker')


class EditIssuePageLocators(object):
    ASSIGN_TO_ME_LINK = (By.XPATH, "//div[@id='peoplemodule']//a[@id='assign-to-me']")
    ASSIGNEE_VALUE = (By.ID, 'assignee-val')
    SUMMARY_VALUE = (By.XPATH, "//header[@id='stalker']//h1[@id='summary-val']")
    SUMMARY_EDIT_FORM = (By.ID, 'summary')
    SUMMARY_EDIT_FORM_SUBMIT_BUTTON = (By.XPATH, "//form[@id='summary-form']//button[@type='submit']")
    PRIORITY_VALUE = (By.XPATH, "//div[@id='details-module']//span[@id='priority-val']")
    PRIORITY_EDIT_FORM = (By.ID, 'priority-field')
    PRIORITY_EDIT_FORM_SUBMIT_BUTTON = (By.XPATH, "//form[@id='priority-form']//button[@type='submit']")
    PEOPLE_MODULE = (By.ID, 'peoplemodule')
