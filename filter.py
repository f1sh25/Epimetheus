from bs4 import BeautifulSoup
import csv

def filter_text_by_class(html_file, class_name):
    with open(html_file, 'r', encoding='utf-8') as file:  # Specify the correct encoding here
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    filtered_text = []

    for element in soup.find_all(class_=class_name):
        if element.text.strip():
            filtered_text.append(element.text.strip())

    return filtered_text

def profile_creater(names: list):
    profiles = []
    for name in names:
        first_last_name = name.split()
        link=(f"https://www.linkedin.com/in/{first_last_name[0].lower()}-{first_last_name[1].lower()}")
        profiles.append(link)
    return profiles




# Example usage
html_file = 'metadata.html'  # Replace with your input file name
class_name = "ember-view lt-line-clamp lt-line-clamp--single-line org-people-profile-card__profile-title t-black"  # Replace with the HTML class name you want to filter

names = filter_text_by_class(html_file, class_name)

class_name = "ember-view lt-line-clamp lt-line-clamp--multi-line"

bios = filter_text_by_class(html_file, class_name)

profile_link = profile_creater(names)




with open("filtered_data.csv", "w") as users_csv:
    fieldnames=["name","bio","link"]
    writer = csv.DictWriter(users_csv,delimiter=";",lineterminator="\n",quotechar='"',fieldnames=fieldnames)
    writer.writeheader()
    for index in range(len(names)):
        try:
            writer.writerow({"name":names[index],"bio":bios[index],"link":profile_link[index]})
        except:
            writer.writerow({"name":names[index],"bio":None,"link":profile_link[index]})