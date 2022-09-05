# shazam.py

Python library for the [Shazam](https://shazam.com) API. This library is based off of [ShazamAPI](https://github.com/Numenorean/ShazamAPI) by [Numenorean](https://github.com/Numenorean) but some added features.

### Install
```
pip3 install shazam.py
```
You'll also need to have ffmpeg installed and added to PATGH.

### Usage

Synchronous Shazam:

```python
from shazam import Shazam

mp3_file_content_to_recognize = open('a.mp3', 'rb').read()

with Shazam(mp3_file_content_to_recognize) as results:
    for res in results:
        print(res)  # current offset & shazam response to recognize requests
```

Asynchronous operations are also supported:

```python
from shazam import AsyncShazam

mp3_file_content_to_recognize = open('a.mp3', 'rb').read()

async with AsyncShazam(mp3_file_content_to_recognize) as results:
    async for res in results:
        print(res)
```

There is also support for using your own session objects and using `Shazam` and `AsyncShazam` outside of
a context manager.



### Credits to:
https://github.com/Numenorean/ShazamAPI (and by proxy, https://github.com/marin-m/SongRec)
