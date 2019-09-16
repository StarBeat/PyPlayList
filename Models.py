from datetime import timedelta

class IBaseList(object):
    def __init__(self, entities :list  = None, file_name :str  = ""):#py 的默认参数只初始化一次，后续默认参数指向相同对象
        self.file_name :str = file_name
        self.entities :list = entities if None else list()
    class Entity():
        def __init(self, path :str):
            self.path :str = path

    def GetTracksPaths(self):
        paths : list = None
        for i in self.entities:
            paths.append(self.Entity(i).path)
        return paths

class BaseList(object):
    def __init__(self, path :str = ""):
        self.path :str = path

class M3u(IBaseList):
    def __init__(self, is_extened :bool = False, file_name :str  = ""):
        super(M3u, self).__init__(file_name)
        self.is_extened :bool = is_extened
    is_extened :bool
    class M3uBase(BaseList):
        def __init__(self, title :str = "", album :str = "", album_artist :str = "", duration :timedelta = timedelta(milliseconds = 0), path :str = ""):
            super().__init__(path)
            self.title :str = title
            self.album :str = album
            self.album_artist :str = album_artist
            self.duration :timedelta = duration

class Pls(IBaseList):
    def __init__(self, version :int = -1, file_name :str  = ""):
        super(Pls, self).__init__(file_name)
        self.version :int = 2
    class  PlsBase(BaseList):
        def __init__(self, title :str = "", length :timedelta = timedelta(milliseconds = 0), nr :int = 0, path :str = ""):
            super().__init__(path)
            self.title :str = title
            self.length :timedelta = length
            self.nr :int = nr

    def GetNums(self):
        return len(self.entities)

class Wpl(IBaseList):
    def __init__(self, author :str = "", generator :str = "", 
                 guid :str = "", item_count :int = -1, title :str = "", total_duration:timedelta = timedelta(milliseconds = 0), file_name :str  = ""):
        super(Wpl, self).__init__(file_name)
        self.author :str = author
        self.generator :str =generator
        self.guid :str = guid
        self.item_count :int = item_count
        self.title :str = title
        self.total_duration:timedelta =total_duration

    class WplBase(BaseList):
        def __init__(self, album_title :str = "", album_artist :str = "", 
                     duration :timedelta = None, track_title :str = "", track_artist :str = "", path :str = ""):
            super().__init__(path)
            self.album_title :str = album_title
            self.album_artist :str = album_artist
            self.duration :timedelta = duration
            self.track_title :str = track_title
            self.track_artist :str = track_artist


class Zpl(IBaseList):
    def __init__(self, author :str = "", generator :str = "", 
                 guid :str = "", item_count :int = -1, title :str = "", total_duration:timedelta = timedelta(milliseconds = 0), file_name :str  = ""):
        super(Zpl, self).__init__(file_name)
        self.author :str = author
        self.generator :str =generator
        self.guid :str = guid
        self.item_count :int = item_count
        self.title :str = title
        self.total_duration:timedelta =total_duration

    class ZplBase(BaseList):
        def __init__(self, album_title :str = "", album_artist :str = "", 
                     duration :timedelta = None, track_title :str = "", track_artist :str = "", path :str = ""):
            super().__init__(path)
            self.album_title :str = album_title
            self.album_artist :str = album_artist
            self.duration :timedelta = duration
            self.track_title :str = track_title
            self.track_artist :str = track_artist