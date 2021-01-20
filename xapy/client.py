# encoding: utf-8
import requests


class Client:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get(self, endpoint: str, return_response=False):
        url = "https://xapi.us/v2{}".format(endpoint)
        headers = {
            "X-AUTH": self.api_key,
            "Accept-Language": "nl-NL"
        }

        res = requests.get(url, headers=headers)
        res.raise_for_status()

        if return_response:
            return res
        return res.json()

    def get_profile(self):
        """Return profile information for the authenticated user."""
        return self._get("/profile")

    def get_account_xuid(self):
        """Return the Xbox User ID of the authenticated user."""
        return self._get("/accountXuid")

    def get_messages(self):
        """Return the messages for the authenticated user."""
        return self._get("/messages")

    def get_conversations(self):
        """Return the conversations for the authenticated user."""
        return self._get("/conversations")

    def get_xuid_for_gamertag(self, gamertag: str):
        """Return the Xbox User ID that belongs to a specific gamertag."""
        return self._get("/xuid/{}".format(gamertag))

    def get_gamertag_for_xuid(self, xuid: str) -> str:
        """Return the gamertag that belongs to a specific Xbox User ID."""
        res = self._get("/gamertag/{}".format(xuid), return_response=True)
        return res.text
