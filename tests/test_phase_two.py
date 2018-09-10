import pytest
import requests
from configparser import ConfigParser, ExtendedInterpolation
import os
import random
import string

from src.clients.jira.rest.jira_rest_client import JiraRestClient
from src.entities.jira.payload import Payload

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(PATH('../resources/test_config.ini'))

entities_to_delete = []
jira_rest_client = JiraRestClient()

@pytest.fixture
def jira_rest_client_setup(request):
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

    def teardown():
        for entity in entities_to_delete:
            jira_rest_client.delete_given_entity(config.get('JIRA', 'jira.url.rest.create.issue'), entity)

    request.addfinalizer(teardown)

    return jira_rest_client


def test_login_positive():
    response = requests.get(
        config.get('JIRA', 'jira.url.rest.auth'),
        auth=(config.get('JIRA', 'jira.user'), config.get('JIRA', 'jira.password')),
    )
    message = Payload(response.text)
    assert response.status_code == 200,\
        'Actual status code {} is different from Expected {}'.format(response.status_code, 200)
    assert message.name == config.get('JIRA', 'jira.user'),\
        'Actual user name {} if different from Expected {}'.format(message.name, config.get('JIRA', 'jira.user'))


def test_login_wrong_user():
    response = requests.get(
        config.get('JIRA', 'jira.url.rest.auth'),
        auth=('wrong_user', config.get('JIRA', 'jira.password')),
    )
    assert response.status_code == 401,\
        'Actual status code {} is different from Expected {}'.format(response.status_code, 200)


def test_login_wrong_password():
    response = requests.get(
        config.get('JIRA', 'jira.url.rest.auth'),
        auth=(config.get('JIRA', 'jira.user'), 'wrong_password'),
    )
    assert response.status_code == 401,\
        'Actual status code {} is different from Expected {}'.format(response.status_code, 200)


def test_can_post_new_bug(jira_rest_client_setup):
    response = jira_rest_client_setup.create_new_entity(
        config.get('JIRA', 'jira.url.rest.create.issue'),
        config.get('JIRA', 'jira.project'),
        config.get('JIRA', 'jira.issue.type')
    )
    assert response.status_code == 201, 'Actual status code {} is different from Expected {}'.format(
        response.status_code, 201)

    message = Payload(response.text)
    print('Created entity with id = %s'.format(message.id))

    response = jira_rest_client_setup.search_for_entity_by_given_filter(
        config.get('JIRA', 'jira.url.rest.search.issue'),
        config.get('JIRA', 'jira.project'),
        'id={}'.format(message.id)
    )
    assert response.status_code == 200, 'Actual status code {} is different from Expected {}'.format(
        response.status_code, 200)
    entities_to_delete.append(message.key)


def test_post_bug_with_missing_required_fields(jira_rest_client_setup):
    response = jira_rest_client_setup.create_new_entity(
        config.get('JIRA', 'jira.url.rest.create.issue'),
        config.get('JIRA', 'jira.project'),
        config.get('JIRA', 'jira.issue.type'),
        fill_required_fields=False
    )
    assert response.status_code == 400, 'Actual status code {} is different from Expected {}'.format(
        response.status_code, 400)


def test_post_bug_with_too_long_string_value(jira_rest_client_setup):
    body = jira_rest_client_setup.generate_json_to_post_entity(
        config.get('JIRA', 'jira.project'),
        config.get('JIRA', 'jira.issue.type'),
        jira_rest_client_setup.required_fields,
        True,
        1000
    )
    response = jira_rest_client_setup.create_new_entity(
        config.get('JIRA', 'jira.url.rest.create.issue'),
        config.get('JIRA', 'jira.project'),
        config.get('JIRA', 'jira.issue.type'),
        request_body=body
    )
    assert response.status_code == 400, 'Actual status code {} is different from Expected {}'.format(
        response.status_code, 400)


@pytest.mark.parametrize("test_input, expected", [
    ("5", 5),
    ("1", 1),
    ("0", 0),
])
def test_search_for_given_amount_of_issues(jira_rest_client_setup, test_input, expected):
    response = jira_rest_client_setup.search_for_entity_by_given_filter(
        config.get('JIRA', 'jira.url.rest.search.issue'),
        config.get('JIRA', 'jira.project'),
        None,
        test_input
    )
    message = Payload(response.text)
    actual_max_results = message.maxResults
    assert response.status_code == 200, 'Actual status code {} is different from Expected {}'.format(
        response.status_code, 200)
    assert actual_max_results == expected, 'Actual max results {} is different from Expected {}'.format(
        actual_max_results, expected)


def test_can_update_existing_bug(jira_rest_client_setup):
    response = jira_rest_client_setup.create_new_entity(
        config.get('JIRA', 'jira.url.rest.create.issue'),
        config.get('JIRA', 'jira.project'),
        config.get('JIRA', 'jira.issue.type')
    )
    assert response.status_code == 201, 'Actual status code {} is different from Expected {}'.format(
        response.status_code, 201)

    message = Payload(response.text)
    print('Created entity with id = %s'.format(message.id))
    entities_to_delete.append(message.key)

    fields_to_update = {'description': 'Here is random character {}'.format(random.choice(string.ascii_lowercase))}
    response = jira_rest_client_setup.update_existing_entity(
        config.get('JIRA', 'jira.url.rest.create.issue'),
        message.id,
        fields_to_update
    )
    assert response.status_code == 204, 'Actual status code {} is different from Expected {}'.format(
        response.status_code, 204)

    response = jira_rest_client_setup.search_for_entity_by_given_filter(
        config.get('JIRA', 'jira.url.rest.search.issue'),
        config.get('JIRA', 'jira.project'),
        'id={}'.format(message.id)
    )
    assert response.status_code == 200, 'Actual status code {} is different from Expected {}'.format(
        response.status_code, 200)

    message = Payload(response.text)
    assert message.issues[0].get('fields').get('description') == fields_to_update.get('description'),\
        'Actual status code {} is different from Expected {}'.format(
            message.issues[0].get('fields').get('description'), fields_to_update.get('description'))
