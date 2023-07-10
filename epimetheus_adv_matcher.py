from neo4j import GraphDatabase
import weighter
import weighter_keywords


URI = "neo4j://localhost"
AUTH = ("neo4j", "password")
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

class SchoolLinker:
    def __init__(self):
        pass




def school_match_finder(students:list):
    keyword_match_dictionary = {key: [] for key in weighter_keywords.education_keyword_ratings}
    

    for student in students:
        try:
            keyword_match_dictionary[student.education_keyword].append(student)
        except KeyError:
            pass


    #create dynamic study year dictionary

    
    study_class = {key: [] for key in range(len(students))}
    
   


    for student_a in students:
            study_class[student_a]=[]
            
            for student_b in students:
                if student_b.name == student_a.name:
                    pass
                else:
                    a_education_year = student_a.education_year
                    b_education_year = student_b.education_year
                    
                    if a_education_year == [0]:
                        pass
                    else:

                        try:
                            if (max(b_education_year)<=max(a_education_year) and max(b_education_year)>=min(a_education_year)) or min(b_education_year)>=min(a_education_year) and min(b_education_year)<=max(a_education_year):
                                study_class[student_a].append(student_b)
                                #student_b.asigned_to_study_class=True
                        except:
                            pass
            

    for key in study_class:
        same_time = study_class[key]
        
        if len(same_time)>1 and key.unlinked_from_school==True:
            for person in same_time:
                if key.education_keyword == person.education_keyword:
                    
                    records, summary, keys = driver.execute_query("""
                    MATCH (p:TMP {name: $name}),(f:TMP {name: $friend})
                    MERGE (p)-[:studied_same_school_time_same_place {weight: 1, cost:1}]->(f)
                    """, name=key.name, friend=person.name,
                    database_="neo4j",
                    )
                else:
                    #print(f"{key.name} linked!")
                    records, summary, keys = driver.execute_query("""
                    MATCH (p:TMP {name: $name}),(f:TMP {name: $friend})
                    MERGE (p)-[:studied_school_same_time {weight: 0.75, cost:1/0.75}]->(f)
                    """, name=key.name, friend=person.name,
                    database_="neo4j",
                    )
                key.unlinked_from_school=False                


    for student_a in students:
        for student_b in students:
            if student_b.name == student_a.name or student_a.unlinked_from_school==False:
                    pass
            else:
                #print(f"{student_a.name} linked!")
                records, summary, keys = driver.execute_query("""
                    MATCH (p:TMP {name: $name}),(f:TMP {name: $friend})
                    MERGE (p)-[:studied_same_school {weight: 0.25, cost: 1/0.25}]->(f)
                    """, name=student_a.name, friend=student_b.name,
                    database_="neo4j",
                    )
        

                

def company_match_finder(workers:list):
    keyword_match_dictionary = {key: [] for key in weighter_keywords.department_keywords}
    

    for student in workers:
        try:
            keyword_match_dictionary[student.department].append(student)
        except KeyError:
            pass


    #create dynamic study year dictionary

    
    company_class = {key: [] for key in range(len(workers))}          


    for worker_a in workers:
        for worker_b in workers:
            if worker_b.name == worker_a.name or worker_a.unlinked_from_school==False:
                    pass
            else:
                #print(f"{worker_a.name} linked!")
                records, summary, keys = driver.execute_query("""
                    MATCH (p:TMP {name: $name}),(f:TMP {name: $friend})
                    MERGE (p)-[:worked_same_company {weight: 0.25, cost: 1/0.25}]->(f)
                    """, name=worker_a.name, friend=worker_b.name,
                    database_="neo4j",
                    )
        



def school_buddies():
    print("find all school nodes")
    schools, summary, keys = driver.execute_query(
    "MATCH (p:School) RETURN p.name AS name",
    database_="neo4j",
    )
    # Summary information
    print("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(schools),
            time=summary.result_available_after))
    print("find all persons connected to the school")
    for raw_school in schools:
       
        school = raw_school.value()
        record, summary, keys = driver.execute_query(
        "MATCH p=(n:TMP)-[r:studied_in]->(:School {name: $name}) RETURN n",
        database_="neo4j", name=school
        )
        #check if more then 1 connection
        if len(record)==1:
            pass
        else:
            #print(school)
            students = []
            for person in record:
                data = person.data()
                try:
                    interests = data["n"]["interests"]
                except:
                    interests = []
                data_list=[data["n"]["name"],data["n"]["link"],data["n"]["intro"],data["n"]["location"],data["n"]["about"],data["n"]["skills"],data["n"]["experiences"],data["n"]["accomplishments"],data["n"]["education"],data["n"]["connections"],interests]
                
                person_obj=weighter.Target(data_list)
                weighter.CompanyDepartments.department_finder(person_obj)
                weighter.StatusWeighter.status_finder(person_obj)
                weighter.EducationWeigter.education_finder(person_obj)
                students.append(person_obj)

            school_match_finder(students)   
                

def company_buddies():
    #find all school nodes
    companies, summary, keys = driver.execute_query(
    "MATCH (p:Company) RETURN p.name AS name",
    database_="neo4j",
    )
    # Summary information
    print("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(companies),
            time=summary.result_available_after))
    
    

    for raw_company in companies:

        #find all persons connected to the school        
        company = raw_company.value()
        record, summary, keys = driver.execute_query(
        "MATCH p=(n:TMP)-[r:Worked_at]->(:Company {name: $name}) RETURN n",
        database_="neo4j", name=company
        )
        
        #check if more then 1 connection
        if len(record)==1:
            pass
        else:
            #print(company)
            
            workers = []
            for person in record:
                data = person.data()
                try:
                    interests = data["n"]["interests"]
                except:
                    interests = []
                data_list=[data["n"]["name"],data["n"]["link"],data["n"]["intro"],data["n"]["location"],data["n"]["about"],data["n"]["skills"],data["n"]["experiences"],data["n"]["accomplishments"],data["n"]["education"],data["n"]["connections"],interests]
                
                person_obj=weighter.Target(data_list)
                weighter.CompanyDepartments.department_finder(person_obj)
                weighter.StatusWeighter.status_finder(person_obj)
                weighter.EducationWeigter.education_finder(person_obj)
                workers.append(person_obj)
                
            company_match_finder(workers)   

def interest_buddies():
    pass

#interest buddies

#colleagues

#superior matcher

#

        
if __name__ == "__main__":
    school_buddies()
    #company_buddies()