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

user_list_raw="log.csv"
user_dict=[]
with open(user_list_raw) as users:
    for user in users:
        row = user.replace("\n", "")
        data = row.split(";")
        if data[0]!="username":
            user_dict.append({"username":data[0],"password":data[1], "used":int(data[2])})
    users.close()

with open("log.csv", "w") as users_csv:
    fieldnames=["username","password","used"]
    writer = csv.DictWriter(users_csv,delimiter=";",lineterminator="\n",quotechar='"',fieldnames=fieldnames)
    writer.writeheader()
    for user in user_dict:
        writer.writerow(user)