# shazam.py

Python library for the [Shazam](https://shazam.com) API. This library is based off of [ShazamAPI](https://github.com/Numenorean/ShazamAPI) and [SongRec](https://github.com/marin-m/SongRec) but some added features.

NOTE: that this is still in its design and development phase. It works and \*could\* be used in production but beware of possible breaking changes.


### Install
```
pip3 install shazam.py
```

If you're on linux, you'll also have to install `pkg-config` and `libasound2-dev` with your preferred package manager.


### Usage

Synchronous Shazam:

```python
from shazam import Shazam

mp3_file = open('a.mp3', 'rb').read()

with Shazam(mp3_file) as shazam:
    print(shazam.result)  # data received from the shazam api
```

A partially-asynchronous method is also provided:
(partially because only requests are done asynchronously and not the signature generation. See [#1](https://github.com/Middledot/shazam.py/issues/1))

```python
from shazam import AsyncShazam

mp3_file = open('a.mp3', 'rb').read()

async with AsyncShazam(mp3_file) as shazam:
    print(shazam.result)
```

There is also support for using your own session objects and using `Shazam` and `AsyncShazam` outside of
a context manager using the execute function.


## Notes on the Shazam API

Shazam's api takes a "signature" of a song to search in their database before returning a result.

If you want to know more about the specifics of the algorithm, you can read the [paper](https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf) written by a co-founder of Shazam.

The implementation of the algorithm was written by @marin-m in [their project](https://github.com/marin-m/SongRec).
It was adapted to work with python through pyo3 here.


### Credits to:

https://github.com/marin-m/SongRec
https://github.com/Numenorean/ShazamAPI
