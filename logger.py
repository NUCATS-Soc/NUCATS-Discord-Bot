import logging
import os

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


class Logger:
    """Simple static class used to create and store loggers."""

    loggers: "dict[str, logging.Logger]" = {}

    @classmethod
    def get_logger(
        cls, name: "str", file: "str" = "logs/logs.log", level: "logging._Level" = logging.INFO
    ) -> "logging.Logger":
        """Get a file logger with the given name and level.
        The name should be the name of the module that is using the logger.

        ```py
        # Example usage
        logger = Logger.get_logger(__name__)
        logger.info("Hello world!")
        ```

        :param name: name of the logger. Should be the name of the module using the logger.
        :param file: file to log to, defaults to "logs/server/logs.log". If None, it will not log to a file.
        :param level: the logger will output messages up unitl this level, defaults to logging.INFO
        :return: existing logger with the given name or a new logger if one does not exist
        """
        if name not in cls.loggers:
            cls.loggers[name] = logging.getLogger(name)
            cls.loggers[name].setLevel(level)
            if file is not None:
                os.makedirs(os.path.dirname(file), exist_ok=True)
                handler = logging.FileHandler(file)
                handler.setLevel(level)
                formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                handler.setFormatter(formatter)
                cls.loggers[name].addHandler(handler)
        return cls.loggers[name]
