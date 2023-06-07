import os
import csv
import time
from bs4 import BeautifulSoup

current_index=0
class Target:
    def __init__(self, name:str,link:str):
        self.name=name
        self.link=link
        self.intro = ""
        self.about="" #kesken
        self.skills=[]
        self.location=""
        self.experiences=[]
        self.interests=[]
        self.accomplishments=[]
        self.education=[]
        self.connections=""


    def section_finder(self,id:str):
        with open("RAW.html", 'r', encoding='utf-8') as file:
            html = file.read()
        soup = BeautifulSoup(html, "html.parser")
        sections = soup.find_all(class_="artdeco-card ember-view relative break-words pb3 mt2")
        for section in sections:
            if section.find("div", {"id":id}):
                return section
        return None
    

    def find_intro(self):
        with open("RAW.html", 'r', encoding='utf-8') as file:
            html = file.read()
        soup = BeautifulSoup(html, "html.parser")
        intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
        works_at_loc = intro.find("div", {'class': 'text-body-medium'})
        self.intro = works_at_loc.get_text().strip()
        location = soup.find(class_="text-body-small inline t-black--light break-words")
        self.location = location.text.strip()
       
    def find_about(self):
        about_box = self.section_finder("about")
        about_tag= about_box.find(class_="pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center")
        self.about=about_tag.find(class_="visually-hidden").text.strip()
        

    def find_experiences(self):
        experience = self.section_finder("experience")
        for li_tag in experience.find_all(class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"):
            title_tag=li_tag.find(class_="mr1 t-bold")
            desc_tag = li_tag.find(class_="t-14 t-normal")
            dur_tag =li_tag.find(class_="t-14 t-normal t-black--light")
            try:
                job_title=title_tag.find(class_="visually-hidden")
                desc=desc_tag.find(class_="visually-hidden")
                dur=dur_tag.find(class_="visually-hidden")
                #strip text out
                self.experiences.append((job_title.text.strip(),desc.text.strip(),dur.text.strip()))
            except:
                pass
            
    def find_education(self):
        education = self.section_finder("education")
        for li_tag in education.find_all(class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"):
            title_tag = li_tag.find(class_="mr1 hoverable-link-text t-bold")
            desc_tag = li_tag.find(class_="t-14 t-normal")
            dur_tag = li_tag.find(class_="t-14 t-normal t-black--light")

            try:
                dur=dur_tag.find(class_="visually-hidden")
                title=title_tag.find(class_="visually-hidden")
                desc=desc_tag.find(class_="visually-hidden")
                #strip text out
                self.education.append((title.text.strip(),desc.text.strip(),dur.text.strip()))
            except:
                try:
                    title=title_tag.find(class_="visually-hidden")
                    desc=desc_tag.find(class_="visually-hidden")
                    #strip text out
                    self.education.append((title.text.strip(),desc.text.strip()))
                
                except:
                    pass

    def find_connections(self):
        with open("RAW.html", 'r', encoding='utf-8') as file:
            html = file.read()
        soup = BeautifulSoup(html, "html.parser")
        connection_field = soup.find(class_="pv-top-card--list pv-top-card--list-bullet")
        connections_raw=connection_field.text.strip()
        connections_lst=connections_raw.split()
        self.connections = connections_lst[0] 

    def find_skills(self):
        skills=self.section_finder("skills")
        for li_tag in skills.find_all(class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"):
            skill_tag=li_tag.find(class_="mr1 hoverable-link-text t-bold")
            endorsments_tag = li_tag.find(class_="pvs-list__outer-container")
            endorsment_count = endorsments_tag.find_all(class_="pvs-list__item--one-column")
            
            try:
                skill = skill_tag.find(class_="visually-hidden")
                endorsments = endorsment_count[-2].find(class_="visually-hidden")
            except:
                pass    
            self.skills.append((skill.text.strip(),endorsments.text.strip()))
                

    def find_interest(self):
        interests_location = self.section_finder("interests")
        interests_tab = interests_location.find(class_="pvs-list ph5 display-flex flex-row flex-wrap")
        for li_tag in interests_tab.find_all(class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--two-column"):
            title_tag = li_tag.find(class_="display-flex flex-wrap align-items-center full-height")
            desc_tag = li_tag.find(class_="t-14 t-normal")
            folowers_tag = li_tag.find(class_="t-14 t-normal t-black--light" )
            try:
                desc=desc_tag.find(class_="visually-hidden")
                title=title_tag.find(class_="visually-hidden")
                
                folowers=folowers_tag.find(class_="visually-hidden")
                
                #strip text out
                
                self.interests.append((title.text.strip(),desc.text.strip(),folowers.text.strip()))
            except:
                try:

                    title=title_tag.find(class_="visually-hidden")
                    folowers=folowers_tag.find(class_="visually-hidden")
                
                #strip text out
                
                    self.interests.append((title.text.strip(),None,folowers.text.strip()))    
                except:
                    pass


    def find_accomplishments(self):
        interests = self.section_finder("honors_and_awards")
        for li_tag in interests.find_all(class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"):
            title_tag = li_tag.find(class_="display-flex flex-wrap align-items-center full-height")
            desc_tag = li_tag.find(class_="t-14 t-normal")
            try:
                title=title_tag.find(class_="visually-hidden")
                desc=desc_tag.find(class_="visually-hidden")
                #strip text out
                
                self.accomplishments.append((title.text.strip(),desc.text.strip()))
            except:
                pass

    def scrape(self):
        #func_list=[self.find_about(),self.find_education(),self.find_experiences(),, self.find_skills(),self.find_accomplishments()]

        try:
            self.find_about()
        except:
            pass
        try:
            self.find_connections()
        except:
            pass
        try:
            self.find_interest()
        except:
            pass
        try:
            self.find_education()
        except:
            pass
        try:
            self.find_experiences()
        except:
            pass
        try:
            self.find_intro()
        except:
            pass
        try:
            self.find_skills()
        except:
            pass
        try:
            self.find_accomplishments()
        except:
            pass

            
            
            
            
            
    

    

class AppFunctions:

    def users():
        with open("fine_filtered_data.csv") as imput_file:
            user_data=csv.reader(imput_file,delimiter=";",lineterminator="\n",quotechar='"')
            user_profiles = []
            for row in user_data:
                if "link" != row[2]:
                    name = row[0]
                    user_name=row[0].split()
                    user_name="_".join(user_name)
                    user_profiles.append((name, user_name.lower(),row[2]))
        return user_profiles
    

    def user_offerer(user_list:list):
        for user in user_list:
            global current_index
            current_index+=1
            yield(user)

    def create_new_output_file():
        with open("output.csv","w", encoding="utf-8") as output_file:
            fieldnames=["name","link","intro","location","about","skills","experiences","accomplishments","education","connections","interests"]
            writer = csv.DictWriter(output_file,delimiter=";",lineterminator="\n",quotechar='"',fieldnames=fieldnames)
            writer.writeheader()

    def target_data_loging(person:Target):
        with open("output.csv","a",encoding="utf-8") as output_file:
            fieldnames=["name","link","intro","location","about","skills","experiences","accomplishments","education","connections","interests"]
            writer = csv.DictWriter(output_file,delimiter=";",lineterminator="\n",quotechar='"',fieldnames=fieldnames)
            writer.writerow({"name":person.name,"link":person.link,"intro":person.intro,"location":person.location,"about":person.about,"skills":person.skills,"experiences":person.experiences,"accomplishments":person.accomplishments,"education":person.education,"connections":person.connections,"interests":person.interests})

    def progress_checker():
        processed_names = []
        
        with open("output.csv", encoding="utf-8") as output_file:
            for line in output_file:
                row=line.replace("\n","")
                data = row.split(";")

                if data[0]=="name":
                    pass
                else:
                    processed_names.append(data[0])
                    
        return processed_names
        #check user offerer status




    def raw_file_creater():
        comandstring=f"notepad.exe RAW.html"
        os.system(comandstring)

    def raw_file_clearer():
        with open("RAW.html","w") as file:
            file.write("")



class App:
    def __init__(self):
        target_list=AppFunctions.users()
        self.target_list_length=len(target_list)
        self.target_generator = AppFunctions.user_offerer(target_list)
        
    def manual(self):
        print("Commands:")
        print("1 Continue/start")
        print("2 View Stats")
        print("3 check progress") 
        print("4 manual entry")
        print("420 to clear output")
        print("69 Stop")
    
    def start(self):
        self.manual()
        while True:
            print()

            command = input("Command: ")
            if command == "69":
                print("goodbye!")
                break
            elif command == "1":
                self.add_data()
            elif command == "2":
                self.stats()
            elif command == "3":
                self.check_progress()
            elif command == "4":
                self.manual_entry()
            elif command == "420":
                self.clear_file()
            else:
                self.manual()
    def add_data(self):
        target = next(self.target_generator)
        name=target[0]
        link=target[2]
        print("Current Target: ")
        print(f"name: {name}, link:{link}")
        print("input HTML site code")
        AppFunctions.raw_file_creater()
        person_data=Target(name,link)
        
        person_data.scrape()
        
        AppFunctions.target_data_loging(person_data)

        AppFunctions.raw_file_clearer()
    
    def stats(self):
        global current_index
        print()
        print(f"Progress: {round(current_index/self.target_list_length*100)}%:({current_index}/{self.target_list_length})")

    def check_progress(self):
        global current_index
        processed_names = AppFunctions.progress_checker()
        
        if len(processed_names)>0:
            for s in range(self.target_list_length):
                name = next(self.target_generator)
                if processed_names[-1]==name[0]:
                    current_index=s+1
                    print("progress updated!")
                    break
        
    def manual_entry(self):
        name=input("input target name: ")
        link=input("input target profile link: ")
        print("Current Target: ")
        print(f"name: {name}, link:{link}")
        print("input HTML site code")
        AppFunctions.raw_file_creater()
        person_data=Target(name,link)
        
        person_data.scrape()
        
        AppFunctions.target_data_loging(person_data)

        AppFunctions.raw_file_clearer()

    def clear_file(self):
        while True:
            command=input("Are you sure? (Y/N): ").lower()
            if command=="y":
                AppFunctions.create_new_output_file()
                print()
                print("file cleared!")
                break
            elif command=="n":
                break
            else:
                print("incorrect input!")



aplication = App()
aplication.start()