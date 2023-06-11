from neo4j import GraphDatabase
import epimetheus_adv_matcher
import ast
import csv

data_list=[]
URI = "neo4j://localhost"
AUTH = ("neo4j", "password")
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()


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


class Database_updater:
    def input_users(self):
        for user in data_list:
            summary = driver.execute_query(
            "MERGE (:Person {name: $name})",  
            name=user.name,  
            database_="neo4j",  
            )
    def delete_all_users(self):
        for user in data_list:
            records, summary, keys = driver.execute_query("""
            MATCH (p:Person {name: $name})
            DETACH DELETE p
            """, name=user.name,
            database_="neo4j",
            )
        print(f"Query counters: {summary.counters}.")

    def update_about(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.about = $about
        """, name=person.name, about=person.about,
        database_="neo4j",
        )

    def update_location(self,person:Target):
    
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.location = $location
        """, name=person.name, location=person.location,
        database_="neo4j",
        )
    
    def update_link(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.link = $link
        """, name=person.name, link=person.link,
        database_="neo4j",
        )
    
    def update_intro(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.intro = $intro
        """, name=person.name, intro=person.intro,
        database_="neo4j",
        )
    
    def update_skills(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.skills = $skills
        """, name=person.name, skills=person.skills,
        database_="neo4j",
        )

    def update_experiences(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.experiences = $experiences
        """, name=person.name, experiences=str(person.experiences),
        database_="neo4j",
        )
    
    def update_education(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.education = $education
        """, name=person.name, education=str(person.education),
        database_="neo4j",
        )
    
    def update_accomplishments(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.accomplishments = $accomplishments
        """, name=person.name, accomplishments=str(person.accomplishments),
        database_="neo4j",
        )
    
    def update_connections(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.connections = $connections
        """, name=person.name, connections=person.connections,
        database_="neo4j",
        )

    def update_skills(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.skills = $skills
        """, name=person.name, skills=person.skills,
        database_="neo4j",
        )
    
    def update_interests(self, person: Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:Person {name: $name})
        SET p.interests = $interests
        """, name=person.name, interests=person.interests,
        database_="neo4j",
        )
    
    
    def update_all(self,person:Target):
        #try:
            #self.input_users()
            self.update_intro(person=person)
            self.update_accomplishments(person=person)
            self.update_about(person=person)
            self.update_connections(person=person)
            self.update_experiences(person=person)
            self.update_education(person=person)
            self.update_link(person=person)
            self.update_skills(person=person)
            self.update_location(person=person)
            self.update_interests(person=person)
        #except:
            #pass


class Database_matchmaker:
    def location_matcher(person:Target):
        location = person.location.split(",")
        if len(location)==3:
            records, summary, keys = driver.execute_query("""
            MATCH (p:Person {name: $name}),(c:city {name: $city})
            MERGE (p)-[:located_in]->(c)
            """, name=person.name, city=location[0],
            database_="neo4j",
            )
    
    def city_matchmaker():
        location_filter()
        for city in cities_provinces: 
            records, summary, keys = driver.execute_query("""
            MATCH (c:city {name: $city}),(p:Province {name: $province})
            MERGE (c)-[:in]->(p)
            """, city=city[0], province=city[1],
            database_="neo4j",
        )
        print(f"Query counters: {summary.counters}.")


    def country_matchmaker():
        location_filter()
        for city in cities_provinces: 
            records, summary, keys = driver.execute_query("""
            MATCH (c:Province {name: $Province}),(p:Country{name:"Finland"})
            MERGE (c)-[:in]->(p)
            """, Province=city[1],
            database_="neo4j",
        )
    
    def education_matchmaker(person:Target):
        education = person.education
        for school in education:
            records, summary, keys = driver.execute_query("""
            MATCH (p:Person {name: $name}),(c:School {name: $School})
            MERGE (p)-[:studied_in]->(c)
            """, name=person.name, School=school[0],
            database_="neo4j",
            )
    
    def experience_matchmaker(person: Target):
        experiences = person.experiences
        for experience in experiences:
            if " · Full-time" in experience[1]:
                company= experience[1].replace(" · Full-time","")
            else:
                company= experience[1]
            
            if "Present" in experience[2]:
                records, summary, keys = driver.execute_query("""
                MATCH (p:Person {name: $name}),(c:Company {name: $Company})
                MERGE (p)-[:Works_currently_at]->(c)
                """, name=person.name, Company=company,
                database_="neo4j",
                )
            else:
                records, summary, keys = driver.execute_query("""
                MATCH (p:Person {name: $name}),(c:Company {name: $Company})
                MERGE (p)-[:Worked_at]->(c)
                """, name=person.name, Company=company,
                database_="neo4j",
                )


class Database_deleter:
    def delete_all_users():
        for user in data_list:
            records, summary, keys = driver.execute_query("""
            MATCH (p:Person {name: $name})
            DETACH DELETE p
            """, name=user.name,
            database_="neo4j",
            )
        print(f"Query counters: {summary.counters}.")


    def delete_all_cities():
        for city in cities:
            records, summary, keys = driver.execute_query("""
            MATCH (p:city {name: $name})
            DETACH DELETE p
            """, name=city,
            database_="neo4j",
            )
        print(f"Query counters: {summary.counters}.")


    def delete_all_provinces():
        for province in provinces:
            records, summary, keys = driver.execute_query("""
            MATCH (p:Province {name: $name})
            DETACH DELETE p
            """, name=province,
            database_="neo4j",
            )
        print(f"Query counters: {summary.counters}.")

    def delete_all_schools():
        schools=school_filter()
        for school in schools:
            records, summary, keys = driver.execute_query("""
            MATCH (p:School {name: $name})
            DETACH DELETE p
            """, name=school,
            database_="neo4j",
            )
        print(f"Query counters: {summary.counters}.")

    


def csv_reader():
    with open("output.csv", newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[0]=="name":
                pass
            else:
                henkilö = Target(row)
                data_list.append(henkilö)

                    

csv_reader()

#for user in data_list:
    #print(user.location)
# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"

cities=[]
provinces=[]
cities_provinces=[]

def location_filter():
    for user in data_list:
        location = user.location.split(",")
        if len(location)==3 and location[0] not in cities:
            if location[1] not in provinces:
                provinces.append(location[1])
            cities.append(location[0])
            cities_provinces.append((location[0],location[1]))


def location_creater():
    for provice in provinces:
            summary = driver.execute_query(
            "MERGE (:Province {name: $name})",  
            name=provice,  
            database_="neo4j",  
            ).summary
            
    for city in cities:
            summary = driver.execute_query(
            "MERGE (:city {name: $name})",  
            name=city,  
            database_="neo4j",  
            ).summary


def school_filter():
    unique_schools = []
    for target in data_list:
        
        education_raw = target.education
        if education_raw=="education":
            pass
        else:
            #print(type(education_raw))
            
            try:
                for school in education_raw:
                    if school[0] not in unique_schools:
                        unique_schools.append(school[0])
            except:
                pass
    return unique_schools


def school_creater():
    schools=school_filter()
    for school in schools:
        summary = driver.execute_query(
        "MERGE (:School {name: $name})",  
        name=school,  
        database_="neo4j",  
        ).summary
    print("Created {nodes_created} nodes in {time} ms.".format(
        nodes_created=summary.counters.nodes_created,
        time=summary.result_available_after
    ))
        
    
def experience_fiter():
    unique_experiences = []
    for target in data_list:
        experiences=target.experiences
        for experience in experiences:
            if " · Full-time" in experience[1]:
                company= experience[1].replace(" · Full-time","")
            else:
                company= experience[1]

            if company not in unique_experiences:
                unique_experiences.append(company)
    return unique_experiences


def experience_creater():
    experineces=experience_fiter()
    for expoerience in experineces:
        summary = driver.execute_query(
        "MERGE (:Company {name: $name})",  
        name=expoerience,  
        database_="neo4j",  
        ).summary
    print("Created {nodes_created} nodes in {time} ms.".format(
        nodes_created=summary.counters.nodes_created,
        time=summary.result_available_after
    ))


#experience_creater()
delter = Database_deleter
#school_creater()
#location_creater()
#city_matchmaker()
#country_matchmaker()
#delter.delete_all_users()

database = Database_updater()

for person in data_list:
    database.update_all(person=person)
    #print(person.intro)
    Database_matchmaker.location_matcher(person)
    Database_matchmaker.education_matchmaker(person)
    Database_matchmaker.experience_matchmaker(person)
    
epimetheus_adv_matcher.buddies()

