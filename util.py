import boto3

from typing import Iterator


def aws_profiles() -> Iterator[str]:
    """Yield all profile names that can be found in the current config file."""
    s = boto3.Session()
    yield from s.available_profiles
