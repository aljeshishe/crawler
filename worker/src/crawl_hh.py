import io
import logging
import os
import re
from datetime import datetime
import boto3
import pandas as pd
import requests

log = logging.getLogger(__name__)
df = pd.DataFrame(
    data={"Title": ["Book I", "Book II", "Book III"], "Price": [56.6, 59.87, 74.54]},
    columns=["Title", "Price"],
)
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")



def s3fs():
    import s3fs

    fs = s3fs.S3FileSystem(
        anon=False,
        use_ssl=True,
        client_kwargs={
            "region_name": "eu-central-1",
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            # "verify": True,
        }
    )
    print(fs.ls(''))
    fs.read_bytes("crawler-data-7892h32/package.json")
    fs.write_text(f"s3://{AWS_S3_BUCKET}/myfile.txt", "Hello World")
    return


    key = "file.csv"
    df.to_csv(
        f"s3://{AWS_S3_BUCKET}/{key}",
        index=False,
        storage_options={
            "key": AWS_ACCESS_KEY_ID,
            "secret": AWS_SECRET_ACCESS_KEY,
            "asynchronous": False
        })


def handler():
    print("\n".join(f"{k}={v}" for k, v in sorted(os.environ.items())))
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    url = "https://hh.ru/search/vacancy?text=python&salary=&clusters=true&area=1001&area=2&ored_clusters=true&enable_snippets=true"
    resp = requests.get(url=url, headers=headers)
    resp.raise_for_status()
    result = int(re.search("'vacancies_found': '(\d+)'", resp.text).group(1))
    print(result)

    key = f'data.csv'
    s3_client = boto3.client("s3")
    try:
        response = s3_client.get_object(Bucket=AWS_S3_BUCKET, Key=key)
        status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        assert status_code == 200, f"HTTPStatusCode={status_code} expected:200"
        df = pd.read_csv(io.BytesIO(response["Body"].read()))
    except s3_client.exceptions.NoSuchKey as e:
        df = pd.DataFrame(columns=['dt', 'count'])

    df = df.append(dict(dt=datetime.utcnow(), count=result), ignore_index=True)

    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

        response = s3_client.put_object(
            Bucket=AWS_S3_BUCKET, Key=key, Body=csv_buffer.getvalue()
        )

        status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        assert status_code == 200, f"HTTPStatusCode={status_code} expected:200"


    # wrangle implementation
    # path = f's3://{AWS_S3_BUCKET}/data.csv'
    # try:
    #     df = wr.s3.read_csv(path=path)
    # except awswrangler.exceptions.NoFilesFound:
    #     df = pd.DataFrame(columns=['dt', 'count'])

    # df = df.append(dict(dt=datetime.utcnow(), count=result), ignore_index=True)
    # wr.s3.to_csv(df=df, path=path)

    # boto3_save_csv()
    # save2()
    # AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    # df = pd.DataFrame()
    # df.to_csv(f"s3://{AWS_S3_BUCKET}/crawl_hh/data.zip")



def save2():
    import boto3

    some_binary_data = b"Here we have some data"

    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    s3 = boto3.resource("s3")
    object = s3.Object(bucket_name=AWS_S3_BUCKET, key="test.txt")
    object.put(Body=some_binary_data)


def boto3_save_csv():
    # with io.StringIO() as csv_buffer:
    #     df.to_csv(csv_buffer, index=False)
    #
    #     s3_client = boto3.client(
    #         "s3",
    #         aws_access_key_id=AWS_ACCESS_KEY_ID,
    #         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    #         # aws_session_token=AWS_SESSION_TOKEN,
    #     )
    #     response = s3_client.put_object(
    #         Bucket=AWS_S3_BUCKET, Key="files/books.csv", Body=csv_buffer.getvalue()
    #     )
    #
    #     status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    #
    #     if status == 200:
    #         print(f"Successful S3 put_object response. Status - {status}")
    #     else:
    #         print(f"Unsuccessful S3 put_object response. Status - {status}")

    a = df.to_csv(
        f"s3://{AWS_S3_BUCKET}/test.csv",
        index=False,
        storage_options={
            "key": AWS_ACCESS_KEY_ID,
            "secret": AWS_SECRET_ACCESS_KEY,
        },
    )
    print(a)


if __name__ == "__main__":
    handler()
