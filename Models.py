from datetime import timedelta

class IBaseList(object):
    def __init__(self, path :str = None, file_name :str  = None, entities :list  = None):
        self.path :str = path
        self.file_name :str = file_name
        self.entities :list = entities
    class Entity():
        def __init(self, path :str = None):
            self.path :str = path

    def GetTracksPaths(self):
        paths : list = None
        for i in self.entities:
            paths.append(self.Entity(i).path)
        return paths

class M3u(IBaseList):
    def __init__(self, is_extened :bool = False):
        self.is_extened :bool = is_extened
    is_extened :bool
    class M3uBase:
        def __init__(self, title :str = None, album :str = None, album_artist :str = None, duration :timedelta = None):
            self.title :str = title
            self.album :str = album
            self.album_artist :str = album_artist
            self.duration :timedelta = duration

class Pls(IBaseList):
    def __init__(self, version :int = None):
        self.version :int = 2
    class  PlsBase:
        def __init(self, title :str = None, length :timedelta = None, nr :int = None):
            self.title :str
            self.length :timedelta
            self.nr :int

    def GetNums(self):
        return len(self.entities)

class Wpl(IBaseList):
    def __init__(self, author :str = None, generator :str = None, 
                 guid :str = None, item_count :int = None, title :str = None, total_duration:timedelta = None):
        self.author :str = author
        self.generator :str =generator
        self.guid :str = guid
        self.item_count :int = item_count
        self.title :str = title
        self.total_duration:timedelta =total_duration

    class WplBase:
        def __init__(self, album_title :str = None, album_artist :str = None, 
                     duration :timedelta = None, track_title :str = None, track_artist :str = None):
            self.album_title :str = album_title
            self.album_artist :str = album_artist
            self.duration :timedelta = duration
            self.track_title :str = track_title
            self.track_artist :str = track_artist


class Zpl(IBaseList):
    def __init__(self, author :str = None, generator :str = None, 
                 guid :str = None, item_count :int = None, title :str = None, total_duration:timedelta = None):
        self.author :str = author
        self.generator :str =generator
        self.guid :str = guid
        self.item_count :int = item_count
        self.title :str = title
        self.total_duration:timedelta =total_duration

    class ZplBase:
        def __init__(self, album_title :str = None, album_artist :str = None, 
                     duration :timedelta = None, track_title :str = None, track_artist :str = None):
            self.album_title :str = album_title
            self.album_artist :str = album_artist
            self.duration :timedelta = duration
            self.track_title :str = track_title
            self.track_artist :str = track_artist