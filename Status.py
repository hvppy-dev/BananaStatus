import requests
import json
import time
import locale
import ctypes

from tkinter import *
from tkinter import messagebox as mb

def LangSetup(self):
    locale.getdefaultlocale()
    windll = ctypes.windll.kernel32
    windll.GetUserDefaultUILanguage()
    SysLang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    return SysLang

class AnimatedStatus:
    def loadJson(self):
        jsonData = json.load(open("StatusList.json", "rb"))
        statusList = jsonData["Status"]
        timeDelay = jsonData["TimeDelay"]
        token = jsonData["Token"]
        listSize = len(statusList)
        return statusList, timeDelay, listSize, token

    def start(self):
        try:
            json.load(open("StatusList.json", "rb"))
        except:
            LangCheck = LangSetup(self)
            if LangCheck == "ru_RU":
                mb.showerror("Ошибка", "\nStatusList.json не найден\n")
            else:
                mb.showerror("Error", "\nStatusList.json not found\n")
            exit()
        statusList, timeDelay, listSize, token = self.loadJson()

        headers = {"Host": "discord.com",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
           "Accept": "*/*",
           "Accept-Language": "ru",
           "Accept-Encoding": "gzip, deflate, br",
           "Content-Type": "application/json",
           "Authorization": token}

        counter = 0
        while 1:
            if counter < listSize:
                data = {"custom_status": statusList[counter]}
                requests.patch('https://discord.com/api/v9/users/@me/settings', json.dumps(data), headers=headers)
                statusList, timeDelay, listSize, token = self.loadJson()
                counter += 1
                time.sleep(timeDelay)
            else:
                counter = 0        

if __name__ == "__main__":
    main = AnimatedStatus()
    try:
        main.start()    
    except:
        while True:
            LangCheck = LangSetup(main)
            if LangCheck == "ru_RU":
                ErrorCheck = mb.askyesno("Ошибка", "Ошибка подключения.\nХотите попробовать ещё раз?")
            else:
                ErrorCheck = mb.askyesno("Error", "Connection error.\nTry again?")
            if ErrorCheck == True:
                main.start()
            else:
               exit()        