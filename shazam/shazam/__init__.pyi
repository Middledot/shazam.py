"""
The MIT License (MIT)

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


# Stub file for rust implementation
# idk how to change the submodule name
# so it's also called shazam for now

from typing import Dict, List, Literal


class FrequencyPeak:
    fft_pass_number: int
    peak_magnitude: int
    corrected_peak_frequency_bin: int
    sample_rate_hz: int

    def get_frequency_hz(self) -> float: ...
    def get_amplitude_pcm(self) -> float: ...
    def get_seconds(self) -> float: ...


# before you ask I don't actually know
class FrequencyBand:
    _250_520: Literal[0]
    _520_1450: Literal[1]
    _1450_3500: Literal[2]
    _3500_5500: Literal[3]


class DecodedSignature:
    sample_rate_hz: int
    number_samples: int
    frequency_band_to_sound_peaks: Dict[FrequencyBand, List[FrequencyPeak]]

    @staticmethod
    def decode_from_binary(data: bytes) -> DecodedSignature: ...
    @staticmethod
    def decode_from_uri(uri: str) -> DecodedSignature: ...
    def encode_to_binary(self) -> bytes: ...
    def encode_to_uri(self) -> str: ...


def make_signature_from_buffer(bytes: bytes) -> DecodedSignature: ...
