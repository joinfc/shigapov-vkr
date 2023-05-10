#!/usr/bin/python

"""Публикация в качестве бессерверной функции"""

import os
from tomllib import load

files = [
    "*.py",
    "config.ini"
    "requirements.txt",
]

os.system("zip function.zip {' '.join(files)}")

with open("config.ini", mode="rb") as f:
    config = load(f)

os.system(
    "yc serverless function version create"
    f" --cloud-id {config['CLOUD_ID']}"
    f" --folder-name {config['FOLDER_NAME']}"
    f" --function-name {config['FUNCTION_NAME']}"
    " --runtime python311"
    " --entrypoint main.lambda_handler"
    " --memory 128MB"
    " --execution-timeout 5s"
    " --source-path function.zip"
    " --environment"
    f" BOT_TOKEN='{config['TOKEN']}'"
)

os.system("function.zip")

os.system(
    f"curl https://api.telegram.org/bot{config['TOKEN']}/"
    f"setWebhook?url={config['URL']}"
)
