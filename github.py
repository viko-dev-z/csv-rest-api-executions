import json
from typing import Any, Union

import requests
import basicauth
import pandas
import math
import re

class GitHub:
    def __init__(self, filename):
        self.filename = filename
        self.client = basicauth.basicauth()
        self.data = pandas.read_csv(filename)
        self.results = []
        self.data.fillna('', inplace=True)
        self.total_records = len(self.data.index) - 1

    def test_api(self):
        print('Authenticating...')
        print(self.client.auth_header())

    def next_record_unique(self, i, key_field):
        if i == self.total_records:
            print('finished!')
            return i + 1
        else:
            i = i + 1
            if self.data[key_field][i] == self.data[key_field][i - 1]:
                print('skipping row in GH')
                self.next_record(i + 1, key_field)
            else:
                return i

    def next_record(self, i, error_field, success_field):
        if i == self.total_records:
            print('finished!_')
            return i + 1
        else:
            i = i + 1
            if (self.data[error_field][i] == self.data[error_field][i - 1] or self.data[success_field][i] == self.data[success_field][i - 1]):
                print('skipping row' + str(i))
                self.next_record(i + 1, error_field, success_field)
            else:
                return i


    def get_users(self, payload):
        for record in payload:
            record_name = record['endpoint']
            json = record['data']
            for index in record['rows']:
                # print("debug01: "+ str(record_name[index-2]))
                response = self.get_user(record_name[index], json)
                if response.startswith('Error:'):
                    self.data['Error Message'][index] = response
                    self.data.to_csv(self.filename, index=False)
                else:
                    self.data['Execution Results'][index] = response
                    self.data['Error Message'][index] = ''
                    self.data.to_csv(self.filename, index=False)


    def get_user(self, name, payload):
        user = requests.get(self.client.base_url + '/users/' + str(name),
                                     headers={
                                         'Authorization': self.client.auth_header(),
                                         'Content-Type': 'application/json'
                                     })
        print(str(user.url))
        print(str(payload))
        print(str(user.status_code))
        if user.status_code == 200:
            json_response = user.json()
            print(json_response)
            if ('name' in json_response) & ('email' in json_response):
                success_message = str(json_response['name']) + ' - ' \
                                  + str(json_response['email'])
                return success_message
        else:
            print('we failed for user: ' + str(name) )
            error_message = "Error: " + str(user.status_code) + " - " + str(user.reason)
            # \ + "\n\r" +str(user.text)
            print(user.text)
            return error_message




