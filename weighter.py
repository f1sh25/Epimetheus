data_list=[]
import ast
import csv
import weighter_keywords

class Target:

    def __init__(self, rivi:list):
       
        self.name = rivi[0]
        self.link = rivi[1]
        self.intro = rivi[2]
        self.location = rivi[3]
        self.about = rivi[4]
        self.skills = rivi[5]
        self.experiences = ast.literal_eval(rivi[6])
        self.accomplishments = ast.literal_eval(rivi[7])
        self.education = ast.literal_eval(rivi[8])
        self.connections = rivi[9]
        self.interests = rivi[10]
        self.department = ""
        self.department_value = 0
        self.status = ""
        self.status_value = 0
        self.education_level = ""
        self.education_level_weight = 0
        self.education_keyword = ""
        self.education_keyword_weight = 0
        self.education_year=0
        self.asigned_to_study_class=False


def csv_reader():
    with open("output.csv", newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[0]=="name":
                pass
            else:
                henkilö = Target(row)
                data_list.append(henkilö)


class CompanyDepartments:

    def department_finder(person:Target):
        department_keywords = weighter_keywords.department_keywords
        department_values = weighter_keywords.department_impact
        index=0
        for keywords in department_keywords:
            for keyword in department_keywords[keywords]:
                if keyword.lower() in person.about.lower() or keyword.lower() in person.intro.lower() and person.department=="":
                    person.department=keywords
                    person.department_value=department_values[keywords]
            
    
        

class StatusWeighter:
    def status_finder(person:Target):
        status_keywords = weighter_keywords.employment_status_keywords
        status_values = weighter_keywords.employment_status_importance
        index=0
        
        for keywords in status_keywords:
            for keyword in status_keywords[keywords]:
                if keyword.lower() in person.about.lower() or keyword.lower() in person.intro.lower() and person.status=="":
                    person.status=keywords
                    person.status_value=status_values[keywords]
                    


class EducationWeigter:
    def education_finder(person:Target):
        
        for education in person.education:

            education_desc=education[1]
            try:
                education_year_raw=education[2]
                education_year=education_year_raw.split(" - ")
                education_year=[int(year) for year in education_year]
            except:
                education_year=[0]
            

            for education_keyword in weighter_keywords.education_keyword_ratings:
                if education_keyword.lower() in education_desc.lower() and person.education_keyword=="":
                    person.education_keyword=education_keyword
                    person.education_keyword_weight=weighter_keywords.education_keyword_ratings[education_keyword]
                    person.education_year=education_year

            for education_level in weighter_keywords.education_level_keyword:
                for education_keyword in weighter_keywords.education_level_keyword[education_level]:
                    if education_keyword.lower() in education_desc.lower() and person.education_level_weight<weighter_keywords.education_ratings[education_level]:
                        person.education_level=education_level
                        person.education_level_weight = weighter_keywords.education_ratings[education_level]



if __name__ == "__main__":

    csv_reader()


    dep = CompanyDepartments()
    status = StatusWeighter()
    education = EducationWeigter()
    for person in data_list:
        status.status_finder(person)
        education.education_finder(person)




