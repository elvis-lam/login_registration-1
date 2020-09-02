# login_registration
------------------------------------------------------------

## App's Purpose:
-Using multiple validations to create new user registration, and returning user login functionality

-Flash specific error messages depending on which input field is incorrect

-Send messages to other users in database

-Read/Delete messages that are sent from other users

============================================================

## Technologies Utilized:
-HTML
-Bootstrap CSS
-Python
-MySQL
-Flask
-Session
-Flash
-Bcrypt

=============================================================

## Developer Techniques:
-Validation requirements for all user inputs
-Connecting to the database to check email existence
-Using Bcrypt to hash passwords for user safety

-Using database to dynamically create/read/update/delete http responses
-Less database interaction by using SQL queries that are specific yet also reducing repitition

=============================================================


 ### Screenshots of the app's functions:

--------------------------------------------------------------

Database with empty users table & messages table:
![initial users table](/static/usersTable1.jpg)
![initial messages table](/static/messagesTable1.jpg)

--------------------------------------------------------------

Index.html, registering a new user to the database
![index.html](/static/index1.jpg)
![registering](/static/index2.jpg)

--------------------------------------------------------------

First user in the database, messages page (no other users to send/receieve messages)
![first user view](/static/index3.jpg)
--------------------------------------------------------------

Other registered users added to database
![multiple users in database](/static/index4.jpg)
--------------------------------------------------------------

Receiving messages and the ability to send messages
![send/receive messages based on database](/static/index5.jpg)
--------------------------------------------------------------

