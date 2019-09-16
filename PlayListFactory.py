from Content import *
class ContentFactory(object):
    @staticmethod
    def Create(arg :str):
        if arg.lower() == "m3u" or arg.lower() == "meu8":
            return M3u8Content()
        elif arg.lower() == "pls":
            return PlsContent()
        elif arg.lower() == "wpl":
            return WplContent()
        elif arg.lower() == "zpl":
            return ZplContent()
