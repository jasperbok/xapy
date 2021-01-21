# encoding: utf-8
class Achievement:

    def __init__(self, name: str, locked_description: str, description: str, gamerscore: int, is_secret: bool,
                 is_unlocked: bool, image_url: str):
        """Create a new Achievement.

        :param name: The achievement's name
        :param locked_description: The achievement's description while it's locked
        :param description: The achievement's description after it's unlocked
        :param gamerscore: The gamerscore value of the achievement
        :param is_secret: Whether this is a secret achievement
        :param is_unlocked: Whether the achievement has been unlocked
        :param image_url: A hyperlink to the achievement's icon image
        :type name: str
        :type locked_description: str
        :type description: str
        :type gamerscore: int
        :type is_secret: bool
        :type is_unlocked: bool
        :type image_url: str
        """
        self.name = name
        self.locked_description = locked_description
        self.description = description
        self.gamerscore = gamerscore
        self.is_secret = is_secret
        self.is_unlocked = is_unlocked
        self.image_url = image_url

    def __repr__(self):
        return 'Achievement "{}"'.format(self.name)

    def __str__(self):
        return self.name

    @staticmethod
    def from_api_response(json_data: dict):
        """Create an achievement from a JSON response.

        This method determines whether the JSON contains an Xbox 360 or
        an Xbox One achievement and returns a normalized instance of the
        Achievement class based on this data.

        :param json_data: The JSON response.
        :type json_data: dict
        :raise NotImplementedError: If the type of the achievement
        cannot be determined a NotImplementedError will be raised.
        """
        if 'progressState' in json_data:  # progressState was added for Xbox One achievements.
            return Achievement._from_xboxone_api_data(json_data)
        elif 'flags' in json_data:  # flags only appeared in Xbox 360 achievements.
            return Achievement._from_xbox360_api_data(json_data)
        else:
            raise NotImplementedError('Unable to determine the type of the achievement')

    @staticmethod
    def _from_xbox360_api_data(json_data):
        return Achievement(
            json_data['name'],
            json_data['lockedDescription'],
            json_data['description'],
            json_data['gamerscore'],
            json_data['isSecret'],
            json_data['unlocked'],
            json_data['imageUnlocked']
        )

    @staticmethod
    def _from_xboxone_api_data(json_data):
        gamerscore = 0
        for reward in json_data['rewards']:
            if reward['name'] == 'Gamerscore':
                gamerscore = reward['value']
                break

        icon_url = ''
        for asset in json_data['mediaAssets']:
            if asset['type'] == 'Icon':
                icon_url = asset['url']
                break

        return Achievement(
            json_data['name'],
            json_data['lockedDescription'],
            json_data['description'],
            gamerscore,
            json_data['isSecret'],
            json_data['progressState'] == 'Achieved',
            icon_url
        )
