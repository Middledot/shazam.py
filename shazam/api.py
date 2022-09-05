import asyncio
import uuid
import time
import requests
import aiohttp
from pydub import AudioSegment
from io import BytesIO

from typing import Dict, Iterator, Tuple

from .algorithm import SignatureGenerator
from .signature_format import DecodedMessage

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
        execute: bool = True,
        
        lang: str = LANG,
        timezone: str = TIME_ZONE,
    ):
        self.song_data = song_data
        self._execute = execute
        self.results = None
        self._endpoint = Endpoint(lang, timezone)

    def normalize_audio_data(self, song_data: bytes) -> AudioSegment:
        audio: AudioSegment = AudioSegment.from_file(BytesIO(song_data))  # TODO: remove typehint

        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        return audio

    def create_signature_generator(self, audio: AudioSegment) -> SignatureGenerator:
        signature_generator = SignatureGenerator()
        signature_generator.feed_input(audio.get_array_of_samples())
        signature_generator.MAX_TIME_SECONDS = self.MAX_TIME_SECONDS
        if audio.duration_seconds > 12 * 3:
            signature_generator.samples_processed += 16000 * (int(audio.duration_seconds / 16) - 6)
        return signature_generator


class Shazam(_BaseShazam):
    def __init__(self, *args, **kwargs):
        session = kwargs.pop("session", None)
        super().__init__(*args, **kwargs)

        self.session = session
        self._created = False
        if not session:
            self._created = True
            self.session = requests.Session()

    def execute(self) -> Iterator[Tuple[float, Dict]]:
        self.audio = self.normalize_audio_data(self.song_data)
        signatureGenerator = self.create_signature_generator(self.audio)
        while True:
            signature = signatureGenerator.get_next_signature()
            if not signature:
                break

            results = self.send_request(signature)
            currentOffset = signatureGenerator.samples_processed / 16000

            yield currentOffset, results

    def send_request(self, sig: DecodedMessage) -> dict:
        data = {
            'timezone': self._endpoint.time_zone,
            'signature': {
                'uri': sig.encode_to_uri(),
                'samplems': int(sig.number_samples / sig.sample_rate_hz * 1000)
            },
            'timestamp': int(time.time() * 1000),
            'context': {},
            'geolocation': {}
        }

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

    def __iter__(self):
        return self.results

    def __enter__(self):
        if self._execute:
            self.results = self.execute()

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
        self.audio = self.normalize_audio_data(self.song_data)
        signatureGenerator = self.create_signature_generator(self.audio)
        while True:
            signature = signatureGenerator.get_next_signature()
            if not signature:
                break

            results = await self.send_request(signature)
            currentOffset = signatureGenerator.samples_processed / 16000

            yield currentOffset, results

    async def send_request(self, sig: DecodedMessage) -> dict:
        data = {
            'timezone': self._endpoint.time_zone,
            'signature': {
                'uri': sig.encode_to_uri(),
                'samplems': int(sig.number_samples / sig.sample_rate_hz * 1000)
            },
            'timestamp': int(time.time() * 1000),
            'context': {},
            'geolocation': {}
        }

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

    def __aiter__(self):
        return self.results

    async def __aenter__(self):
        if self._execute:
            self.results = self.execute()

        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        if self._created:
            await self.session.close()
