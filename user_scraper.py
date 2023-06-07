from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from threading import Thread
from linkedin_scraper import Person, actions
import json
import requests
import random
import csv
import time



class ScrapingUser:
    def __init__(self,username:str,password:str,used:int):
        self.user=username
        self.password = password
        self.used = int(used)
    def sanakirja(self):
        lause = {"username":self.user,"password":self.password,"used":self.used}
        return lause
    def add_use(self):
        self.used+=1

# PROXY FUNCTIONS
def proxy_finder():

  # Retrieve latest proxies
  proxies_req = Request('https://www.sslproxies.org/')
  proxies_req.add_header('User-Agent', ua.random)
  proxies_doc = urlopen(proxies_req).read().decode('utf8')

  soup = BeautifulSoup(proxies_doc, 'html.parser')
  proxies_table = soup.find("table")

  # Save proxies in the array
  for row in proxies_table.find_all('tr'):
    cells=row.find_all("td")
    row_data=[]
    for cell in cells:
      row_data.append((cell.text.strip()))
    if len(row_data) ==8:
      proxies.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
      })

def proxy_finder_geonode():
  url = "https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc"  # Replace with the actual URL of the site

  response = requests.get(url)
  if response.status_code == 200:
      data = json.loads(response.text)
      if "data" in data and len(data["data"]) > 0:
        for item in data["data"]:
          ip = item.get("ip")
          port = item.get("port")
          proxies.append(({
      'ip': ip,
      'port': port
      }))

def proxy_checker():
  # Choose a random proxy
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

  for n in range(1, 100):
    req = Request('http://icanhazip.com')
    req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

    # Every 10 requests, generate a new proxy
    if n % 10 == 0:
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

    # Make the call
    try:
      my_ip = urlopen(req).read().decode('utf8')
      working_ones+=1
      print('#' + str(n) + ': ' + my_ip)
    except: # If error, delete this proxy and find another one
      del proxies[proxy_index]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

def proxy_final_check(ip:str):
  req = Request('http://icanhazip.com')
  req.set_proxy(ip,"http")
  try:
      urlopen(req).read().decode('utf8')
      print("proxy working")
      return ip
  except: # If error, delete this proxy and find another one
      print('Proxy not working')
      next_ip = next(proxy_gen)
      print(f"switching to {next_ip}")
      return proxy_final_check(next_ip)

def random_proxy():
  return random.randint(0, len(proxies) - 1)

def proxy_offerer():
  while True:
     picked_proxy=proxies[0]
     ip=picked_proxy["ip"]
     port=picked_proxy["port"]
     proxy_format=(f"{ip}:{port}")
     yield proxy_format
     proxies.remove(proxies[0])
   
# SCRAPING USER's
def users():
   with open("fine_filtered_data.csv") as imput_file:
      user_data=csv.reader(imput_file,delimiter=";",lineterminator="\n",quotechar='"')
      user_profiles = []

      for row in user_data:
         if "link" != row[2]:
            user_name=row[0].split()
            user_name="_".join(user_name)
            user_profiles.append((user_name.lower(),row[2]))
      return user_profiles

def less_used_user():
    return_user=()
    user_use_count=100000
    for user in user_list:
        if user.used<user_use_count:
            user_use_count=user.used
            return_user=user
    return return_user

# SCRAPING functions



def scraper_main():
  global user_index

  proxy=proxy_final_check(next(proxy_gen))

  print(f"acting as: {proxy}")

  #options = uc.ChromeOptions()

  #options.add_argument(f'--proxy-server={proxy}')
  #options.add_argument("start-maximized")

  print("starting driver:")

  #driver = uc.Chrome(options=options)

  time.sleep(2)

  #chosen_one=less_used_user()
  #chosen_one.add_use()
  #email = chosen_one.user
  #password = chosen_one.password

  #driver.get("https://www.google.com/")
  profiles=users()
  #actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
  for s in range((len(profiles)-user_index)):
    user_name = profiles[user_index][0]
    user_link = profiles[user_index][1]
    print(user_index)
    if user_index%10==0:
      person_data = Person(user_link, driver=driver,close_on_complete=True, scrape=True)
      time.sleep(180+random(0,180))
      #time.sleep(3)
      
      user_index+=1
      scraper_main()
    else:
      
      time.sleep(180+random(0,180))

      person_data = Person(user_link, driver=driver,close_on_complete=False,scrape=True)
      #data_result.append({user_name:person_data})
      writer.writerow({"name":person_data.name,"bio":person_data.about,"experiences":person_data.experiences,"educations":person_data.interests,"accomplishment":person_data.accomplishments,"company":person_data.company,"job_title":person_data.job_title})
      user_index+=1
    


  
     




ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]
user_list_raw="user_list.csv"
user_list=[]
user_index=0


print("loading proxies")
proxy_finder()
proxy_finder_geonode()

Thread(target=proxy_checker, daemon=True).start()

working_ones=0
print("finding proxies...")

time.sleep(10)

proxy_gen = proxy_offerer()

data_result=[]

kohde="kesko"

with open((f"{kohde}_user_data.csv"), "a") as log_file:
  fieldnames=["name","bio","link","tier","department","student"]
  writer = csv.DictWriter(log_file,delimiter=";",lineterminator="\n",quotechar='"',fieldnames=fieldnames)
  writer.writeheader()
   


scraper_main()


proxy=proxy_final_check(next(proxy_gen))

#driver.get('https://nowsecure.nl')


time.sleep(15)




#driver.get('http://icanhazip.com')
#print(users())

def login_users():
  with open(user_list_raw) as users:
      for user in users:
        row = user.replace("\n", "")
        data = row.split(";")
        print(data)
        if data[0]!="\ufeffusername":
            user_list.append(ScrapingUser(data[0],data[1],data[2]))
      users.close()













#if __name__ == '__main__':
  #proxy_finder()