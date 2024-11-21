import requests
import time
from typing import Optional, List
import os
from ._version import __version__

class Review:
    def __init__(self, form_id: str, api_key: str, base_url: str):
        self.form_id = form_id
        self.api_key = api_key
        self.base_url = base_url
        self.fields = {}
        self.meta = {}
        self.assign_to = []
        self.assign_to_groups = []

    def add_field_data(self, field_name: str, value=None):
        if value is not None:
            self.fields[field_name] = value
        return self

    def set_fields_data(self, fields=None):
        if fields is not None:
            self.fields.update(fields)
        return self

    def clear_field_data(self):
        self.fields = {}
        return self

    def add_meta_data(self, attribute: str, value=None):
        if value is not None:
            self.meta[attribute] = value
        return self

    def set_meta_data(self, fields=None):
        if fields is not None:
            self.meta.update(fields)
        return self

    def assign_to_users(self, user_emails: List[str]):
        if user_emails is not None:
            self.assign_to = user_emails
        return self

    def assign_to_user_groups(self, group_ids: List[str]):
        if group_ids is not None:
            self.assign_to_groups = group_ids
        return self

    def send_request(self):
        version = __version__
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
        }
        body = {
            'formId': self.form_id,
            'fields': self.fields,
            'meta': self.meta,
            **({'assignTo': self.assign_to} if self.assign_to else {}),
            **({'assignToGroups': self.assign_to_groups} if self.assign_to_groups else {}),
            'millis': int(time.time() * 1000),
            'origin': "py-sdk",
            'originV': version,
        }
        try:
          response = requests.post(f"{self.base_url}/requestReview", headers=headers, json=body)
          if not response.ok:
              raise Exception(f"gotoHuman API request failed with status code {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as err:
            raise Exception(f"gotoHuman API request failed: {str(err)}")

        return response.json()


class GotoHuman:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GOTOHUMAN_API_KEY')
        if not self.api_key:
            raise ValueError('Please pass an API key or set it in the environment variable GOTOHUMAN_API_KEY')
        self.base_url = os.getenv('GOTOHUMAN_BASE_URL', 'https://api.gotohuman.com')

    def create_review(self, form_id: str):
        if not form_id:
            raise ValueError('Please pass a form ID')
        return Review(form_id, self.api_key, self.base_url)