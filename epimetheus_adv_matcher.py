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


    for subject_key in keyword_match_dictionary:
        target_list = keyword_match_dictionary[subject_key]
        if len(target_list)>1:
            print((subject_key,[person.name for person in target_list]))
    

    #create dynamic study year dictionary

    print("linkin nodes based on school history")
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
        target_list = study_class[key]
        if len(target_list)>1:
            for person in target_list:
                if key.education_keyword == person.education_keyword:
                    
                    records, summary, keys = driver.execute_query("""
                    MATCH (p:Person {name: $name}),(f:Person {name: $friend})
                    MERGE (p)-[:studied_same_time_and_same_place {weight: 1.0}]->(f)
                    """, name=key.name, friend=person.name,
                    database_="neo4j",
                    )
                else:
                    records, summary, keys = driver.execute_query("""
                    MATCH (p:Person {name: $name}),(f:Person {name: $friend})
                    MERGE (p)-[:studied_same_time {weight: 0.5}]->(f)
                    """, name=key.name, friend=person.name,
                    database_="neo4j",
                    )
                

def company_match_finder(student:list):
    pass

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

    for raw_school in schools:

        print("find all persons connected to the school")       
        school = raw_school.value()
        record, summary, keys = driver.execute_query(
        "MATCH p=(n:Person)-[r:studied_in]->(:School {name: $name}) RETURN n",
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
        "MATCH p=(n:Person)-[r:studied_in]->(:School {name: $name}) RETURN n",
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



        
if __name__ == "__main__":
    school_buddies()