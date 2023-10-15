import os
from typing import TYPE_CHECKING, overload

from dotenv import load_dotenv

if TYPE_CHECKING:
    from typing import Literal

    ListConfigKey = Literal[
        "COMMITTEE_GROUP",
        "CODEWARS_GROUP",
    ]
    ConfigKey = Literal[
        "TOKEN",
        "GOOGLE_AUTH_PASSWORD",
        "MYSQL_HOST",
        "MYSQL_USER",
        "MYSQL_PASSWORD",
        "MYSQL_DATABASE",
        "MYSQL_ROOT_PASSWORD",
        "SERVER_ID",
        "BOT_TESTING_CHANNEL",
        "COMMITTEE_CHANNEL",
        "DRAFT_ANNOUNCEMENTS_CHANNEL",
        "EVENT_PLANNING_CHANNEL",
        "SERVER_UPDATES_CHANNEL",
        "BOT_LOG_CHANNEL",
        "THE_SENATE_VOICE_CHANNEL",
        "INFORMATION_CHANNEL",
        "AUTH_CHANNEL",
        "WELCOME_CHANNEL",
        "ANNOUNCEMENTS_CHANNEL",
        "GENERAL_CHANNEL",
        "ADVICE_CHANNEL",
        "MEMES_CHANNEL",
        "SUGGESTIONS_CHANNEL",
        "TECH_CHAT_CHANNEL",
        "CODING_HELL_CHANNEL",
        "OPPORTUNITIES_CHANNEL",
        "CODEWARS_ANNOUNCEMENTS_CHANNEL",
        "CODEWARS_CHAT_CHANNEL",
        "CODEWARS_LOG_CHANNEL",
        "GAMING_CHANNEL",
        "GAMING_SUGGESTIONS_CHANNEL",
        "STAGE_1_CHANNEL",
        "STAGE_2_CHANNEL",
        "STAGE_3_CHANNEL",
        "PLACEMENT_CHANNEL",
        "MASTERS_AND_POSTGRAD_CHANNEL",
        "LUTHERS_CHANNEL",
        "FIVE_SWANS_VOICE_CHANNEL",
        "QUAYSIDE_VOICE_CHANNEL",
        "KEEL_ROW_VOICE_CHANNEL",
        "MILE_CASTLE_VOICE_CHANNEL",
        "COMMITTEE_ROLE",
        "BOTS_ROLE",
        "VERIFIED_ROLE",
        "MEMBER_ROLE",
        "STAGE_1_ROLE",
        "STAGE_2_ROLE",
        "STAGE_3_ROLE",
        "STAGE_4_ROLE",
        "PLACEMENT_ROLE",
        "POSTGRAD_ROLE",
        "ALUMNI_ROLE",
        "HE_HIM_ROLE",
        "SHE_HER_ROLE",
        "THEY_THEM_ROLE",
        "TESTING_ROLE",
        "NORTHUMBRIA_STUDENT_ROLE",
    ]


class Config:
    """Configuration class.
    It loads the configuration file and provides a typesafe way of accessing
    the config values for the rest of the application.
    """

    __loaded = False

    @classmethod
    def load_config(cls, env_file: "str" = ".env"):
        """Load the configuration by reading the env file and
        putting all the values found in the environment variables.
        It will not override the existing environment variables.

        :param config_file: path to the config file, defaults to ".env"
        """
        load_dotenv(env_file)
        cls.__loaded = True

    @classmethod
    def reload_config(cls, env_file: "str" = ".env"):
        """Reload the configuration by reading the env file and
        putting all the values found in the environment variables.
        It will override the existing environment variables.

        :param config_file: path to the config file, defaults to ".env"
        """
        load_dotenv(env_file, override=True)
        cls.__loaded = True

    @overload
    @classmethod
    def get(cls, key: "ListConfigKey") -> "list[str]":
        ...

    @overload
    @classmethod
    def get(cls, key: "ConfigKey") -> "str":
        ...

    @classmethod
    def get(cls, key: "str") -> "str | list[str]":
        """Get a config value from the environment variables.
        The value will be returned as a string.
        Casting it in the correct type is up to the caller.
        If it is the first time this class is used, it will load the config file
        with the default file name ".env".

        :param key: the key of the config value
        :return: the config value
        """
        if not cls.__loaded:
            cls.load_config()
        if key == "COMMITTEE_GROUP":
            return [
                cls.get("COMMITTEE_CHANNEL"),
                cls.get("DRAFT_ANNOUNCEMENTS_CHANNEL"),
                cls.get("EVENT_PLANNING_CHANNEL"),
                cls.get("SERVER_UPDATES_CHANNEL"),
                cls.get("BOT_LOG_CHANNEL"),
                cls.get("THE_SENATE_VOICE_CHANNEL"),
            ]
        if key == "CODEWARS_GROUP":
            return [
                cls.get("CODEWARS_ANNOUNCEMENTS_CHANNEL"),
                cls.get("CODEWARS_CHAT_CHANNEL"),
                cls.get("CODEWARS_LOG_CHANNEL"),
            ]
        return os.environ.get(key)
