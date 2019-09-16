import os

class Util:
    @staticmethod
    def MakeAbsolutePath(folder :str, file :str):
        pass

    @staticmethod
    def MakeRelativePath(folder :str, file :str):
        pass

    @staticmethod
    def IsAbsolutePath(path :str):
        if path.count > 3:
            if path[1] == ':' and (path[2] == '\\' or path[2] == '/') :
                return True
        return False

    @staticmethod
    def IsRelativePath(path :str):
        if path.starwith(r"/") or path.starwith(r"./") or\
           path.starwith(r"../") or path.starwith("\\") or \
           path.starwith('.\\') or path.starwith("..\\") :
           return True
        return False

    @staticmethod
    def IsStream(url :str):
        return url.find("://")

    @staticmethod
    def UnEscape(content :str):
        if content == "" or content == None:
            return ""
        return content.replace("&amp;", "&").replace("&apos;", "'").replace("&quot;", "\"").replace("&gt;", ">").replace("&lt;", "<")

    @staticmethod
    def Escape(content :str):
        if content == ""or content == None:
            return ""
        return content.replace("&", "&amp;").replace("'", "&apos;").replace("\"", "&quot;").replace(">", "&gt;").replace("<", "&lt;")

    @staticmethod
    def RecursiveTraversal(path:str):
        flist = []
        filels = os.listdir(path)
        for fi in filels:
            if os.path.isdir(fi):
                Util.RecursiveTraversal(fi)
            else:
                flist.append(os.path.join(path, fi))
        return flist

    @staticmethod
    def Walk(path :str):
        flist = []
        for fpath, dirs, fs in os.walk(path):
            for f in fs:
                flist.append(os.path.join(fpath, f))
        return flist
