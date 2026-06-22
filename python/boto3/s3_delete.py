import boto3
import json
import random
from datetime import datetime, timedelta
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, as_completed
# from IPython import embed
s3_client = boto3.client("s3")

buckets = [
    "my-bucket",
]

prefixes = [
    "path/to/files/",
]

random.shuffle(prefixes)

def list_common_prefixes(s3_bucket, prefix):
    s3_client = boto3.client("s3")
    response = s3_client.list_object_versions(Bucket=s3_bucket, Prefix=prefix, Delimiter='/')
    common_prefixes = response.get('CommonPrefixes', [])

    return [common_prefix["Prefix"] for common_prefix in common_prefixes]

def pretty_print(s3_bucket, response):
    # print(json.dumps(response, indent=2))
    print(f"s3://{s3_bucket}/{response['Deleted'][-1]['Key']}")

def delete(s3_bucket: str, prefix: str):
    s3_client = boto3.client("s3")
    paginator = s3_client.get_paginator("list_object_versions")

    page_iterator = paginator.paginate(Bucket=s3_bucket, Prefix=prefix)

    for page in page_iterator:
        if 'Versions' in page:
            versions = page['Versions']

            objects_to_delete = list(map(lambda o: {"Key": o["Key"], "VersionId": o["VersionId"]}, versions))

            if objects_to_delete:
                response = s3_client.delete_objects(Bucket=s3_bucket, Delete={"Objects": objects_to_delete})
                pretty_print(s3_bucket, response)

        if 'DeleteMarkers' in page:
            delete_markers = page['DeleteMarkers']

            objects_to_delete = list(map(lambda o: {"Key": o["Key"], "VersionId": o["VersionId"]}, delete_markers))

            if objects_to_delete:
                response = s3_client.delete_objects(Bucket=s3_bucket, Delete={"Objects": objects_to_delete})
                pretty_print(s3_bucket, response)

if __name__ == '__main__':
    # for s3_bucket in buckets:
    #     for prefix in prefixes:
    #         key_markers = [*"0123456789abcdef"]

    #         arguments = [(s3_bucket, f"{prefix}{key_marker}") for key_marker in key_markers]

    #         with Pool(processes=8) as pool:
    #             pool.starmap(delete, arguments)

    #         # delete(s3_bucket, prefix)

    for prefix in prefixes:
        for s3_bucket in buckets:
            common_prefixes = list_common_prefixes(s3_bucket, prefix)

            while len(common_prefixes) > 0:
                arguments = [(s3_bucket, common_prefix) for common_prefix in common_prefixes]

                try:
                    with Pool(processes=4) as pool:
                        pool.starmap(delete, arguments)
                except Exception as e:
                    pass

                common_prefixes = list_common_prefixes(s3_bucket, prefix)

            delete(s3_bucket, prefix)
