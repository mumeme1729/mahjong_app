import os
from os.path import join, dirname
from dotenv import load_dotenv

env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")