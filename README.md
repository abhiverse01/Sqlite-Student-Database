# Sqlite-Student-Database
# Student records manager using Sqlite3 and Tkinter

In the given application, the database functionalities are implemented using the SQLite database module in Python.


Here's a breakdown of how the database functionalities are implemented:
Database Connection:
The connection to the SQLite database is established using the sqlite3.connect() function,
which takes the name of the database file as a parameter.
In this case, the database file is named 'student_database.db'.
A cursor object is created using the connect.cursor() method.
The cursor is used to execute SQL statements and interact with the database.


Database Table Creation:
The CREATE TABLE IF NOT EXISTS statement is executed using the cursor to create the 'students' table
if it doesn't already exist.
The table has four columns:
'id' (INTEGER, PRIMARY KEY), 'name' (TEXT), 'roll_no' (INTEGER, UNIQUE), and 'other_attributes' (TEXT).
An index is created on the 'name' column using the CREATE INDEX IF NOT EXISTS statement.
This index improves the performance of searching by name.


Retrieving and Displaying Database Records:
The SELECT statement is executed using the cursor to retrieve all the records from the 'students' table.
The retrieved records are displayed in the GUI application by creating
and configuring ttk widgets (labels, buttons, frames) dynamically based on the records.
The records are displayed in a scrollable canvas with a vertical scrollbar.


Adding a New Record:
The 'Add Student' window allows the user to enter the details of a new student record.
When the 'Submit' button is clicked, the INSERT INTO statement is executed
using the cursor to add the new record to the 'students' table.
If the 'roll_no' value already exists in the table (UNIQUE constraint violation), an error message is shown.


Modifying an Existing Record:
The 'Modify Student' window allows the user to modify the details of an existing student record.
The record to be modified is passed to the 'ModifyStudentWindow' frame using the set_record() method.
When the 'Submit' button is clicked, the UPDATE statement is
executed using the cursor to modify the corresponding record in the 'students' table.


Deleting a Record:
Each record displayed in the GUI has a 'Delete' button associated with it.
When the 'Delete' button is clicked, a confirmation dialog is shown to the user.
If the user confirms the deletion, the DELETE FROM statement is executed using the cursor
to remove the corresponding record from the 'students' table.
The record is also removed from the GUI display by destroying the associated widgets.
Overall, the application uses the sqlite3 module to connect to an SQLite database,
execute SQL statements, and perform database operations such as retrieving, adding, modifying, and deleting records.
The retrieved records are displayed in the GUI using tkinter and ttk widgets.
