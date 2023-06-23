from dotenv import dotenv_values
import logging

config = dotenv_values(".env")

API_TOKEN = config["API_TOKEN"]


logging.basicConfig(level=logging.INFO)
