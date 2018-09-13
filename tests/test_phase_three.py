import pytest

from src.clients.jira.rest.jira_rest_client import JiraRestClient


@pytest.mark.flaky(reruns=2)
def test_pass_each_next_time():
    JiraRestClient.number_of_instances += 1
    print(JiraRestClient.number_of_instances)
    assert JiraRestClient.number_of_instances % 2 == 0, 'Expected number of instances should be even'
