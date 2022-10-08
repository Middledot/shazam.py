"""
The MIT License (MIT)

Copyright (c) 2020-2022 marin-m
Copyright (c) 2021-2022 Numenorean
Copyright (c) 2022-present Middledot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import uuid
import time
import requests
import aiohttp

from typing import Dict, Iterator, Tuple

from .shazam import make_signature_from_buffer, DecodedSignature

# this is a country so uh yeah
LANG = 'us'
TIME_ZONE = 'EST'

class Endpoint:
    SCHEME = 'https'
    HOSTNAME = 'amp.shazam.com'

    def __init__(
        self,
        lang: str,
        timezone: str
    ):
        self.lang = lang
        self.time_zone = timezone

    @property
    def url(self) -> str:
        return (
            f'{self.SCHEME}://{self.HOSTNAME}'
            '/discovery/v5'
            f'/{self.lang}/{self.lang.upper()}'
            '/iphone/-/tag/{uuid_a}/{uuid_b}'
        )

    @property
    def params(self) -> dict:
        return {
            'sync': 'true',
            'webv3': 'true',
            'sampling': 'true',
            'connected': '',
            'shazamapiversion': 'v3',
            'sharehub': 'true',
            'hubv5minorversion': 'v5.1',
            'hidelb': 'true',
            'video': 'v3'
        }

    @property
    def headers(self) -> dict:
        return {
            "X-Shazam-Platform": "IPHONE",
            "X-Shazam-AppVersion": "14.1.0",
            "Accept": "*/*",
            "Accept-Language": self.lang,
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Shazam/3685 CFNetwork/1197 Darwin/20.0.0"
        }


class _BaseShazam:
    MAX_TIME_SECONDS = 8

    def __init__(
        self,
        song_data: bytes,
        *,
        lang: str = LANG,
        timezone: str = TIME_ZONE,
    ):
        self.song_data = song_data
        self.result = None
        self._endpoint = Endpoint(lang, timezone)

    def get_payload(self, sig) -> dict:
        return {
            'timezone': self._endpoint.time_zone,
            'signature': {
                'uri': sig.encode_to_uri(),
                'samplems': int(sig.number_samples / sig.sample_rate_hz * 1000)
            },
            'timestamp': int(time.time() * 1000),
            'context': {},
            'geolocation': {}
        }


class Shazam(_BaseShazam):
    def __init__(self, *args, **kwargs):
        session = kwargs.pop("session", None)
        super().__init__(*args, **kwargs)

        self.session = session
        self._created = False
        if not session:
            self._created = True
            self.session = requests.Session()

    def execute(self) -> dict:
        sig = make_signature_from_buffer(self.song_data)
        result = self.send_request(sig)

        return result

    def send_request(self, sig: DecodedSignature) -> dict:
        data = self.get_payload(sig)

        r = self.session.post(
            self._endpoint.url.format(
                uuid_a=str(uuid.uuid4()).upper(),
                uuid_b=str(uuid.uuid4()).upper()
            ),
            params=self._endpoint.params,
            headers=self._endpoint.headers,
            json=data
        )

        return r.json()

    def __enter__(self):
        self.result = self.execute()

        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        if self._created:
            self.session.close()


class AsyncShazam(_BaseShazam):
    def __init__(self, *args, **kwargs):
        session = kwargs.pop("session", None)
        super().__init__(*args, **kwargs)

        self.session = session
        self._created = False
        if not session:
            self._created = True
            self.session = aiohttp.ClientSession()

    async def execute(self) -> Iterator[Tuple[float, Dict]]:
        sig = make_signature_from_buffer(self.song_data)
        result = await self.send_request(sig)

        return result

    async def send_request(self, sig: DecodedSignature) -> dict:
        data = self.get_payload(sig)

        r = await self.session.post(
            self._endpoint.url.format(
                uuid_a=str(uuid.uuid4()).upper(),
                uuid_b=str(uuid.uuid4()).upper()
            ),
            params=self._endpoint.params,
            headers=self._endpoint.headers,
            json=data
        )

        return await r.json()

    async def __aenter__(self):
        self.result = await self.execute()

        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        if self._created:
            await self.session.close()
