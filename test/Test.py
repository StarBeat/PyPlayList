# -*- coding:utf-8 -*-
from Content import *
from Util import Util
import os
import PlayListFactory

if __name__ == "__main__":
    print(os.path.abspath(__file__))
    fl = Util.Util.Walk("test/res")
    for x in fl:
        with open(x) as f:
            content = PlayListFactory.ContentFactory.Create(x[x.rindex(".") + 1: ])
            extm3u_path = "test/test_out/test_.out" 
            content_text = f.read()
           
            parse_res = content.PaserFromStr(content_text)
            content.Save(extm3u_path, parse_res)
            #print(content_text.strip().replace("\n", "").replace("\t", ""))
            out_text = open(extm3u_path).read()
            #print(out_text.strip().replace("\n", "").replace("\t", ""))
            if content_text.strip().replace("\n", "").replace("\r", "") == out_text.strip().replace("\n", "").replace("\r", ""):
                print(x + "\t pass\n")
            else:
                #TODO 对象部分属性比较
                print(x + "\t fail\n")
                pass