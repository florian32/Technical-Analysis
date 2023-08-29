import os


class Config:
    MARKETAUX_ENDPOINT: str = os.getenv("MARKETAUX_ENDPOINT")
    MARKETAUX_TOKEN: str = os.getenv("MARKETAUX_TOKEN")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    SMOOTHING = 3
    WINDOW_RANGE = 1


config = Config()
