import argparse
import logging

import boto3
import botocore.exceptions
import notch

import util

notch.configure()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description="Find access keys for an AWS user account in all available profiles"
)
parser.add_argument(
    "username", help="The username to use when searching for access keys"
)
args = parser.parse_args()

for profile_name in util.aws_profiles():
    log.info(f"Using profile {profile_name}")
    s = boto3.Session(profile_name=profile_name)
    iam = s.resource("iam")
    user = iam.User(args.username)
    try:
        log.info(f"Looking up access keys for {user.arn}")
    except botocore.exceptions.ClientError as e:
        log.error(e)
        continue
    for key in user.access_keys.all():
        log.info(f"Found access key with id {key.id}")
