import os
import time

import backoff
import httpx
from openai import OpenAI


def on_backoff(details):
    print(details.__dict__)


class CustomHTTPClient(httpx.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=Exception,
        max_time=60,
        max_tries=5,
        jitter=backoff.full_jitter,
        on_backoff=on_backoff,
    )
    def send(self, request, *args, **kwargs):
        try:
            response = super().send(request, *args, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retry_after = e.response.headers.get("x-ratelimit-reset-tokens", "0.01s")
                retry_after = float(retry_after.replace("s", ""))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
                raise
            else:
                raise


def create_openai_client():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), http_client=CustomHTTPClient())

    assert isinstance(client, OpenAI)
    assert isinstance(client._client, CustomHTTPClient)
    assert isinstance(client.chat._client, OpenAI)
    return client


openai_client = create_openai_client()
