'''
File Name : main.py
Author : Michael Cates
Date : 2025-06-23
Description :
Learn how to use sqlalchemy, introducing SQL without needing to write SQL code
'''

#imports
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#base class 
Base = declarative_base()

#Person Class inherits from Base
class Person(Base):

    __tablename__ = "People"

    #attributes
    #Column(name_in_db, data_type, primary_key=True/False)
    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, firstname, lastname, gender, age):

        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn}, {self.firstname}, {self.lastname}, {self.gender}, {self.age})"

class Thing(Base):
    __tablename__ = "things"

    t_id = Column("t_id", Integer, primary_key = True)
    description = Column("description", String)
    owner = Column(Integer, ForeignKey("People.ssn"))

    def __init__(self, t_id, description, owner):
        self.t_id = t_id
        self.owner = owner
        self.description = description

    def __repr__(self):
        return f"({self.t_id}) {self.description} owned by {self.owner}"


#Interactions with the database
engine = create_engine("sqlite:///people_db.db", echo=True)#file database
Base.metadata.create_all(bind=engine)

#create a session maker
Session = sessionmaker(bind=engine)#session class
session = Session()#session object

person = Person(123454, "Mike", "Smith", "M", 35)
session.add(person)#add the person to the database
session.commit()#applies the changes to the database

person1 = Person(65432, "Jane", "Doe", "F", 23)
person2 = Person(654654, "Jake", "Austin", "M", 46)
person3 = Person(14581, "Josiah", "King", "M", 22)
person4 = Person(86562, "Louis", "King", "F", 28)

#add the new people to the database
session.add(person1)
session.add(person2)
session.add(person3)
session.add(person4)

session.commit()#commit the changes to the database

'''
#Query to return the people data
results = session.query(Person).filter(Person.firstname.like("%Ja%"))

#iterate through the results
for r in results:
    print(r)
'''

#create Thing objects
t1 = Thing(1, "Car", person2.ssn)
t2 = Thing(2, "Laptop", person1.ssn)
t3 = Thing(3, "Car", person.ssn)
t4 = Thing(4, "House", person2.ssn)
t5 = Thing(5, "Book", person4.ssn)

#add the objects to the database
session.add(t1)
session.add(t2)
session.add(t3)
session.add(t4)
session.add(t5)

#commit the changes to the database
session.commit()

#make a query on both databases
results = session.query(Thing, Person).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Mike")

#print the results
for r in results:
    print(r)



