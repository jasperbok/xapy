# encoding: utf-8
import requests


class Client:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get(self, endpoint: str):
        url = "https://xapi.us/v2{}".format(endpoint)
        headers = {
            "X-AUTH": self.api_key,
            "Accept-Language": "nl-NL"
        }

        res = requests.get(url, headers=headers)
        res.raise_for_status()

        return res.json()

    def get_profile(self):
        """Return profile information for the authenticated user."""
        return self._get("/profile")
