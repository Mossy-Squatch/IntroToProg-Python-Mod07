# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using functions, classes, objects and
# structured error handling
# Change Log:
#   Chuck Epperson,02/23/2024,Created Script
#
# ------------------------------------------------------------------------------------------ #
import json
from sys import exit

# Define the Data Constants
MENU: str = """
------ Course Registration Program ------
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
"""

FILE_NAME: str = "Enrollments.json"


# Define the Data Variables and constants

menu_choice: str ="" # Hold the choice made by the user.
students: list = []  # A table of student data

#Define class Student
class Person:

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
    
    @property
    def first_name(self):
        return self.__first_name.title()
    
    @first_name.setter
    def first_name(self, value:str):
        if value.isalpha() or value =="":
            self.__first_name = value
        else:
            raise ValueError("First name should only contain letters!")
    
    @property
    def last_name(self):
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value:str):
        if value.isalpha() or value =="":
            self.__last_name = value
        else:
            raise ValueError("The last name should only contain letters!")        

# Define class Student, with inheritance from Person
class Student(Person):

    def __init__(self, first_name: str, last_name: str, course_name: str = ""):
        super().__init__(first_name, last_name)
        self.course_name = course_name
    
    @property
    def course_name(self):
        return self.__course_name
    
    @course_name.setter
    def course_name(self, value: str):
        if value != "":
            self.__course_name = value
        else:
            raise ValueError("The course name cannot be left blank!")

# File processing - Define class FileProcessor
class FileProcessor:
    # Function for reading data from file
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        try:
            with open(file_name, "r") as file:
                student_data = json.load(file)
        except FileNotFoundError as e:
            IO.output_error_messages("File does not exist!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if file.closed == False:
                file.close()
        return student_data
    
    # Function for writing user input data to file
    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        try:
            with open(file_name, "w") as file:
                json.dump(student_data, file)
            print("-" * 50)
            print("INFO: All rows saved to file!")
            print("-" * 50)
        except TypeError as e:
            IO.output_error_messages("Data is not in valid JSON format!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if file.closed == False:
                file.close()


# User input and output - Define class IO
class IO:
    # Function for displaying error messages
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message --")
            print(error, error.__doc__, type(error), sep="\n")
    
    # Function for displaying the menu options to the user
    @staticmethod
    def output_menu(menu: str):
        print()
        print(menu)
        print()
    
    # Function for prompting user menu selection and storing choice
    @staticmethod
    def input_menu_choice():
        choice = "0"
        try:
            choice = input("Select a menu option (1-4): ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Invalid selection!\nYou must select (1-4)!")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice
    
    # Function for displaying current data to user
    @staticmethod
    def output_student_courses(student_data: list):
        print()
        print("The current data is: ")
        for student in student_data:
            student_first_name = student["FirstName"]
            student_last_name = student["LastName"]
            course_name = student["CourseName"]
            print(f"{student_first_name},{student_last_name},{course_name}")
                
    # Function for user to enter student data
    @staticmethod
    def input_student_data(student_data: list):
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The student's first name should only contain letters!")
            
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The student's last name should only contain letters!")
            
            course_name = input("Please enter the name of the course: ")

            student = {"FirstName": student_first_name,
                       "LastName": student_last_name,
                       "CourseName": course_name}
            student_data.append(student)
            print()
            print(f"You have registered {student["FirstName"]} {student["LastName"]} for {student["CourseName"]}!")
            print()
        except ValueError as e:
            IO.output_error_messages("Value entered was not the correct type of data!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return student_data

# Start of main body - read data from JSON file.
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)


# Present and Process the data
if __name__ == "__main__":
    while (True):
        IO.output_menu(menu=MENU)
        menu_choice = IO.input_menu_choice()
        match menu_choice:
            # Case 1 enter new student data
            case "1":
                student = IO.input_student_data(student_data=students)
            # Case 2 show current data
            case "2":
                IO.output_student_courses(student_data=students)
            # Case 3 save data
            case "3":
                FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
            # Case 4 exit program
            case "4":
                print("Exiting the program")
                exit()
# End