from typing import TypedDict
from functools import cached_property

class TrackImgs(TypedDict):
    # these three seem to just be the same
    background: str
    coverart: str
    covertarthq: str
    # no clue what this is
    joecolor: str

class ShareObj(TypedDict):
    # song name - artist
    subject: str

    # song name by artist
    text: str

    # shazam url
    href: str
    # same as other images in TrackImgs
    image: str
    # I used @Shazam to ...
    twitter: str
    # email share
    html: str
    # snap stuff?
    snapchat: str


class HubObj(TypedDict):
    type: str  # APPLEMUSIC

    # I remember writing down somewhere how to deal with {scalefactor} but
    # I forgot now, so who knows what this goes to idk
    image: str
    # TODO:

class TrackObj(TypedDict):
    layout: int  # always 5
    type: str  # always MUSIC
    key: int  # same as MatchObj.id

    title: str
    subtitle: str  # the artist
    images: TrackImgs
    share: ShareObj
    hub: HubObj
    # TODO:



class MatchObj(TypedDict):
    id: int
    offset: float
    timeskew: float
    frequencyskew: float

class LocationObj(TypedDict):
    accuracy: float

class Response(TypedDict):
    matches: list[MatchObj]
    location: LocationObj
    timezone: str

    track: TrackObj
    tagid: str



class Response:
    def __init__(self, data):
        self.data = data

    @cached_property
    def name(self) -> str:
        # self.data["track"]["share"]["subject"].split("-")[0].rstrip()
        return self.data["track"]["title"]

    @cached_property
    def artist(self) -> str:
        # self.data["track"]["share"]["subject"].split("-")[1].lstrip()
        return self.data["track"]["subtitle"]
    
    @cached_property
    def is_explicit(self) -> bool:
        return self.data["track"]["hub"]["explicit"]

    @cached_property
    def cover_url(self) -> str:
        imgs = self.data["track"].get("images")

        if not imgs:
            return self.data["track"]["share"]["image"]

        # I'm bouta do something really smart
        return imgs.get("background") or (
            imgs.get("coverart") or (
                imgs.get("covertarthq")
            )
        )
