from pathlib import Path
import boto3
from io import BytesIO
from PIL import Image
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BUCKET_NAME = 'cot'

s3 = boto3.client(
    's3', 
    endpoint_url='http://minio:9000', 
    aws_access_key_id='access-key', 
    aws_secret_access_key='secret-key'
)


def generate_cat_meme(i):
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )

    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        img_response = session.get("https://cataas.com/cat/says/%D0%91%D1%83!%20%D0%98%D1%81%D0%BF%D1%83%D0%B3%D0%B0%D0%BB%D1%81%D1%8F%3F?fontSize=50&fontColor=white", timeout=10)
        img_response.raise_for_status()
        img = Image.open(BytesIO(img_response.content))

        img.save(f"cat_meme_{i}.jpg")
        if Path(f"cat_meme_{i}.jpg").exists():
            s3.upload_file(f"cat_meme_{i}.jpg", BUCKET_NAME, f"cat_meme_{i}.jpg")

    except ValueError as ve:
        print(f"Value error occurred: {ve}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

try:
    s3.create_bucket(Bucket=BUCKET_NAME)
except Exception as e:
    pass
    # print(f"Bucket {BUCKET_NAME} already exists or error: {e}")

for i in range(1000):
    generate_cat_meme(i)
    print(f"Generated cat meme {i}")
