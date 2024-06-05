#Coding Partners: Israel Lopez + Christopher Jimenez

import psycopg2
connection = psycopg2.connect(database='test_db')

cursor = connection.cursor()

#Functions
    #Create
def createItem(table):
     values = []
     if table == "companies":
        name = input("What is the name of the company?: ")
        state = input("In what state is the company located?: ")
        if name and state:
            print('this works')
            values.extend([name, state])
            cursor.execute(F"INSERT INTO {table} (name, state) VALUES (%s, %s)", values)
            connection.commit()
    
     if table == "people":
        first_name = input("What is the employee name?: ")
        age = int(input("How old is the employee?: "))
        email = input("What is the employee's email?: ")
        employer_id = int(input("What is their employer's id?: "))
        if first_name and age and email and employer_id:
            print('this works')
            values.extend([first_name, age, email, employer_id])
            cursor.execute(F"INSERT INTO {table} (first_name, age, email, employer_id) VALUES (%s, %s, %s, %s)", values)
            connection.commit()

def updateItem(table):
    values = []
    if table == "companies":
        cursor.execute("SELECT * FROM companies")
        print(cursor.fetchall())
        id = input("Select the company to update by id: ")
        name = input("What is the company name: ")
        state = input("What is the state that company is loacted in: ")
        values.extend([name, state, id])
        cursor.execute("UPDATE companies SET name = %s, state = %s WHERE id = %s", values)
        connection.commit()
    
    if table == "people":
        cursor.execute("SELECT * FROM people")
        print(cursor.fetchall())
        id = int(input("Select the employee to update by id: "))
        first_name = input("What is the employee name?: ")
        age = int(input("How old is the employee?: "))
        email = input("What is the employee's email?: ")
        employer_id = int(input("What is their employer's id?: "))
        values.extend([first_name, age, email, employer_id, id])
        cursor.execute("UPDATE people SET first_name = %s, age = %s, email = %s, employer_id = %s WHERE id = %s", values)
        connection.commit()

def deleteItem(table):
    values = []
    if table == "companies":
        cursor.execute("SELECT * FROM companies")
        print(cursor.fetchall())
        id = input("Select the company to delete by id: ")
        values.extend([id])
        cursor.execute("DELETE FROM companies WHERE id = %s", values)
        connection.commit()
    
    if table == "people":
        cursor.execute("SELECT * FROM people")
        print(cursor.fetchall())
        id = input("Select the employee to delete by id: ")
        values.extend([id])
        cursor.execute("DELETE FROM people WHERE id = %s", values)
        connection.commit()

            
#Start App
def startTool():
        print("Welcome to your Customer Relationship Management Tool")
        while True:
            answer1 = input("What would you like to access?: 1.Companies Table 2.People Table 3.Exit - ")
            if int(answer1) == 3:
                print("Exiting...")
                break                   
            answer2 = input("What would you like to do?: 1.View 2.Create 3.Update 4.Delete 5.View Relational Table 6.Exit - ")
            if int(answer1) and int(answer2) == 6:
                print("Exiting...")
                break
            if int(answer1) == 1 and int(answer2) == 1:
                cursor.execute("SELECT * FROM companies")
                print(cursor.fetchall())
            if int(answer1) == 2 and int(answer2) == 1:
                cursor.execute("SELECT * FROM people")
                print(cursor.fetchall())
            if int(answer1) == 1 and int(answer2) == 2:
                createItem("companies")
            if int(answer1) == 2 and int(answer2) == 2:
                createItem("people")
            if int(answer1) == 1 and int(answer2) == 3:
                updateItem("companies")
            if int(answer1) == 2 and int(answer2) == 3:
                updateItem("people")
            if int(answer1) == 1 and int(answer2) == 4:
                deleteItem("companies")
            if int(answer1) == 2 and int(answer2) == 4:
                deleteItem("people")           
            if int(answer1) and int(answer2) == 5:
                cursor.execute("SELECT * FROM people FULL OUTER JOIN companies ON people.employer_id = companies.id")
                print(cursor.fetchall())
            
startTool()

# People Table
# cursor.execute("SELECT * FROM people")
# print(cursor.fetchall())
# # Companies Table
# cursor.execute("SELECT * FROM companies")
# print(cursor.fetchall())

# cursor.execute("INSERT INTO people (first_name, age, email, employer_id) VALUES (%s, %s, %s, %s)", ['joe', 25, 'joe5@gmail.com', 2])

# cursor.execute("INSERT INTO companies (name, state) VALUES (%s, %s)", ['Google', 'IL'])

# cursor.execute("UPDATE people SET first_name = %s, age = %s, email = %s, employer_id = %s WHERE id = %s", ['steve', 23, 'seteve@gmail.com', 2, 12])

# cursor.execute("UPDATE companies SET name = %s, state = %s WHERE id = %s", ['Salesforce', 'VA', 2])

# cursor.execute("DELETE FROM people WHERE id = %s", [20])

# cursor.execute("DELETE FROM companies WHERE id = %s", [5])

#Relate Employees with Companies
# cursor.execute("SELECT * FROM people FULL OUTER JOIN companies ON people.employer_id = companies.id")
# print(cursor.fetchall())

cursor.close()
connection.close()

