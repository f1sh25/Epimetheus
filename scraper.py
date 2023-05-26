from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import requests
import re as re
import time
import pandas as pd
import csv
import random
import json

#koodin alku


class User:
    def __init__(self,username:str,password:str,used:int):
        self.user=username
        self.password = password
        self.used = int(used)
    def sanakirja(self):
        lause = {"username":self.user,"password":self.password,"used":self.used}
        return lause
    def add_use(self):
        self.used+=1

def less_used_user():
    return_user=()
    user_use_count=100000
    for user in user_list:
        if user.used<user_use_count:
            user_use_count=user.used
            return_user=user
    return return_user




#-----PROXY SETTING------

PROXY="185.20.71.38:443"

#------------------------

#-------TARGET-----------

target_company="kesko"

#-----------------------

#ladataan käyttäjät        
user_list_raw="user_list.csv"
user_list=[]
with open(user_list_raw) as users:
    for user in users:
        row = user.replace("\n", "")
        data = row.split(";")
        print(data)
        if data[0]!="\ufeffusername":
            user_list.append(User(data[0],data[1],data[2]))
    users.close()



chosen_one=less_used_user()


PATH = (r"C:\Users\ilpoa\epimetheus\drivers\chromedriver.exe")
USER=chosen_one.user
PASSWORD=chosen_one.password




print(PATH)
print("Chosen one: ")
print(USER)
print(PASSWORD)
print(f"used {chosen_one.used}")




#init for proxy
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(PATH, options=options)


stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

#driver.get(f"https://www.linkedin.com/company/{target_company}/people/")
driver.get("https://bot.incolumitas.com/#botChallenge")
time.sleep(3)

#---------login------------

email=driver.find_element(By.ID,"username")
email.send_keys(USER)
password=driver.find_element(By.ID,"password")
password.send_keys(PASSWORD)
chosen_one.add_use() #lisätään käyttö
time.sleep(2+random.randint(0,3)) #jitter
password.send_keys(Keys.RETURN)


peoples = bs.find_all("div", {"class" :"artdeco-entity-lockup__content"})


targets = []
for human in peoples:
    #name = 
    #bio =
    #link =








time.sleep(20)
quit()





#kirjataan käyttäjämuutokset
with open("log.csv", "w") as users_csv:
    fieldnames=["username","password","used"]
    writer = csv.DictWriter(users_csv,delimiter=";",lineterminator="\n",quotechar='"',fieldnames=fieldnames)
    writer.writeheader()
    for user in user_list:
        writer.writerow(user.sanakirja())