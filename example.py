import psycopg2
connection = psycopg2.connect(database='test_db')

cursor = connection.cursor()

cursor.execute("SELECT * FROM people")
print(cursor.fetchall()) 

# We can protect our program from SQL injenction by using the "%s" parameter then ending the string and adding a second argument as a List with the values where the placeholder symbol/parameter "%s" is --> NOTE: We can have as many placeholder symbols/parameters, but we need to keep track of them and include them in the List in the order in which they will appear in the string
# cursor.execute("SELECT * FROM people WHERE id = %s", [3])

# We can limit our fetch to one item with the fetchone() method, but we can also do it within the SQL command
# print(cursor.fetchone())

# cursor.execute("INSERT INTO people (first_name, age, email, employer_id) VALUES (%s, %s, %s, %s)", ['Django', 15, 'django@gmail.com', 1])
# connection.commit()

# cursor.execute('DELETE FROM people WHERE id = %s', [6])
# connection.commit()

# cursor.execute('UPDATE people SET first_name = %s, age = %s WHERE id = %s', ['Spongebob', 12, 5])
# connection.commit()

cursor.close()
connection.close()
