import json
import os, re, base64
import boto3
import logging

logger = logging.getLogger("lambda_function")
logger.setLevel("DEBUG")


def handler(event, context):
    logger.info(f"Event: {event}")

    my_page = page_router(
        event["httpMethod"], event["queryStringParameters"], event["body"]
    )

    return my_page


def page_router(http_method, query_string, form_body):

    if http_method == "GET":
        logger.info("GET received")

        html_file = open("contact_us.html", "r")
        html_content = html_file.read()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html_content,
        }

    if http_method == "POST":
        logger.info("POST received")
        logger.info(f"form_body: {form_body}")

        insert_record(form_body)

        html_file = open("confirm.html", "r")
        html_content = html_file.read()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html_content,
        }


def insert_record(form_body):
    # form_body = form_body.replace("=", "' : '")
    # form_body = form_body.replace("&", "', '")
    # form_body = "INSERT INTO dojotable value {'" + form_body + "'}"
    #
    # client = boto3.client('dynamodb')
    # client.execute_statement(Statement=form_body)
    logger.info(f"Form received.... {form_body}")
