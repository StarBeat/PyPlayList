from datetime import timedelta
import re
from abc import ABC, abstractmethod
import Models
from Util import Util
try: 
    import xml.etree.cElementTree as ET
    from xml.etree.cElementTree import ElementTree
except ImportError: 
    import xml.etree.ElementTree as ET 
    from xml.etree.ElementTree import ElementTree
def indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
class AbsPlayListWR(object):
    @abstractmethod
    def PaserFromStr(self, arg:str):
        pass

    @abstractmethod
    def ToText(self, arg:Models.IBaseList):
        pass

    def PaserFromFile(self, path:str):
        with open("PlaylistExt.m3u") as f:
            return self.PaserFromStr(f.read())

    def Save(self, path:str, model:Models.IBaseList):
        with open(path, "w") as w:
            w.write(self.ToText(model))

class M3u8Content(AbsPlayListWR):
    def PaserFromStr(self, arg:str):
        m3 = Models.M3u()
        lins :list = arg.splitlines()
        if lins[0] == "#EXTM3U":
            m3.is_extened = True
        else:
            m3.is_extened = False
            m3.entities.append(Models.M3u.M3uBase(title = "", duration = 0, path = lins[0]))
        prevLineIsExtInf :bool = False
        title :str = ""
        artist :str = ""
        album :str = ""
        seconds :int = 0
        for i in lins[1:]:
            if i.startswith("#"):
                if m3.is_extened:
                    if i.startswith("#EXTINF"):
                        prevLineIsExtInf = True
                        try:
                            title = i[i.index(',') + 1:]
                        except IndexError:
                            title = ""
                        try:
                            seconds = int(i[8: i.index(',')])
                        except IndexError or ValueError:
                            seconds = 0
                    elif i.startswith("#EXTALB"):
                        try:
                            album = i[i.index(":") + 1:]
                        except IndexError:
                            album = ""
                    elif i.startswith("#EXTART"):
                        try:
                            artist = i[i.index(":") + 1 :]
                        except IndexError:
                            artist = ""
            else:
                if not m3.is_extened or not prevLineIsExtInf:
                    title = ""
                    artist = ""
                    album = ""
                    seconds = 0
                m3.entities.append(m3.M3uBase(album = album, album_artist = artist, duration = timedelta(seconds = seconds), title = title, path = i))
                prevLineIsExtInf = False
        return m3

    def ToText(self, arg:Models.M3u):
        m3 = arg
        text :str = ""
        if m3.is_extened:
            text :str = "#EXTM3U\n"
        for x in m3.entities:
            if m3.is_extened:
                if x.album != "":
                    text += "#EXTALB:" + x.album + "\n"
                if x.album_artist != "":
                    text += "#EXTART:" + x.album_artist + "\n"
                if x.duration.days >= 0:
                    text += "#EXTINF:" + x.duration.seconds.__str__() + "," + x.title + "\n"
                else:
                    text += "#EXTINF:" + "-1" + "," + x.title + "\n"
            text += x.path + "\n"
        return text

class PlsContent(AbsPlayListWR):
    def __getNr(self, arg:str):
        nr :int = -1
        try:
            if arg.startswith("File"):
                nr = int(arg[4: arg.index("=")])
            elif arg.startswith("Title"):
                nr = int(arg[5: arg.index("=")])
            elif arg.startswith("Length"):
                nr = int(arg[6: arg.index("=")])
        except IndexError or ValueError:
            nr = -1

        return nr 

    def PaserFromStr(self, arg:str):
        pls = Models.Pls()
        lines :list = arg.splitlines()
        path :str = ""
        if lines[0].strip() != "[playlist]":
            return pls
        for i in lines:
            nr :int = self.__getNr(i)
            entrys :list = [x for x in pls.entities if x.nr == nr]
            if i.startswith("File"):
                try:
                    path :str = i[i.index("=") + 1:]
                except IndexError:
                    path = ""
                if len(entrys) > 0:
                    entrys[0].path = path
                else:
                    pls.entities.append(pls.PlsBase(path = path, nr = nr))
            elif i.startswith("Title"):
                try:
                    title :str = i[i.index("=") + 1:]
                except IndexError:
                    title :str = ""
                if title != "":
                    if len(entrys) > 0:
                        entrys[0].title = title
                    else:
                        pls.entities.append(pls.PlsBase(title = title, nr = nr))
            elif i.startswith("Length"):
                try:
                    length :timedelta = i[i.index("=") + 1:]
                except IndexError:
                    length :timedelta = 0
                if len(entrys) > 0:
                    entrys[0].length = length
                else:
                    pls.entities.append(pls.PlsBase(length = length, nr = nr))
        pls.entities.sort(key = lambda x: x.nr)
        #pls.entities.sort(cmp = lambda x, y: x.nr > y.nr)
        return pls

    def ToText(self, arg:Models.Pls):
        pls = arg
        nr :int = 0
        text :str = "[playlist]\n"
        for i in pls.entities:
            nr += 1
            text += "File" + nr.__str__() + "=" + i.path + "\n"
            if i.title != "":
                text += "Title" + nr.__str__() + "=" + i.title + "\n"
            if i.length != 0 and i.length != timedelta(milliseconds = 0):
                text += "Length" + nr.__str__() + "=" + i.length.__str__() + "\n"
            text += "\n"
        text += "NumberOfEntries=" + nr.__str__() + "\n"
        text += "\n" + "Version=2"
        return text

