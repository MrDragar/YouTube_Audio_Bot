import logging
import json

from dotenv import dotenv_values

config = dotenv_values(".env")

API_TOKEN = config["API_TOKEN"]
ADMINS_ID = json.loads(config["ADMINS_ID"])

logging.basicConfig(level=logging.INFO)
