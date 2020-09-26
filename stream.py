from sanitize import sanitize

class Stream:
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

    def isLive(self, streams) -> bool:
        for stream in streams:
            if stream.streamName == self.streamName:
                return True
        return False
