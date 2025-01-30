import os
import requests
import json

from anypy.object import Object
from anypy.space import Space
from anypy.relation import Relation
from anypy.type import Type


class Anytype:
    def __init__(self):
        self.app_name = ''
        self.space_id = ''
        self.token = ''
        self.app_key = ''
        self.headers = {}

    def auth(self):
        userdata = self._get_userdata_folder()
        anytoken = os.path.join(userdata, "any_token.json")
        if self.app_name == "":
            self.app_name = "Python API"

        if os.path.exists(anytoken):
            auth_json = json.load(open(anytoken))
            self.token = auth_json.get("session_token")
            self.app_key = auth_json.get("app_key")
            if self._validate_token():
                return

        url = f"http://localhost:31009/v1/auth/display_code?app_name={self.app_name}"
        response = requests.post(url)
        if response.status_code != 200:
            raise Exception("Error: ", response.json())

        api_four_digit_code = input("Enter the 4 digit code: ")
        challenge_id = response.json().get("challenge_id")
        url = f"http://localhost:31009/v1/auth/token?challenge_id={challenge_id}&code={api_four_digit_code}"
        response = requests.post(url)
        if response.status_code != 200:
            raise Exception("Error: ", response.json())

        with open(anytoken, "w") as file:
            json.dump(response.json(), file, indent=4)
        self.token = response.json().get("session_token")
        self.app_key = response.json().get("app_key")
        self._validate_token()

    def _validate_token(self):
        url = "http://localhost:31009/v1/spaces?offset=0&limit=500"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.app_key}"
        }
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Token validation failed: {e}")
            return False

    def _get_userdata_folder(self):
        userdata = os.path.join(os.path.expanduser("~"), ".anytype")
        if not os.path.exists(userdata):
            os.makedirs(userdata)
        return userdata

    def get_spaces(self, offset=0, limit=10):
        api_url = "http://localhost:31009/v1"
        url = f"{api_url}/spaces/"
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception("Error: ", response.json())

        results = []
        for data in response.json().get("data", []):
            new_item = Space()
            new_item._headers = self.headers
            for key, value in data.items():
                if key == "blocks":
                    new_item.__dict__[key] = value
                else:
                    new_item.__dict__[key] = value
            results.append(new_item)

        return results
