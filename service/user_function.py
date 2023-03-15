# Standard Library Imports
import os
import re
import json
import time
import base64
import urllib.parse
import logging
from enum import Enum
from pprint import pprint
from typing import List
from pathlib import Path

# Third-Party Imports
import boto3
import requests

# Project-Level Imports
from service.utils import process_normal, process_via_threading
from service.user_model import User

# filename = Path(__file__).stem
# logger = logging.getLogger(filename)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logging.basicConfig()

BASE_URL = "https://random-data-api.com/api/v2/"


class ContentType(Enum):
    text_html = "text/html"
    zip = "application/zip"
    json = "application/json"


class ApiResources(Enum):
    users = "users"
    address = "addresses"
    banks = "banks"
    appliances = "appliances"
    beers = "beers"
    blood_types = "blood_types"
    credit_cards = "credit_cards"


def handler(event, context):
    logger.info(
        f'Event: {event["httpMethod"]}, {event["queryStringParameters"]}, {event["body"]}'
    )
    logger.info(f"Context: {context}")

    my_page = page_router(http_method=event["httpMethod"], body=event["body"])

    return my_page


def page_router(
    http_method,
    body,
):

    if http_method == "GET":
        logger.info("GET received")

        html_path = os.path.join(os.path.dirname(__file__), "index.html")
        html_file = open(html_path, "r")
        html_content = html_file.read()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": ContentType.text_html.value},
            "body": html_content,
        }

    if http_method == "POST":
        logger.info("POST received")

        new_body = urllib.parse.parse_qs(body)
        user_num = next(iter(new_body.get("user_num", [])), None)
        logger.info(f"user_num: {user_num}")

        users = call_api(user_num)

        # path = os.path.join(os.path.dirname(__file__), "tmp")
        # logger.info(f"Writing to {path}")

        # process pool executor
        # process_via_threading(path=path, data_list=users)
        # process_normal(path=path, data_list=users)

        # files = bytes("", "utf-8")
        # zip_file = base64.b64encode(files).decode("ascii")
        #
        # return {
        #     "statusCode": 200,
        #     "headers": {"Content-Type": ContentType.zip.value},
        #     "body": zip_file,
        # }

        names = [f"{user.last_name}, {user.first_name}" for user in users]

        return {
            "statusCode": 200,
            "headers": {"Content-Type": ContentType.json.value},
            "body": json.dumps(names),
        }


def call_api(user_num) -> List[User]:

    params = {
        "size": user_num,
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
