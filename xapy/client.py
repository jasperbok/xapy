# encoding: utf-8
import requests

from .achievement import Achievement
from .game import Game
from .gamercard import Gamercard


class Client:

    def __init__(self, api_key: str, lang: str = "en-US", xuid: int = None):
        """Create a new Client instance.

        Arguments:
        api_key -- the API key from your xapi.us profile

        Keyword arguments:
        lang -- the language code to send to the API (default "en-US")
        """
        self.api_key = api_key
        self.lang = lang
        self.xuid = xuid

    def _get(self, endpoint: str, return_response=False):
        url = "https://xapi.us/v2{}".format(endpoint)
        headers = {
            "X-AUTH": self.api_key,
            "Accept-Language": self.lang
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

    def get_gamertag_for_xuid(self, xuid: int) -> str:
        """Return the gamertag that belongs to a specific Xbox User ID."""
        res = self._get("/gamertag/{}".format(xuid), return_response=True)
        return res.text

    def get_profile_for_xuid(self, xuid: int):
        """Return profile information for a specific Xbox User ID."""
        return self._get('/{}/new-profile'.format(xuid))

    def get_gamercard_for_xuid(self, xuid: int) -> Gamercard:
        """Return the gamercard for a specific Xbox User ID."""
        return Gamercard.from_api_response(self._get('/{}/gamercard'.format(xuid)))

    def get_xbox360_games_for_xuid(self, xuid: int):
        """Return the list of Xbox 360 games for a specific Xbox User ID."""
        res = self._get('/{}/xbox360games'.format(xuid))
        games = []
        for data in res['titles']:
            games.append(Game(
                data['titleId'],
                data['name'],
                data['totalGamerscore'],
                data['currentGamerscore'],
                data['currentAchievements'],
                Game.XBOX_360
            ))

        return games

    def get_xboxone_games_for_xuid(self, xuid: int):
        """Return the list of Xbox One games for a specific Xbox User ID."""
        res = self._get('/{}/xboxonegames'.format(xuid))
        games = []
        for data in res['titles']:
            if data['platform'] == 'XboxOne' or data['platform'] == 'Durango':  # 'Durango' is a codename for Xbox One.
                platform = Game.XBOX_ONE
            elif data['platform'] == 'WindowsOneCore':
                platform = Game.WINDOWS
            else:
                print(data['platform'])
                platform = Game.UNKNOWN
            games.append(Game(
                data['titleId'],
                data['name'],
                data['maxGamerscore'],
                data['currentGamerscore'],
                data['earnedAchievements'],
                platform
            ))

        return games

    def get_title_achievements_for_xuid(self, xuid: int, title_id: int) -> list[Achievement]:
        """Return the list of a game's achievements.

        :param xuid: An Xbox User ID.
        :param title_id: The ID of the game to retrieve achievements for.
        :type xuid: int
        :type title_id: int
        :return: A list of Achievement objects.
        :rtype: list[Achievement]
        """
        data = self._get('/{}/achievements/{}'.format(xuid, title_id))
        achievements = []

        for achievement_data in data:
            achievements.append(Achievement.from_api_response(achievement_data))

        return achievements
