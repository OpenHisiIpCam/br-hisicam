#!/usr/bin/env python3
import hashlib
import hmac
import time
import os
import urllib.request


KEY_ID = os.getenv("S3_KEY_ID")
KEY = os.getenv("S3_KEY")

if KEY_ID is None and KEY is None:
    keyfile = os.path.join(os.getenv("HOME"), ".s3key")
    with open(keyfile, "r") as f:
        KEY_ID, KEY = f.readline().strip().split(" ")


AWS_HOST = "storage.yandexcloud.net"
AWS_REGION = "ru-central1"
AWS_SERVICE = "s3"


def sha256hash(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    m = hashlib.sha256()
    m.update(data)
    return m.digest()


def sign(key, data):
    if isinstance(key, str):
        key = key.encode("utf-8")
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hmac.digest(key, data, "sha256")


def get_key(secret, scope):
    date, region, service, req = scope.split("/")
    return sign(sign(sign(sign("AWS4" + secret, date), region), service), req)


_signed_headers = ("host", "x-amz-content-sha256", "x-amz-date")


def sign_request(method, uri, host):
    now = time.gmtime()
    timestamp = time.strftime("%Y%m%dT%H%M%SZ", now)
    date = time.strftime("%Y%m%d", now)
    scope = f"{date}/{AWS_REGION}/{AWS_SERVICE}/aws4_request"

    headers = {
        "host": host,
        "x-amz-content-sha256": "UNSIGNED-PAYLOAD",
        "x-amz-date": timestamp
    }

    # make canonical request
    canon = (
        method.upper() + "\n" +
        uri + "\n" +
        "" + "\n"  # no query params
    )
    for h in _signed_headers:
        canon += h + ":" + headers[h] + "\n"
    canon += "\n"
    canon += ";".join(_signed_headers) + "\n"
    canon += "UNSIGNED-PAYLOAD"

    canon_hash = sha256hash(canon.encode("utf-8")).hex()

    data = f"AWS4-HMAC-SHA256\n{timestamp}\n{scope}\n{canon_hash}"

    auth_value = (
        "AWS4-HMAC-SHA256 "
        f"Credential={KEY_ID}/{scope},"
        f"SignedHeaders={';'.join(_signed_headers)},"
        f"Signature={sign(get_key(KEY, scope), data).hex()}"
    )

    headers["Authorization"] = auth_value
    return headers


def make_s3_request(method, uri, host, headers=None, **kwargs):
    if headers is None:
        headers = {}
    headers.update(sign_request(method=method, uri=uri, host=host))
    return urllib.request.Request(
        url=f"https://{host}{uri}",
        headers=headers,
        method=method,
        **kwargs
    )


# -------------------------------------------------------------------------------------------------
def upload(file, bucket, object_key, content_type=None):
    print(f"Upload {file} into {AWS_HOST}/{bucket}/{object_key} ...")
    with open(file, "rb") as f:
        data = f.read()

    headers = {}
    if content_type is not None:
        headers["Content-Type"] = content_type

    req = make_s3_request(
        method="PUT",
        uri=f"/{bucket}/{object_key}",
        host=AWS_HOST,
        headers=headers,
        data=data
    )
    resp = urllib.request.urlopen(req)


# -------------------------------------------------------------------------------------------------
def download(file, bucket, object_key):
    print(f"Download from {AWS_HOST}/{bucket}/{object_key} ...")

    req = make_s3_request(
        method="GET",
        uri=f"/{bucket}/{object_key}",
        host=AWS_HOST
    )

    resp = urllib.request.urlopen(req)
    with open(file, "wb") as f:
        f.write(resp.read())


# -------------------------------------------------------------------------------------------------
class UploadWrap:
    """ Upload file into storage
    """
    @staticmethod
    def add_args(parser):
        parser.add_argument("-f", "--file", help="Source file to be uploaded", metavar="PATH", required=True)
        parser.add_argument("-k", "--object-key", help="Storage object key", metavar="KEY", required=True)
        parser.add_argument("-b", "--bucket", help="Storage bucket", required=True)
        parser.add_argument("-c", "--content-type", help="Content-Type for uploaded file", metavar="MIME")

    @staticmethod
    def run(args):
        upload(args.file, args.bucket, args.object_key, args.content_type)


class DownloadWrap:
    """ Download file from storage
    """
    @staticmethod
    def add_args(parser):
        parser.add_argument("-f", "--file", help="Destination file", metavar="PATH", required=True)
        parser.add_argument("-k", "--object-key", help="Storage object key", metavar="KEY", required=True)
        parser.add_argument("-b", "--bucket", help="Storage bucket", required=True)

    @staticmethod
    def run(args):
        download(args.file, args.bucket, args.object_key)


def main():
    import argparse

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="Action")
    for action in (UploadWrap, DownloadWrap):
        action_parser = subparsers.add_parser(action.__name__[:-4].lower(), help=action.__doc__.strip() if action.__doc__ else None)
        action.add_args(action_parser)
        action_parser.set_defaults(action=action)

    args = parser.parse_args()

    args.action.run(args)


if __name__ == "__main__":
    main()
