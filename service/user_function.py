import json
import os
import re
import base64
import boto3
import requests
import logging
from pathlib import Path
from enum import Enum
from pprint import pprint
from user_model import User
from utils import process_via_threading, process_normal
import time

# filename = Path(__file__).stem
# logger = logging.getLogger(filename)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logging.basicConfig()

BASE_URL = "https://random-data-api.com/api/v2/"


class ContentType(Enum):
    text_html = "text/html"
    zip = "application/zip"


class ApiResources(Enum):
    users = "users"
    address = "addresses"
    banks = "banks"
    appliances = "appliances"
    beers = "beers"
    blood_types = "blood_types"
    credit_cards = "credit_cards"


def handler(event, context):
    logger.info(f"Event: {event}")

    my_page = page_router(
        event["httpMethod"], event["queryStringParameters"], event["body"]
    )

    return my_page


def page_router(http_method, query_string=None, form_body=None):

    if http_method == "GET":
        logger.info("GET received")

        html_file = open("index.html", "r")
        html_content = html_file.read()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": ContentType.text_html.value},
            "body": html_content,
        }

    if http_method == "POST":
        logger.info("POST received")

        users = call_api()

        path = os.path.join(os.path.dirname(__file__), "tmp")
        logger.info(f"Writing to {path}")

        # process pool executor
        # process_via_threading(path=path, data_list=users)
        process_normal(path=path, data_list=users)

        # files = bytes("", "utf-8")
        # zip_file = base64.b64encode(files).decode("ascii")
        #
        # return {
        #     "statusCode": 200,
        #     "headers": {"Content-Type": ContentType.zip.value},
        #     "body": zip_file,
        # }


def call_api():

    params = {
        "size": 50,
    }
    url = f"{BASE_URL}{ApiResources.users.value}"

    logger.info("Calling API")

    response = requests.get(url=url, params=params).json()

    if not response:
        logger.error("Issue calling API", exc_info=True)

    logger.info(f"Call successful. Creating {len(response)} users.")

    return [User.parse_obj(user) for user in response]


# if __name__ == "__main__":
#     start_time = time.time()
#     page_router("POST")
#     print("--- %s seconds ---" % (time.time() - start_time))
