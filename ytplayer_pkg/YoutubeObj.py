
class YoutubeObj(object):
    def __init__(self, name, url, duration):
        print('>>YTObj>>', name, url, duration)
        self.name = name
        self.url = url
        self.duration = duration