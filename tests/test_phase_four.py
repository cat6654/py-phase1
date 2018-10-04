import random
import string

import allure
import pytest
from configparser import ConfigParser, ExtendedInterpolation

from allure_commons.types import AttachmentType
from selenium import webdriver
import os

from src.clients.jira.rest.jira_rest_client import JiraRestClient
from src.entities.jira.payload import Payload
from src.pages.dashboard_page import DashboardPage
from src.pages.edit_issue_page import EditIssuePage
from src.pages.login_page import LoginPage
from src.pages.search_issues_page import SearchPage
from webdriver_manager.chrome import ChromeDriverManager
# pytestmark = pytest.mark.webtest

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read_file(open(PATH('../resources/test_config.ini')))
expected_login_error = "Sorry, your username and password are incorrect - please try again"
expected_no_results_text = 'No issues were found to match your search'
jira_rest_client = JiraRestClient()


@pytest.fixture
def driver_setup(request):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(10)

    def fin():
        dashboard_page = DashboardPage(driver)
        dashboard_page.logout()
        driver.quit()
    request.addfinalizer(fin)
    return driver


@pytest.fixture
def setup_and_login(driver_setup):
    driver_setup.get(config.get('JIRA', 'jira.url.ui.login'))
    login_page = LoginPage(driver_setup)
    login_page.set_user_name(config.get('JIRA', 'jira.user'))
    login_page.set_password(config.get('JIRA', 'jira.password'))
    login_page.click_login_button()


def rest_cleanup():
    response = jira_rest_client.search_for_entity_by_given_filter(
        config.get('JIRA', 'jira.url.rest.search.issue'),
        config.get('JIRA', 'jira.project'),
        'reporter={}'.format(config.get('JIRA', 'jira.user'))
    )
    message = Payload(response.text)
    for issue in message.issues:
        jira_rest_client.delete_given_entity(config.get('JIRA', 'jira.url.rest.create.issue'), issue.get('key'))


@pytest.fixture
def jira_rest_setup(request):
    jira_rest_client.login(
        config.get('JIRA', 'jira.url.rest.auth'),
        config.get('JIRA', 'jira.user'),
        config.get('JIRA', 'jira.password'),
    )
    jira_rest_client.get_required_fields(
        config.get('JIRA', 'jira.url.rest.meta'),
        config.get('JIRA', 'jira.project'),
        config.get('JIRA', 'jira.issue.type')
    )
    rest_cleanup()

    fields_to_add = {'labels': ['one_defect']}
    jira_rest_client.create_new_entity(
        config.get('JIRA', 'jira.url.rest.create.issue'),
        config.get('JIRA', 'jira.project'),
        config.get('JIRA', 'jira.issue.type'),
        additional_fields=fields_to_add
    )
    fields_to_add = {'labels': ['five_defects']}
    for i in range(5):
        jira_rest_client.create_new_entity(
            config.get('JIRA', 'jira.url.rest.create.issue'),
            config.get('JIRA', 'jira.project'),
            config.get('JIRA', 'jira.issue.type'),
            additional_fields=fields_to_add
        )
    request.addfinalizer(rest_cleanup)


@allure.testcase("Login with valid credentials in UI test")
def test_login_positive_case(driver_setup):
    with pytest.allure.step("Navigate to login screen"):
        driver_setup.get(config.get('JIRA', 'jira.url.ui.login'))

    with pytest.allure.step("Fill in valid credentials and click 'login' button"):
        login_page = LoginPage(driver_setup)
        login_page.set_user_name(config.get('JIRA', 'jira.user'))
        login_page.set_password(config.get('JIRA', 'jira.password'))
        login_page.click_login_button()
        allure.attach(driver_setup.get_screenshot_as_png(), name='valid_credentials_login',
                      attachment_type=AttachmentType.PNG)

    with pytest.allure.step("Verify if user was navigated to dashboard page after successful login"):
        assert driver_setup.current_url == config.get('JIRA', 'jira.url.ui.dashboard'),\
            'Actual url {} is different from Expected {}'.format(
                driver_setup.current_url, config.get('JIRA', 'jira.url.ui.dashboard')
            )


@allure.testcase("Login with wrong username in UI test")
def test_login_wrong_username(driver_setup):
    with pytest.allure.step("Navigate to login screen"):
        driver_setup.get(config.get('JIRA', 'jira.url.ui.login'))

    with pytest.allure.step("Fill in wrong username and click 'login' button"):
        login_page = LoginPage(driver_setup)
        login_page.set_user_name('wrong_username')
        login_page.set_password(config.get('JIRA', 'jira.password'))
        login_page.click_login_button()
        allure.attach(driver_setup.get_screenshot_as_png(), name='wrong_user_login',
                      attachment_type=AttachmentType.PNG)

    with pytest.allure.step("Verify if user is still at login page after failed login"):
        assert driver_setup.current_url == config.get('JIRA', 'jira.url.ui.login'),\
            'Actual url {} is different from Expected {}'.format(
                driver_setup.current_url, config.get('JIRA', 'jira.url.ui.login')
            )
    with pytest.allure.step("Verify if login error message is correct"):
        assert expected_login_error in login_page.get_error_text(), \
            'Actual error {} is different from Expected {}'.format(login_page.get_error_text(), expected_login_error)


