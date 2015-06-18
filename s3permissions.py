#!/usr/bin/python3

import boto3
import json
from terminaltables import DoubleTable

client = boto3.client('s3')
bucket_list = client.list_buckets()


def analyze_bucket(bucket):
    bucket_location = client.get_bucket_location(Bucket=bucket)['LocationConstraint']
    new_client = boto3.client('s3', region_name=bucket_location)
    bucket_acl = new_client.get_bucket_acl(Bucket=bucket)
    permission = []

    for grants in bucket_acl['Grants']:

        if ('URI' in grants['Grantee']) and ('AllUser' in grants['Grantee']['URI']):
            permission.append(grants['Permission'])

    if len(permission) == 1:

        if permission[0] == 'READ':
            globalListAccess = 'YES'
            globalWriteAccess = 'NO'

        table_data = [
            ['BucketName', 'Region', 'GlobalListAccess', 'GlobalWriteAccess'],
            [bucket, bucket_location, globalListAccess, globalWriteAccess],
        ]
        table = DoubleTable(table_data)
        table.inner_row_border = True
        print(table.table)

    elif len(permission) > 1:

        if permission[0] == 'READ':
            globalListAccess = 'YES'
        if permission[1] == 'WRITE':
            globalWriteAccess = 'YES'
        else:
            globalWriteAccess = 'NO'

        table_data = [
            ['BucketName', 'Region', 'GlobalListAccess', 'GlobalWriteAccess'],
            [bucket, bucket_location, globalListAccess, globalWriteAccess],

        ]
        table = DoubleTable(table_data)
        table.inner_row_border = True
        print(table.table)

def connect_s3():
    client = boto3.resource('s3')

    for bucket in client.buckets.all():
        analyze_bucket(bucket.name)


if __name__ == "__main__":
    try:
        print()
        connect_s3()
    except Exception as err:
        print(err)

