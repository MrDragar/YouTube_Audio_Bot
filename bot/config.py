import logging
import json

from dotenv import dotenv_values

config = dotenv_values(".env")

API_TOKEN = config["API_TOKEN"]
ADMINS_ID = json.loads(config["ADMINS_ID"])
CHANNEL_ID = json.loads(config["CHANNEL_ID"])
BROWSERS = json.loads(config["BROWSERS"])
DEBUG = (config["DEBUG"]).lower().strip() == "true"
WEBHOOK_HOST = config["WEBHOOK_HOST"]
WEBHOOK_PORT = int(config["WEBHOOK_PORT"])

print(BROWSERS)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)

