# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from Util import Util

class Music163():
    def __init__(self, phone:str, passworld:str):
        self.phone = phone
        self.passworld = passworld
        self.browser = webdriver.Chrome()
        self.browser.get("https://music.163.com")
        time.sleep(1)
        self.browser.maximize_window()

    def login(self):
        num = 0
        while True:
            try:
                a_login = self.browser.find_elements_by_tag_name('a')
                for x in a_login:
                    if x.text == "登录":
                        x.click()
                        break
                btn_mobile = self.browser.find_element_by_class_name('u-btn2-2')
                btn_mobile.click()
                phonenum_input = self.browser.find_element_by_id('p')
                phonenum_input.send_keys(self.phone)
                password_input = self.browser.find_element_by_id('pw')
                password_input.clear()
                password_input.send_keys(self.passworld)
                password_input.send_keys(Keys.ENTER)
                time.sleep(0.5)
                break
            except :
                if num < 5:
                    print("logine faile try agine: %d" % num)
                    num += 1
    
    def GtoMySpace(self):
        self.browser.get("https://music.163.com/my/")
        self.browser.switch_to.frame('contentFrame')
        time.sleep(0.5)

    def GetMusicList(self):
        myls = self.browser.find_element_by_class_name('n-minelst-1').find_elements_by_tag_name('li')
        for i in range(len(myls)):
            while True:
                try:
                   myls = self.browser.find_element_by_class_name('n-minelst-1').find_elements_by_tag_name('li')
                   ml = myls[i].find_element_by_class_name('s-fc0')
                   file_name = Util.Util.ToFileName(ml.text)
                   ml.click()
                   time.sleep(0.5)

                   tb = self.browser.find_element_by_class_name('m-table')
                   trs = tb.find_elements_by_tag_name('tr')
                   print("\n%s start num %d:" % (file_name, len(trs)))

                   with open("163/rst/" + file_name + ".txt", "w", encoding = 'utf-8') as f:
                       for tr in trs:
                           tds = tr.find_elements_by_tag_name('td')
                           if len(tds) >= 5:
                               title = tds[1].find_element_by_tag_name('b').get_attribute('title').replace('\xa0', ' ')
                               dur = tds[2].find_element_by_class_name('u-dur').text
                               art = tds[3].find_element_by_tag_name('span').get_attribute('title')
                               album = tds[4].find_element_by_tag_name('a').get_attribute('title')
                               f.write('title:\t' + title + '\tdur:' + dur + '\tart:' + art + '\talbum:' + album + '\n')
                       print("%s done\n" % file_name)
                   time.sleep(0.5)
                   if i < len(myls) - 1:
                       myls[i].find_element_by_class_name('s-fc0').send_keys(Keys.DOWN)
                   break
                except Exception as e:
                   print(e)

if __name__ == '__main__':
    m = Music163("", "")
    m.login()
    m.GtoMySpace()
    m.GetMusicList()
    while True:
        print("main")
        time.sleep(10)