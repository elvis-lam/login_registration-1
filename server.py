# from flask import render_template, redirect, request, session, flash, jsonify
# from flask_bcrypt import Bcrypt   
# # from mysqlconnection import connectToMySQL
# from datetime import datetime

# importing from module 
from login_registration import app, bcrypt
from login_registration.config import routes

# import re   # "re"regular expression operations
# import pymysql
# import pymysql.cursors #makes data sent as python dictionaries

# mysql = connectToMySQL('registrationsdb')

# # used for email validation
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# app = Flask(__name__) 
# bcrypt = Bcrypt(app)  
# app.secret_key = "ThisIsSecret!"

# # ==============================================================
# #                     INDEX ROUTE
# # ==============================================================
# @app.route('/')
# def index():
#     mysql = connectToMySQL('registrationsdb')
#     return render_template('index.html')

# # ==============================================================
# #                  REGISTER BUTTON ROUTE
# # ==============================================================
# @app.route('/register', methods=['POST'])
# def register():

#     # name validation
#     # --------------------------------------
#     if len(request.form['first_name']) < 2:
#         flash("first name must be at least 2 characters", 'f-name')
#     if len(request.form['last_name']) < 2:
#         flash("last name must be at least 2 characters", 'l-name')
    
#     # new-email validation
#     # --------------------------------------
#     if not EMAIL_REGEX.match(request.form['new-email']):
#         flash("Invalid Email Address!", 'new-email')

#     # checking if email already exists in db
#     # --------------------------------------
#     mysql = connectToMySQL('registrationsdb')
#     query = "SELECT * FROM users WHERE email = %(email)s;"
#     data = { "email" : request.form['new-email']}
#     matchingEmail = mysql.query_db(query, data)

#     if matchingEmail:
#         flash("Email already exists", 'new-email')
    
#     # new-password validation
#     # --------------------------------------
#     if len(request.form['new-password']) < 8:
#         flash("password must be at least 8 characters", 'new-password')
    
#     # confirm-password validation
#     # --------------------------------------
#     if request.form['new-password'] != request.form['confirm-password']:
#         flash("passwords don't match", 'confirm-password')
    
#     # initiate any flash messages on index.html
#     # --------------------------------------
#     if '_flashes' in session.keys():
#         return redirect("/")

#     # ADD NEW USER TO DATABASE : hash password
#     # --------------------------------------
#     else:
#         mysql = connectToMySQL('registrationsdb')
#         pw_hash = bcrypt.generate_password_hash(request.form['new-password']) 

#         query = "INSERT INTO users (first_name, last_name, email, password_hash, user_level, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, '1', NOW(), NOW());"
#         data = {
#              "first_name": request.form['first_name'],
#              "last_name": request.form['last_name'],
#              "email": request.form['new-email'],
#              "password_hash": pw_hash,
#          }
#         new_user_id=mysql.query_db(query, data)

#         # get user_id and store into session
#         session['user_id'] = new_user_id
#         session['user_name'] = request.form['first_name']
#         session['new_user'] = True
#         print('SESSION:', session)
#         flash("Aww yeah, you successfully registered.  You can now log in using the same information you provided!", 'success')

#         return redirect('/')
    

# # ========================================================
# #                  LOGIN BUTTON ROUTE
# # ========================================================
# @app.route('/login', methods=['POST'])
# def login():
    
#     # check if email exists in database
#     # --------------------------------------
#     mysql = connectToMySQL('registrationsdb')
#     query = "SELECT * FROM users WHERE email = %(email)s;"
#     data = { "email" : request.form['login-email'] }
#     result = mysql.query_db(query, data)
#     if result:
#         if bcrypt.check_password_hash(result[0]['password_hash'], request.form['password']):
            
#             # if True: store some user data in session
#             session['user_id'] = result[0]['id']
#             session['user_name'] = result[0]['first_name']
#             session['user_level'] = result[0]['user_level']

#             print("**************USER LEVEL", session['user_level'])

#             # based on user_level, redirect to admin or user
#             if session['user_level'] == '9':
#                 return redirect('/admin')
            
#             else: 
#                 return redirect('/user')
    
#         # if username & password don't match
#         # --------------------------------------
#         else:
#             flash("You could not be logged in", 'login')
#             return redirect("/")


# # =======================================================
# #                   IF ADMIN:
# # =======================================================
# @app.route('/admin')
# def admin():
#     user_id = session['user_id']

#     # data: users 
#     # -------------------------------------------
#     mysql = connectToMySQL('registrationsdb')
#     query = "SELECT id, first_name, last_name, email, user_level FROM users WHERE NOT (id = %(user_id)s);"
#     data = {
#         'user_id': user_id
#     }
#     users = mysql.query_db(query, data)

#     return render_template('admin.html', users = users)


# # =======================================================
# #                   DELETE USER:
# # =======================================================
# @app.route('/deleteUser', methods=['POST'])
# def deleteUser():