@allure.testcase("Login with wrong password in UI test")
def test_login_wrong_password(driver_setup):
    with pytest.allure.step("Navigate to login screen"):
        driver_setup.get(config.get('JIRA', 'jira.url.ui.login'))

    with pytest.allure.step("Fill in wrong password and click 'login' button"):
        login_page = LoginPage(driver_setup)
        login_page.set_user_name(config.get('JIRA', 'jira.user'))
        login_page.set_password('wrong_password')
        login_page.click_login_button()
        allure.attach(driver_setup.get_screenshot_as_png(), name='wrong_password_login',
                      attachment_type=AttachmentType.PNG)

    with pytest.allure.step("Verify if user is still at login page after failed login"):
        assert driver_setup.current_url == config.get('JIRA', 'jira.url.ui.login'),\
            'Actual url {} is different from Expected {}'.format(
                driver_setup.current_url, config.get('JIRA', 'jira.url.ui.login')
            )
    with pytest.allure.step("Verify if login error message is correct"):
        assert expected_login_error in login_page.get_error_text(), \
            'Actual error {} is different from Expected {}'.format(login_page.get_error_text(), expected_login_error)


@allure.testcase("Search for issues in UI test")
@pytest.mark.parametrize("test_input, expected", [
    ("one_defect", '1 of 1'),
    ("five_defects", '1 of 5'),
    ("no_defects", expected_no_results_text),
])
def test_search_issues(jira_rest_setup, setup_and_login, driver_setup, test_input, expected):
    with pytest.allure.step("Navigate to search issues page"):
        dashboard_page = DashboardPage(driver_setup)
        dashboard_page.go_to_search_issues_page()

    with pytest.allure.step("Search for issues using advanced search"):
        search_page = SearchPage(driver_setup)
        search_page.search_for_issue_using_advanced_search('reporter = currentUser() and labels = "{}"'.format(test_input))
        allure.attach(driver_setup.get_screenshot_as_png(), name='search_results',
                      attachment_type=AttachmentType.PNG)

    with pytest.allure.step("Verify if actual search results match the expected results"):
        if expected == expected_no_results_text:
            assert expected in search_page.get_search_no_results_text(), \
                'Actual error {} is different from Expected {}'.format(search_page.get_search_no_results_text(), expected)
        else:
            assert expected in search_page.get_search_results_showing_text(),\
                'Actual showing text {} is different from Expected {}'.format(search_page.get_search_results_showing_text(), expected)


@allure.testcase("Update issue in UI test")
def test_update_issue(jira_rest_setup, setup_and_login, driver_setup):
    expected_summary = 'Updated summary {}'.format(''.join(random.choice(string.ascii_lowercase) for x in range(10)))
    expected_priority = 'High'
    expected_assignee = config.get('JIRA', 'jira.user').replace('_', " ")

    with pytest.allure.step("Navigate to search issues page"):
        dashboard_page = DashboardPage(driver_setup)
        dashboard_page.go_to_search_issues_page()

    with pytest.allure.step("Search for issue to update"):
        search_page = SearchPage(driver_setup)
        search_page.search_for_issue_using_advanced_search('reporter = currentUser() and labels = "one_defect"')
        allure.attach(driver_setup.get_screenshot_as_png(), name='search_results_for_update', attachment_type=AttachmentType.PNG)

    with pytest.allure.step("Update summary field value"):
        edit_issue_page = EditIssuePage(driver_setup)
        edit_issue_page.set_summary_field_value(expected_summary)
    with pytest.allure.step("Update priority field value"):
        edit_issue_page.set_priority_field_value(expected_priority)
    with pytest.allure.step("Click assign to me link"):
        edit_issue_page.click_assign_to_me_link()

    with pytest.allure.step("Verify if all fields were updated with expected values"):
        actual_assignee = edit_issue_page.get_assignee_field_value()
        actual_summary = edit_issue_page.get_summary_field_value()
        actual_priority = edit_issue_page.get_priority_field_value()
        allure.attach(driver_setup.get_screenshot_as_png(), name='update_results',
                      attachment_type=AttachmentType.PNG)

        assert expected_summary in actual_summary, \
            'Actual summary: {} is different from expected: {}'.format(actual_summary, expected_summary)
        assert expected_priority in actual_priority, \
            'Actual priority: {} is different from expected: {}'.format(actual_priority, expected_priority)
        assert expected_assignee in actual_assignee, \
            'Actual assignee: {} is different from expected: {}'.format(actual_assignee, expected_assignee)
