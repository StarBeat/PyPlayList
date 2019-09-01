from datetime import timedelta
from abc import ABC, abstractmethod
import Models

class IPlayListWR(object):
    @abstractmethod
    def PaserFromStr(self, arg:str):
        pass

    @abstractmethod
    def ToText(self, arg:Models.IBaseList):
        pass

class M3u8Content(IPlayListWR):
    def PaserFromStr(self, arg:str):
        m3 = Models.M3u()
        lins :list = arg.splitlines()
        if lins[0] == "#EXTM3U":
            m3.is_extened = True
        else:
            m3.is_extened = False
            m3.entities.append(Models.M3u.M3uBase(title = "", duration = 0))
            m3.path = lins[0]
        prevLineIsExtInf :bool = False
        title :str = ""
        artist :str = ""
        album :str = ""
        seconds :int = 0
        for i in lins:
            if i.startwith("#"):
                if m3.is_extened:
                    if i.startwith("#EXTINF"):
                        prevLineIsExtInf = True
                        title = i[i.index(',') + 1,]
                        seconds = int(i[8, i.index(',') - 8])
                    elif i.startwith("#EXTALB"):
                        album = i[i.index(":") + 1,]
            else:
                if not m3.is_extened or not prevLineIsExtInf:
                    title = ""
                    artist = ""
                    album = ""
                    seconds = 0
                m3.entities.append(Models.M3u.M3uBase(album = album, album_artist = artist, duration = timedelta(seconds), title = title))
                m3.path = i
                prevLineIsExtInf = False
        return m3

    def ToText(self, args):
        m3 = Models.M3u(args)
        text :str = ""#EXTM3U"\n"
        for x in m3.entities:
            if m3.is_extened:
                if x.album != None:
                    text += "#EXTALB:" + x.album
                if x.album_artist != None:
                    text += "#EXTART:" + x.album_artist
                text += "#EXTINF:" + timedelta(x.duration).seconds + "," + x.title
            text += m3.path
        return text

class M3uContent(object):
    pass

class PlsContent(object):
    pass

class WplContent(object):
    pass

class ZplContent(object):
    pass