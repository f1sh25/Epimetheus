from neo4j import GraphDatabase
from graphdatascience import GraphDataScience
import epimetheus_adv_matcher
import pandas as pd
from tqdm import tqdm
from weighter import *



URI = "neo4j://localhost"
AUTH = ("neo4j", "password")
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

gds = GraphDataScience(URI, AUTH, database="neo4j")

target_company = "Kesko - K-Group"

class DatabaseUpdaterForPOI:
    def __init__(self, company):
        self.company = company

    def input_users(self, person: Target):
        
            summary = driver.execute_query(
            "MERGE (p:TMP {name: $name})",  
            name=person.name,  
            database_="neo4j",  
            )
    def delete_all_users(self, person: Target):
        
            records, summary, keys = driver.execute_query("""
            MATCH (p:TMP {name: $name})
            DETACH DELETE p
            """, name=person.name,
            database_="neo4j",
            )
            

    def update_about(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.about = $about
        """, name=person.name, about=person.about,
        database_="neo4j",
        )

    def update_location(self,person:Target):
    
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.location = $location
        """, name=person.name, location=person.location,
        database_="neo4j",
        )
    
    def update_link(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.link = $link
        """, name=person.name, link=person.link,
        database_="neo4j",
        )
    
    def update_intro(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.intro = $intro
        """, name=person.name, intro=person.intro,
        database_="neo4j",
        )
    
    def update_skills(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.skills = $skills
        """, name=person.name, skills=person.skills,
        database_="neo4j",
        )

    def update_experiences(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.experiences = $experiences
        """, name=person.name, experiences=str(person.experiences),
        database_="neo4j",
        )
    
    def update_education(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.education = $education
        """, name=person.name, education=str(person.education),
        database_="neo4j",
        )
    
    def update_accomplishments(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.accomplishments = $accomplishments
        """, name=person.name, accomplishments=str(person.accomplishments),
        database_="neo4j",
        )
    
    def update_connections(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.connections = $connections
        """, name=person.name, connections=person.connections,
        database_="neo4j",
        )

    def update_skills(self,person:Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.skills = $skills
        """, name=person.name, skills=person.skills,
        database_="neo4j",
        )
    
    def update_interests(self, person: Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        SET p.interests = $interests
        """, name=person.name, interests=person.interests,
        database_="neo4j",
        )
    
    def find_nodeID(self, person: Target):
        records, summary, keys = driver.execute_query("""
        MATCH (p:TMP {name: $name})
        return ID(p) as nodeID
        """, name=person.name, interests=person.interests,
        database_="neo4j",
        )
       
        id = (records[0].data()["nodeID"])
        person.id = id
    
    
    def update_all(self,person:Target):
        #try:
            self.input_users(person)
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
            self.find_nodeID(person)
        #except:
            #pass


class Database_matchmaker:
    def location_matcher(person:Target):
        location = person.location.split(",")
        if len(location)==3:
            records, summary, keys = driver.execute_query("""
            MATCH (p:TMP {name: $name}),(c:city {name: $city})
            MERGE (p)-[:located_in]->(c)
            """, name=person.name, city=location[0],
            database_="neo4j",
            )
    
    def education_matchmaker(person:Target):
        education = person.education
        for school in education:
            records, summary, keys = driver.execute_query("""
            MATCH (p:TMP {name: $name}),(c:School {name: $School})
            MERGE (p)-[:studied_in]->(c)
            """, name=person.name, School=school[0],
            database_="neo4j",
            )
    
    def experience_matchmaker(person: Target):
        experiences = person.experiences
        for experience in experiences:
            if " · Full-time" in experience[1]:
                company= experience[1].replace(" · Full-time","")
            elif " · Part-time" in experience[1]:
                company= experience[1].replace(" · Part-time","")
            else:
                company= experience[1]
            
            if "Present" in experience[2]:
                records, summary, keys = driver.execute_query("""
                MATCH (p:TMP {name: $name}),(c:Company {name: $Company})
                MERGE (p)-[:Works_currently_at]->(c)
                """, name=person.name, Company=company,
                database_="neo4j",
                )
            else:
                records, summary, keys = driver.execute_query("""
                MATCH (p:TMP {name: $name}),(c:Company {name: $Company})
                MERGE (p)-[:Worked_at]->(c)
                """, name=person.name, Company=company,
                database_="neo4j",
                )

poi_dict = {}

targets = []
class TemporaryPeople:

    def find_targets(self):
        usr_list = []
        peoples, summary, keys = driver.execute_query("""
                    MATCH (n:Person)-[r:Works_currently_at]->(:Company {name: $company}) return n
                    """, company = target_company,
                    database_="neo4j"
                    )
        print(f"Query counters: {summary.counters}.")
        
        for usr in peoples:
            data = usr.data()
            
            try:
                interests = data["n"]["interests"]
            except:
                interests = []
            data_list=[data["n"]["name"],data["n"]["link"],data["n"]["intro"],data["n"]["location"],data["n"]["about"],data["n"]["skills"],data["n"]["experiences"],data["n"]["accomplishments"],data["n"]["education"],data["n"]["connections"],interests]
            usr_list.append(Target(data_list))
        return usr_list
    

    
        


    def create_people(self):
        global targets
        targets = self.find_support_people()

        db_updater = DatabaseUpdaterForPOI(company=target_company)
        total_iterations = len(targets)
        progress_bar = tqdm(total=total_iterations, desc="Matching nodes")
        for person in targets:
            db_updater.update_all(person)
            Database_matchmaker.education_matchmaker(person)
            Database_matchmaker.experience_matchmaker(person)
            Database_matchmaker.location_matcher(person)
            progress_bar.update(1)
        
        progress_bar.close()


        dep = CompanyDepartments()
        for person in targets:
            dep.previous_department_finder(person)

        poi_list = high_value_person_finder(targets)
        global poi_dict
        for poi in poi_list:
            poi_dict[poi[2]]=poi[1]
        
        

    


    def find_support_people(self):
        
        tmp_users = self.find_targets()
        tmp_users_name_list = [user.name for user in tmp_users]
        
        #print(tmp_users_name_list)
    

        

        print("find all company nodes")
        companies, summary, keys = driver.execute_query(
        "MATCH (n:TMP)-[r:Worked_at]->(p:Company) RETURN p.name AS name",
        database_="neo4j",
        )
        # Summary information
        #print("The query `{query}` returned {records_count} records in {time} ms.".format(
            #query=summary.query, records_count=len(companies),
            #time=summary.result_available_after))
        
        #print("find all school nodes")
        schools, summary, keys = driver.execute_query(
        "MATCH (n:TMP)-[r:studied_in]->(p:School) RETURN p.name AS name",
        database_="neo4j",
        )

        #print("find all persons connected to the company")

        progress_bar = tqdm(total=len(companies)+len(schools), desc="searching POI...")

        for raw_company in companies:
       
            company = raw_company.value()
            record, summary, keys = driver.execute_query(
            "MATCH p=(n:Person)-[r:Worked_at]->(:Company {name: $name}) RETURN n",
            database_="neo4j", name=company
            )
            #print(school)
            
            for person in record:
                data = person.data()
                
                try:
                    interests = data["n"]["interests"]
                except:
                    interests = []

                data_list=[data["n"]["name"],data["n"]["link"],data["n"]["intro"],data["n"]["location"],data["n"]["about"],data["n"]["skills"],data["n"]["experiences"],data["n"]["accomplishments"],data["n"]["education"],data["n"]["connections"],interests]
                if data["n"]["name"] not in tmp_users_name_list:
                    #print('Found support target  ' + data_list[0])
                    tmp_users.append(Target(data_list))
                    tmp_users_name_list.append(data_list[0])
            #print()
            progress_bar.update(1)


       
        # Summary information
        #print("The query `{query}` returned {records_count} records in {time} ms.".format(
            #query=summary.query, records_count=len(schools),
            #time=summary.result_available_after))
        


        #print("find all persons connected to the school")
        
        #progress_bar = tqdm(total=len(schools), desc="find all persons connected to the school")

        for raw_school in schools:
       
            school = raw_school.value()
            record, summary, keys = driver.execute_query(
            "MATCH p=(n:Person)-[r:studied_in]->(:School {name: $name}) RETURN n",
            database_="neo4j", name=school
            )
            #print(school)
            
            for person in record:
                data = person.data()
                #print(data["n"]["name"])
                try:
                    interests = data["n"]["interests"]
                except:
                    interests = []

                data_list=[data["n"]["name"],data["n"]["link"],data["n"]["intro"],data["n"]["location"],data["n"]["about"],data["n"]["skills"],data["n"]["experiences"],data["n"]["accomplishments"],data["n"]["education"],data["n"]["connections"],interests]
                if data["n"]["name"] not in tmp_users_name_list:
                    #print('Found support target  ' + data_list[0])
                    tmp_users.append(Target(data_list))
                    tmp_users_name_list.append(data_list[0])
            #print()
            progress_bar.update(1)

        progress_bar.close()
        return tmp_users
        

    






tmp =TemporaryPeople()

tmp.create_people()
tmp.create_people()
epimetheus_adv_matcher.company_buddies()
epimetheus_adv_matcher.school_buddies()
db_upt = DatabaseUpdaterForPOI(company=target_company)


res = gds.graph.project.estimate(["TMP"],["studied_school_same_time", "worked_same_company", "studied_same_school", "studied_same_school_time_same_place"],readConcurrency=4 )

#print(res["bytesMax"])

try:
    #G, result = gds.graph.project("tmp-graph",["TMP"],[{"studied_school_same_time": {"properties": ["weight"]}}, "worked_same_company", "studied_same_school", "studied_same_school_time_same_place"],readConcurrency=4 )
    G, result = gds.graph.project("tmp-graph",["TMP"],[{"studied_school_same_time": {"properties": ["weight","cost"]}}, {"worked_same_company": {"properties": ["weight","cost"]}}, {"studied_same_school": {"properties": ["weight","cost"]}}, {"studied_same_school_time_same_place": {"properties": ["weight","cost"]}}],readConcurrency=4 )
    assert G.node_count() == result["nodeCount"]
except:
    G = gds.graph.get('tmp-graph')



center_result = gds.eigenvector.stream(G,relationshipWeightProperty="weight", maxIterations=20)

sorted_results = center_result.sort_values(by=["score"])

last_50_nodes = sorted_results['nodeId'].tolist()

df_list = []
user_central_list = []

progress_bar = tqdm(total=len(last_50_nodes), desc="path finding...")
for id in last_50_nodes:
    path_result = gds.allShortestPaths.dijkstra.stream(G,sourceNode=id,relationshipWeightProperty="cost")
    path_result = path_result.loc[path_result["index"] != 0]
    path_result['path_weight'] = path_result.apply(lambda row: poi_dict.get(row['targetNode'], 0) / row['totalCost'], axis=1)
    sorted_path_result = path_result.sort_values(by=["path_weight"])
    path_weigth_sum = sorted_path_result["path_weight"].sum()
    user_central_list.append((id,path_weigth_sum))
    df_list.append(sorted_path_result.tail())
    progress_bar.update(1)

progress_bar.close()

user_central_list = sorted(user_central_list, key= lambda x: x[1], reverse=True)

print()
for user in user_central_list[:10]:
    for target in targets:
        if str(target.id) == str(user[0]):
            name = target.name 
    print(f"NAME: {name} ID: {user[0]} path weight sum = {user[1]}")


comb_list = pd.concat(df_list, ignore_index=True)
comb_list_sorted = comb_list.sort_values(by=["path_weight"])

print("Most valuable paths")
print()
print(comb_list_sorted.tail())

gds.graph.drop(gds.graph.get('tmp-graph'))

quit()

for user in targets:
    db_upt.delete_all_users(user)



    