class WplContent(AbsPlayListWR):
    def PaserFromStr(self, arg:str):
        wpl = Models.Wpl()
        path :str = ""
        self.version = re.search(r'\d+\.\d+', arg).group()
        root = ET.fromstring(arg)
        head = root.find("head")
        attr = head.find("author")
        wpl.author = attr.text if attr != None and attr.text != None else ""
        attr = head.find("guid")
        wpl.guid = attr.text if attr != None and attr.text != None else ""
        attr = head.find("title")
        wpl.title = attr.text if attr != None and attr.text != None else ""

        elements = head.findall("meta")
        for i in elements:
            name :str = Util.Util.UnEscape(i.get("name"))
            content :str = Util.Util.UnEscape(i.get("content"))
            if name == "Generator":
                wpl.generator = content
            elif name == "ItemCount":
                try:
                    wpl.item_count = int(content)
                except ValueError:
                    wpl.item_count = 0
            elif name == "totalDuration":
                try:
                    wpl.total_duration = timedelta(milliseconds = int(content))
                except ValueError:
                    wpl.total_duration = timedelta(milliseconds = 0)
        seqs = root.find("body").findall("seq")
        media_elements :list = []
        for x in seqs:
            media_elements.append(x.findall("media"))
        for media in media_elements:
            for i in media:
                src :str = Util.Util.UnEscape(i.get("src"))
                track_title = Util.Util.UnEscape(i.get("trackTitle"))
                track_artist = Util.Util.UnEscape(i.get("trackArtist"))
                album_title = Util.Util.UnEscape(i.get("albumTitle"))
                album_artist = Util.Util.UnEscape(i.get("albumArtist"))
                try:
                    duration :timedelta = timedelta(milliseconds = int(Util.Util.UnEscape(i.find("duration"))))
                except ValueError:
                    duration :timedelta = timedelta()
                wpl.entities.append(wpl.WplBase(album_title  = album_title, album_artist  = album_artist, 
                         duration = duration, track_title  = track_title, track_artist = track_artist, path = src))
        return wpl

    def __CreateSeqWithMedia(self, wpl:Models.Wpl):
        seq :ET.Element = ET.Element("seq")
        for i in wpl.entities:
            media :ET.Element = ET.SubElement(seq, "media")
            media.set("src", i.path)
            if i.album_artist != "":
                media.set("albumTitle", i.album_artist)
            if i.album_title != "":
                media.set("albumArtist", i.album_title)
            if i.track_title != "":
                media.set("trackTitle", i.track_title)
            if i.track_artist != "":
                media.set("trackArtist", i.track_artist)
            if i.duration != "":
                media.set("duration", str(i.duration.microseconds))
        return seq

    def __CreateMeta(self, name:str, content:str):
        meta :ET.Element = ET.Element("meta")
        meta.set("content", str(content))
        meta.set("name", name)
        return meta

    def ToText(self, arg:Models.Wpl):
        seq :ET.Element = self.__CreateSeqWithMedia(arg)
        body :ET.Element = ET.Element("body")
        body.insert(0, seq)
        head :ET.Element = ET.Element("head")
        author :ET.Element = ET.Element("author")
        if arg.author != "":
            author.text = arg.author
        guid :ET.Element = ET.Element("guid")
        if arg.guid != "":
            guid.text = arg.guid
        if arg.generator != "":
            head.insert(0, self.__CreateMeta("Generator", arg.generator))
        if arg.item_count > 0:
            head.insert(0, self.__CreateMeta("ItemCount", arg.item_count))

        head.insert(0, self.__CreateMeta("totalDuration", arg.total_duration.microseconds))
        head.insert(0, guid)
        head.insert(0, author)
        title :ET.Element = ET.Element("title")
        title.text = arg.title
        head.append(title)
        smil :ET.Element = ET.Element("smil")
        smil.append(head)
        smil.append(body)
        indent(smil)
        xml_str = ET.tostring(smil)
        #et = ElementTree(smil)
        #et.write('output.xml', encoding='UTF-8')
        return  "<?wpl version=\"" + self.version + "\"?>\n" + xml_str.decode("utf-8")


