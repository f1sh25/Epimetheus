from bs4 import BeautifulSoup
import csv

def filter_text_by_class(html_file, class_name):
    with open(html_file, 'r', encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    name = []
    

    for element in soup.find_all(class_=class_name):
        if element.text.strip():
            name.append(element.text.strip())

    bios_list = []
    for element in soup.find_all(class_=bio_class_name):
        if element.text.strip():
            bios_list.append(element.text.strip())

    href_values = []

    for element in soup.find_all('a', class_=href_class_name):
        href = element.get('href')
        href_componets=href.split("?")
        if href:
            href_values.append(href_componets[0])

    return (name, href_values ,bios_list)

def profile_creater(names: list):
    profiles = []
    for name in names:
        first_last_name = name.split()
        link=(f"https://www.linkedin.com/in/{first_last_name[0].lower()}-{first_last_name[1].lower()}")
        profiles.append(link)
    return profiles


html_file = 'metadata.html'
class_name = "ember-view lt-line-clamp lt-line-clamp--single-line org-people-profile-card__profile-title t-black"
href_class_name='app-aware-link link-without-visited-state'
bio_class_name = "ember-view lt-line-clamp lt-line-clamp--multi-line"

names_link = filter_text_by_class(html_file, class_name)


names = names_link[0]

bios = names_link[2]

profile_link = names_link[1]

for bio in bios:
    print(bio)


with open("filtered_data.csv", "w") as users_csv:
    fieldnames=["name","bio","link"]
    writer = csv.DictWriter(users_csv,delimiter=";",lineterminator="\n",quotechar='"',fieldnames=fieldnames)
    writer.writeheader()
    for index in range(len(names)):
        try:
            writer.writerow({"name":names[index],"bio":bios[index],"link":profile_link[index]})
        except:
            writer.writerow({"name":names[index],"bio":None,"link":None})
            