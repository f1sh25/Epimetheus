from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re as re
import time
import pandas as pd
import csv
import random
import json




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


#ladataan käyttäjät        
user_list_raw="log.csv"
user_list=[]
with open(user_list_raw) as users:
    for user in users:
        row = user.replace("\n", "")
        data = row.split(";")
        if data[0]!="username":
            user_list.append(User(data[0],data[1],data[2]))
    users.close()

def less_used_user():
    return_user=()
    user_use_count=100000
    for user in user_list:
        if user.used<user_use_count:
            user_use_count=user.used
            return_user=user
    return return_user

chosen_one=less_used_user()


PATH = (r"C:\Users\ilpoa\epimetheus\drivers\chromedriver.exe")
USER=chosen_one.user
PASSWORD=chosen_one.password

print(PATH)
print(USER)
print(PASSWORD)


driver = webdriver.Chrome(PATH)

target_company="metsooficial"

driver.get(f"https://www.linkedin.com/company/{target_company}/people/")
time.sleep(3)


email=driver.find_element_by_id("username")
email.send_keys(USER)
password=driver.find_element_by_id("password")
password.send_keys(PASSWORD)
chosen_one.add_use() #lisätään käyttö
time.sleep(3+random.randint(0,5)) #jitter
password.send_keys(Keys.RETURN)




#kirjataan käyttäjämuutokset
with open("log.csv", "w") as users_csv:
    fieldnames=["username","password","used"]
    writer = csv.DictWriter(users_csv,delimiter=";",lineterminator="\n",quotechar='"',fieldnames=fieldnames)
    writer.writeheader()
    for user in user_list:
        writer.writerow(user.sanakirja())
