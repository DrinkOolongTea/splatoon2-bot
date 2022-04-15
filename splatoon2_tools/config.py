import os
from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    resource_path: str = os.path.join(os.path.dirname(__file__), "resource")

    class Config:
        extra = "ignore"
