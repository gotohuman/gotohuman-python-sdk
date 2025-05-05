import httpx
import time
from typing import Any, Dict, Optional, List
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
        self.review_id_to_update = None

    def add_field_data(self, field_name: str, value=None):
        """
        Add a field value for the review.
        
        Args:
            field_name (str): The name of the field.
            value (Any): The value to set for the field. Find the required format in the app.
        Returns:
            Review: The current Review instance (for chaining).
        """
        if value is not None:
            self.fields[field_name] = value
        return self

    def set_fields_data(self, fields=None):
        """
        Set multiple field values for the review at once.
        
        Args:
            fields (dict): A dictionary of field names and values. Find the required format for a field in the app.
        Returns:
            Review: The current Review instance (for chaining).
        """
        if fields is not None:
            self.fields.update(fields)
        return self

    def clear_field_data(self):
        """
        Clear all field data from the review.
        
        Returns:
            Review: The current Review instance (for chaining).
        """
        self.fields = {}
        return self

    def add_meta_data(self, attribute: str, value=None):
        """
        Add or update a single meta attribute for the review.
        
        Args:
            attribute (str): The name of the meta attribute.
            value (Any): The value to set for the attribute.
        Returns:
            Review: The current Review instance (for chaining).
        """
        if value is not None:
            self.meta[attribute] = value
        return self

    def set_meta_data(self, fields=None):
        """
        Set multiple meta attributes for the review at once.
        
        Args:
            fields (dict): A dictionary of meta attribute names and values.
        Returns:
            Review: The current Review instance (for chaining).
        """
        if fields is not None:
            self.meta.update(fields)
        return self

    def assign_to_users(self, user_emails: List[str]):
        """
        Assign the review to specific users by their email addresses.
        
        Args:
            user_emails (List[str]): A list of user email addresses.
        Returns:
            Review: The current Review instance (for chaining).
        """
        if user_emails is not None:
            self.assign_to = user_emails
        return self

    def assign_to_user_groups(self, group_ids: List[str]):
        """
        Assign the review to specific user groups by their group IDs.
        
        Args:
            group_ids (List[str]): A list of user group IDs.
        Returns:
            Review: The current Review instance (for chaining).
        """
        if group_ids is not None:
            self.assign_to_groups = group_ids
        return self

    def update_for_review(self, review_id: str):
        """
        Update an existing review instead of creating a new one.
        
        Args:
            review_id (str): The ID of the review to update.
        Returns:
            Review: The current Review instance (for chaining).
        """
        if review_id is not None:
            self.review_id_to_update = review_id
        return self

    def send_request(self) -> Dict[str, Any]:
      """
      Send the review request synchronously to the API.
      
      Returns:
          Dict[str, Any]: The response from the API as a dictionary.
      Raises:
          Exception: If a network, HTTP, or timeout error occurs.
      """
      try:
          response = httpx.post(
              url=f"{self.base_url}/requestReview",
              headers=self.get_headers(),
              json=self.get_body(),
              timeout=20.0
          )
          response.raise_for_status()
          return response.json()
      except httpx.RequestError as exc:
          raise Exception(f"A network error occurred while requesting {exc.request.url!r}.")
      except httpx.HTTPStatusError as exc:
          raise Exception(f"Error response {exc.response.status_code}:{exc} while requesting {exc.request.url!r}.")
      except httpx.TimeoutException as exc:
          raise Exception(f"Timeout Error: {exc}")

    async def async_send_request(self) -> Dict[str, Any]:
      """
      Send the review request asynchronously to the API.
      
      Returns:
          Dict[str, Any]: The response from the API as a dictionary.
      Raises:
          Exception: If a network, HTTP, or timeout error occurs.
      """
      try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(f"{self.base_url}/requestReview", headers=self.get_headers(), json=self.get_body())
            response.raise_for_status()
            return response.json()
      except httpx.RequestError as exc:
          raise Exception(f"A network error occurred while requesting {exc.request.url!r}: {exc}")
      except httpx.HTTPStatusError as exc:
          raise Exception(f"Error response {exc.response.status_code}:{exc} while requesting {exc.request.url!r}.")
      except httpx.TimeoutException as exc:
          raise Exception(f"Timeout Error: {exc}")

    def get_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
        }

    def get_body(self) -> Dict[str, Any]:
      return {
          'formId': self.form_id,
          'fields': self.fields,
          'meta': self.meta,
          **({'assignTo': self.assign_to} if self.assign_to else {}),
          **({'assignToGroups': self.assign_to_groups} if self.assign_to_groups else {}),
          **({'updateForReviewId': self.review_id_to_update} if self.review_id_to_update is not None else {}),
          'millis': int(time.time() * 1000),
          'origin': "py-sdk",
          'originV': __version__,
      }

class GotoHuman:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize a GotoHuman instance.
        
        Args:
            api_key (str, optional): The API key for authentication. If not provided, will use the GOTOHUMAN_API_KEY environment variable.
        Raises:
            ValueError: If no API key is provided or found in the environment.
        """
        self.api_key = api_key or os.getenv('GOTOHUMAN_API_KEY')
        if not self.api_key:
            raise ValueError('Please pass an API key or set it in the environment variable GOTOHUMAN_API_KEY')
        self.base_url = os.getenv('GOTOHUMAN_BASE_URL', 'https://api.gotohuman.com')

    def create_review(self, form_id: str) -> Review:
        """
        Create a new Review instance for the specified form ID / review template ID.
        
        Args:
            form_id (str): The ID of the form / review template to use for the review.
        Returns:
            Review: A new Review instance.
        Raises:
            ValueError: If no form ID is provided.
        """
        if not form_id:
            raise ValueError('Please pass a form ID')
        return Review(form_id, self.api_key, self.base_url)