#     # getting id from hidden input
#     print(request.form['deleteID'])

#     mysql = connectToMySQL('registrationsdb')
#     query = "DELETE FROM users WHERE (id = %(deleteID)s);"
#     data = {
#         'deleteID': request.form['deleteID']
#     }
#     result = mysql.query_db(query, data)

#     return redirect('/admin')


# # =======================================================
# #       ADMIN ACCESS ROUTE: change user_level in db
# # =======================================================
# @app.route('/adminAccess', methods=['POST'])
# def adminAccess():

#     # if user is already level=1, update it to '9'
#     if request.form['user_level'] == '1':
#         user_level = 9
#     else:
#         user_level = 1

#     mysql = connectToMySQL('registrationsdb')
#     query = "UPDATE users SET user_level = '%(user_level)s' WHERE id = %(id)s;"
#     data = {
#         'user_level': user_level,
#         'id': request.form['accessID']
#     }
#     results = mysql.query_db(query, data)

#     return redirect('/admin')

# # =======================================================
# #                   IF USER:
# # =======================================================
# @app.route('/user')
# def user():
#     return render_template('user.html')


# # =======================================================
# #            GET DATA: after registering/logging in
# # =======================================================
# @app.route('/getData', methods=['GET'])
# def getData():
#     user_id = session['user_id']
#     user_level = session['user_level']
#     print('*****SESSION', session)
#     print('*****USER_ID', user_id)

#     # data of other users for "send a message"
#     # -------------------------------------------
#     mysql = connectToMySQL('registrationsdb')
#     query = "SELECT id, first_name FROM users WHERE NOT (id = %(user_id)s);"
#     data = {
#         'user_id': user_id
#     }
#     otherUsers = mysql.query_db(query, data)

#     # data to show "received messages", newest first, 5 max
#     # -------------------------------------------
#     mysql = connectToMySQL('registrationsdb')
#     message_query = "SELECT user_id, first_name, content, messages.created_at, messages.id FROM messages, users WHERE (receiver_id = %(user_id)s) and user_id = users.id ORDER BY messages.id DESC LIMIT 5;"
#     message_data = {
#         'user_id': user_id
#     }
#     receivedMessages = mysql.query_db(message_query, message_data)

#     # COUNT sent messages 
#     # -------------------------------------------
#     mysql = connectToMySQL('registrationsdb')
#     query = "SELECT COUNT(user_id) FROM registrationsdb.messages WHERE user_id = %(user_id)s;"
#     data = { 'user_id': user_id }
#     count_sent_messages = mysql.query_db(query, data)

#     count_sent = count_sent_messages[0]['COUNT(user_id)']
#     print('******** COUNT SENT MESSAGES:', count_sent)

#     # COUNT received messages 
#     # -------------------------------------------
#     mysql = connectToMySQL('registrationsdb')
#     query = "SELECT COUNT(receiver_id) FROM registrationsdb.messages WHERE receiver_id = %(receiver_id)s;"
#     data = { 'receiver_id': user_id }
#     count_received_messages = mysql.query_db(query, data)
 
#     count_received = count_received_messages[0]['COUNT(receiver_id)']
#     print('******** COUNT RECEIVED MESSAGES:', count_received)

#     #SEND ALL OF THIS DATA TO BE MANIPULATED ON HTML
#     return render_template('messages.html', otherUsers = otherUsers, receivedMessages = receivedMessages, count_sent = count_sent, count_received = count_received)


# # =====================================================
# #                 CREATE A MESSAGE
# # =====================================================
# @app.route('/create_message', methods=['POST'])
# def create_message():
    
#     mysql = connectToMySQL("registrationsdb")
#     query= "INSERT INTO messages (user_id, receiver_id, content, created_at, updated_at) VALUES (%(user_id)s, %(receiver_id)s, %(content)s, NOW(), NOW());"
#     data = {
#         'user_id': session['user_id'],
#         'receiver_id': request.form['receiverId'],
#         'content': request.form['sendMsg']
#         }
#     mysql.query_db(query, data)

#     return redirect('/getData')


# # =====================================================
# #                 DELETE A MESSAGE
# # =====================================================
# @app.route('/delete_message', methods=['POST'])
# def delete_message():

#     mysql = connectToMySQL("registrationsdb")
#     query = "DELETE FROM messages WHERE (id = %(messagesId)s);"
#     data = {
#         'messagesId': request.form['messagesId']
#     }
#     mysql.query_db(query, data)

#     return redirect('/getData')


# # ====================================================
# #        LOG OUT: clear session
# # ====================================================
# @app.route('/logout', methods=['POST'])
# def logout():
#     return redirect('/clear_session')
# # ----------------------------------------
# @app.route('/clear_session')
# def clear_session():
#     session.clear()
#     return redirect('/')


# =======================================================
#         START SERVER **********
# =======================================================
if __name__ == "__main__":
    app.run(debug=True)



