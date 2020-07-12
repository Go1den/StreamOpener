class Stream:
    def __init__(self, gameTitle, previewImage, streamName, streamTitle, stylizedStreamName, viewerCount):
        self.gameTitle = gameTitle
        self.previewImage = previewImage
        self.streamName = streamName
        self.streamTitle = streamTitle
        self.stylizedStreamName = stylizedStreamName
        self.viewerCount = viewerCount

    def isLive(self, streams) -> bool:
        for stream in streams:
            if stream.streamName == self.streamName:
                return True
        return False