class ZplContent(AbsPlayListWR):
    def PaserFromStr(self, arg:str):
        zpl = Models.Zpl()
        path :str = ""
        self.version = re.search(r'\d+\.\d+', arg).group()
        root = ET.fromstring(arg)
        head = root.find("head")
        attr = head.find("author")
        zpl.author = attr.text if attr != None and attr.text != None else ""
        attr = head.find("guid")
        zpl.guid = attr.text if attr != None and attr.text != None else ""
        attr = head.find("title")
        zpl.title = attr.text if attr != None and attr.text != None else ""

        elements = head.findall("meta")
        for i in elements:
            name :str = Util.Util.UnEscape(i.get("name"))
            content :str = Util.Util.UnEscape(i.get("content"))
            if name == "Generator":
                zpl.generator = content
            elif name == "ItemCount":
                try:
                    zpl.item_count = int(content)
                except ValueError:
                    zpl.item_count = 0
            elif name == "totalDuration":
                try:
                    zpl.total_duration = timedelta(milliseconds = int(content))
                except ValueError:
                    zpl.total_duration = timedelta(milliseconds = 0)
        seqs = root.find("body").findall("seq")
        media_elements :list = []
        for x in seqs:
            media_elements.append(x.findall("media"))
        for media in media_elements:
            for i in media:
                src :str = Util.Util.UnEscape(i.get("src"))
                track_title = Util.Util.UnEscape(i.get("trackTitle"))
                track_artist = Util.Util.UnEscape(i.get("trackArtist"))
                album_title = Util.Util.UnEscape(i.get("albumTitle"))
                album_artist = Util.Util.UnEscape(i.get("albumArtist"))
                try:
                    duration :timedelta = timedelta(milliseconds = int(Util.Util.UnEscape(i.find("duration"))))
                except ValueError:
                    duration :timedelta = timedelta()
                zpl.entities.append(zpl.ZplBase(album_title  = album_title, album_artist  = album_artist, 
                         duration = duration, track_title  = track_title, track_artist = track_artist, path = src))
        return zpl

    def __CreateSeqWithMedia(self, zpl:Models.Zpl):
        seq :ET.Element = ET.Element("seq")
        for i in zpl.entities:
            media :ET.Element = ET.SubElement(seq, "media")
            media.set("src", i.path)
            if i.album_artist != "":
                media.set("albumTitle", i.album_artist)
            if i.album_title != "":
                media.set("albumArtist", i.album_title)
            if i.track_title != "":
                media.set("trackTitle", i.track_title)
            if i.track_artist != "":
                media.set("trackArtist", i.track_artist)
            if i.duration != "":
                media.set("duration", str(i.duration.microseconds))
        return seq

    def __CreateMeta(self, name:str, content:str):
        meta :ET.Element = ET.Element("meta")
        meta.set("content", str(content))
        meta.set("name", name)
        return meta

    def ToText(self, arg:Models.Zpl):
        seq :ET.Element = self.__CreateSeqWithMedia(arg)
        body :ET.Element = ET.Element("body")
        body.insert(0, seq)
        head :ET.Element = ET.Element("head")
        author :ET.Element = ET.Element("author")
        if arg.author != "":
            author.text = arg.author
        guid :ET.Element = ET.Element("guid")
        if arg.guid != "":
            guid.text = arg.guid
        if arg.generator != "":
            head.insert(0, self.__CreateMeta("Generator", arg.generator))
        if arg.item_count > 0:
            head.insert(0, self.__CreateMeta("ItemCount", arg.item_count))

        head.insert(0, self.__CreateMeta("totalDuration", arg.total_duration.microseconds))
        head.insert(0, guid)
        head.insert(0, author)
        title :ET.Element = ET.Element("title")
        title.text = arg.title
        head.append(title)
        smil :ET.Element = ET.Element("smil")
        smil.append(head)
        smil.append(body)
        indent(smil)
        xml_str = ET.tostring(smil)
        return  "<?zpl version=\"" + self.version + "\"?>\n" + xml_str.decode("utf-8")