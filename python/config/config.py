#!/usr/bin/python3
# coding= utf-8
""" config file """
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """ This class defines settings """
    
    # Uvicorn Server details
    uvicorn_host: str = "127.0.0.1"
    uvicorn_port: int = 8000

    # redis specific variables
    redis_host: str = "localhost"
    redis_port: str = "6379"

    @classmethod
    def get_settings(cls):
        """ get setting """
        return Settings()