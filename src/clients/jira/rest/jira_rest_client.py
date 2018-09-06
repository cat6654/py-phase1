import random
import string

import requests
import json


from src.entities.jira.payload import Payload


class JiraRestClient:
    required_fields = {}
    cookies = None
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def login(self, url, user, password):
        login = requests.get(
            url,
            auth=(user, password),
        )
        self.cookies = login.cookies

    def get_required_fields(self, url, project, entity):
        self.check_cookies()
        query = {'projectKeys': project, 'issuetypeNames': entity, 'expand': 'projects.issuetypes.fields'}
        response = requests.get(
            url,
            cookies=self.cookies,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
            params=query
        )
        message = Payload(response.text)
        fields = message.projects[0].get('issuetypes')[0].get('fields')
        for field in fields:
            if field != 'project' and field != 'issuetype':
                if fields.get(field).get('required'):
                    self.required_fields[field] = fields.get(field)
        print('Required fields are:')
        print(self.required_fields)

    def create_new_entity(self, url, project, entity, request_body=None, fill_required_fields=True):
        self.check_cookies()

        if not bool(self.required_fields):
            self.get_required_fields(url + 'createmeta', project, entity)
        if request_body is None:
            body = self.generate_json_to_post_entity(project, entity, self.required_fields, fill_required_fields, 50)
        else:
            body = request_body
        return requests.post(
            url,
            cookies=self.cookies,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
            data=body
        )

    def update_existing_entity(self, url, project, entity_id, fields_to_update):
        self.check_cookies()
        fields_dict = {
            'fields': {}
        }
        for field in fields_to_update:
            fields_dict.get('fields')[field] = fields_to_update.get(field)
        body = json.dumps(fields_dict)
        return requests.put(
            '{}{}'.format(url, entity_id),
            cookies=self.cookies,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
            data=body
        )

    def search_for_entity_by_given_filter(self, url, project, search_filter, max_results=100):
        self.check_cookies()
        if search_filter is None:
            query = {'jql': 'project={}'.format(project, search_filter), 'maxResults': max_results}
        else:
            query = {'jql': 'project={}&{}'.format(project, search_filter), 'maxResults': max_results}
        return requests.get(
            url,
            cookies=self.cookies,
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
            params=query
        )

    def generate_json_to_post_entity(self, project, entity, required_fields, fill_in_required_fields, string_len):
        default_fields = {
            'fields': {
                'project': {'key': project},
                'description': 'value for description',
                'issuetype': {'name': entity}
            }
        }
        if fill_in_required_fields:
            for required_field in required_fields:
                if required_field not in default_fields.get('fields'):
                    default_fields.get('fields')[required_field] = self.generate_field_value_by_type(required_field, string_len)
        return json.dumps(default_fields)

    def generate_field_value_by_type(self, field, string_len=50):
        if self.required_fields[field].get('schema')['type'] == 'string':
            return 'Random string {}'.format(''.join(random.choice(string.ascii_lowercase) for x in range(string_len)))
        if self.required_fields[field].get('schema')['type'] == 'user':
            return 'Alexander_Kostuchenko'
        if self.required_fields[field].get('schema')['type'] == 'priority':
            return self.required_fields[field].get('allowedValues')[0].get('name')
        if self.required_fields[field].get('schema')['type'] == 'array':
            if self.required_fields[field].get('allowedValues') is not None:
                return self.required_fields[field].get('allowedValues')[0].get('name')
            else:
                return string_len
        else:
            return 'Default'

    def check_cookies(self):
        if self.cookies is None:
            raise Exception('Your cookies are empty. Login first, you silly.')
