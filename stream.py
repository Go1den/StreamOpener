import io
from urllib.request import urlopen

from PIL import ImageTk, Image

from sanitize import sanitize

class Stream:
    DEFAULT_BOX_ART = None
    DEFAULT_STREAM_PREVIEW = None

    def __init__(self, stream, gameTitle, boxArtURL):
        self.ID = stream['id']
        self.viewerCount = sanitize(str(stream['viewer_count']))
        self.gameID = stream['game_id']
        self.type = stream['type']
        self.userID = stream['user_id']
        self.language = stream['language']
        self.thumbnailURL = sanitize(stream['thumbnail_url'])
        self.stylizedStreamName = sanitize(stream['user_name'])
        self.streamTitle = sanitize(stream['title'])
        self.gameTitle = sanitize(gameTitle)
        self.tagIDs = stream['tag_ids']
        self.startedAt = stream['started_at']

        self.previewImage = sanitize(stream['thumbnail_url'].replace('{width}', '320').replace('{height}', '180'))
        self.streamName = sanitize(stream['thumbnail_url'][52:].split('-')[0])
        self.boxArtURL = boxArtURL

        self.loadedBoxArtImage = None
        self.loadedPreviewImage = None

    def isLive(self, streams) -> bool:
        for stream in streams:
            if stream.streamName == self.streamName:
                return True
        return False

    def setBoxArtImageFromURL(self):
        try:
            rawData = urlopen(self.boxArtURL).read()
            im = Image.open(io.BytesIO(rawData))
            self.loadedBoxArtImage = ImageTk.PhotoImage(im)
        except ValueError:
            self.loadedBoxArtImage = self.DEFAULT_BOX_ART

    def setPreviewImageFromURL(self):
        try:
            rawData = urlopen(self.previewImage).read()
            im = Image.open(io.BytesIO(rawData))
            self.loadedPreviewImage = ImageTk.PhotoImage(im)
        except ValueError:
            self.loadedPreviewImage = self.DEFAULT_STREAM_PREVIEW

    def setImagesFromURL(self):
        self.setBoxArtImageFromURL()
        self.setPreviewImageFromURL()
