from pathlib import Path
from typing import Any



class Config:
    _isintance = None
    _dictionary = {}

    def __new__(cls):
        if cls._isintance is None:
            cls._isintance = super(Config, cls).__new__(cls)

            config_path = Path(__file__).parents[4] / 'resourses' / 'urls.properties'

            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found at {config_path}")

            with open(config_path, "r") as file:
                for line in file:
                    if "=" in line:
                        key, value = line.split("=")
                        cls._dictionary[key] = value.strip()

        return cls._isintance


    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
        return Config()._dictionary.get(key, default_value)