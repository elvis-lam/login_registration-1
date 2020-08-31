from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_bcrypt import Bcrypt   
from mysqlconnection import connectToMySQL
from datetime import datetime

# the "re" module will let us perform some regular expression operations
import re
import pymysql
import pymysql.cursors #makes data sent in the form of python dictionaries

mysql = connectToMySQL('registrationsdb')

# used for email validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__) 
bcrypt = Bcrypt(app)  
app.secret_key = "ThisIsSecret!"

# ===========================================================================
#                               INDEX ROUTE
# ===========================================================================
@app.route('/')
def index():
    mysql = connectToMySQL('registrationsdb')
    return render_template('index.html')

# ===========================================================================
#                           REGISTER BUTTON ROUTE
# ===========================================================================
@app.route('/register', methods=['POST'])
def register():

    # name validation
    # --------------------------------------
    if len(request.form['first_name']) < 2:
        flash("first name must be at least 2 characters", 'f-name')
    if len(request.form['last_name']) < 2:
        flash("last name must be at least 2 characters", 'l-name')
    
    # new-email validation
    # --------------------------------------
    if not EMAIL_REGEX.match(request.form['new-email']):
        flash("Invalid Email Address!", 'new-email')

    # checking if email already exists in db
    # --------------------------------------
    mysql = connectToMySQL('registrationsdb')
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form['new-email']}
    matchingEmail = mysql.query_db(query, data)

    if matchingEmail:
        flash("Email already exists", 'new-email')
    
    # new-password validation
    # --------------------------------------
    if len(request.form['new-password']) < 8:
        flash("password must be at least 8 characters", 'new-password')
    
    # confirm-password validation
    # --------------------------------------
    if request.form['new-password'] != request.form['confirm-password']:
        flash("passwords don't match", 'confirm-password')
    
    # initiate any flash messages on index.html
    # --------------------------------------
    if '_flashes' in session.keys():
        return redirect("/")

    # ADD NEW USER TO DATABASE
    # --------------------------------------
    else:
        mysql = connectToMySQL('registrationsdb')
        pw_hash = bcrypt.generate_password_hash(request.form['new-password']) 
        print("PW HASH:", pw_hash)
        query = "INSERT INTO users (first_name, last_name, email, password_hash, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, NOW(), NOW());"
        data = {
             "first_name": request.form['first_name'],
             "last_name": request.form['last_name'],
             "email": request.form['new-email'],
             "password_hash": pw_hash,
         }
        mysql.query_db(query, data)

# get user_id and store into session
        # session['user_id'] = request.form
        session['user_name'] = request.form['first_name']
        print('SESSION:', session)
        return redirect('/getData')
    

# ===========================================================================
#                              LOGIN BUTTON ROUTE
# ===========================================================================
@app.route('/login', methods=['POST'])
def login():
    
    # check if email exists in database
    # --------------------------------------
    mysql = connectToMySQL('registrationsdb')
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = { "email" : request.form['login-email'] }
    result = mysql.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['password_hash'], request.form['password']):
            
            # if we get True after checking the password, we may put the user id in session
            session['user_id'] = result[0]['id']
            session['user_name'] = result[0]['first_name']

            # never render on a post, always redirect!
            return redirect('/getData')
    
    # if username & password don't match
    # --------------------------------------
    else:
        flash("You could not be logged in", 'login')
        return redirect("/")


# ===========================================================================
#                    after registering/logging in
# ===========================================================================
# NEED TO ADD GETTING MESSAGES IN HERE

@app.route('/getData', methods=['GET'])
def getData():

    user_id= session['user_id']

    print('*****SESSION', session)
    print('*****USER_ID', user_id)
 
    mysql = connectToMySQL('registrationsdb')
    query = "SELECT id, first_name FROM users WHERE NOT (id = %(user_id)s);"
    data = {
        'user_id': user_id
    }

    # will render names and their id (hidden) to send messages
    # saved to, otherUsers 
    all_other_users = mysql.query_db(query, data)
    print('OTHER USERS:', all_other_users)
    
    # return  jsonify(all_clients)

    
   

    # # COUNT sent messages 
    # # -------------------------------------------
    # mysql = connectToMySQL("registrationsdb")
    # query = "SELECT COUNT(user_id) FROM registrationsdb.messages WHERE user_id = %(user_id)s;"
    # data = { 'user_id': session['user_id'] }
    # count_sent_messages = mysql.query_db(query, data)

    # session['count_sent'] = count_sent_messages
    # print('******** COUNT SENT MESSAGES:', count_sent_messages)

    # # COUNT received messages 
    # # -------------------------------------------
    # mysql = connectToMySQL("registrationsdb")
    # query = "SELECT COUNT(receiver_id) FROM registrationsdb.messages WHERE receiver_id = %(user_id)s;"
    # data = { 'receiver_id': session['user_id'] }
    # count_received_messages = mysql.query_db(query, data)

    # print('******** COUNT RECEIVED MESSAGES:', count_received_messages)

    # # DISPLAY RECENT 5 RECEIVED MESSAGES
    # # -------------------------------------------
    # mysql = connectToMySQL("registrationsdb")
    # query = "SELECT * FROM registrationsdb.messages WHERE receiver_id = %(user_id)s ORDER BY id DESC LIMIT 2;"
    # data = { 'receiver_id': session['user_id'] }
    # received_messages = mysql.query_db(query, data)

    # return render_template('messages.html', count_sent_messages = count_sent_messages, count_received_messages = count_received_messages, received_messages = received_messages )

    return render_template('messages.html', otherUsers = all_other_users)

# need to use: if received_messages, then return. else don't return the messages
    # return render_template('messages.html', received_messages = received_messages)

    #messages.html
    #  {{ received_messages[0].created_at }}
    #  {{ received_messages[0].content }}



# ===========================================================================
#                       CREATING A MESSAGE
# ===========================================================================

@app.route('/create_message', methods=['POST'])
def create_message():
    mysql = connectToMySQL("registrationsdb")
    query= "INSERT INTO messages (user_id, receiver_id, content, created_at, updated_at) VALUES (%(user_id)s, %(receiver_id)s, %(content)s, NOW(), NOW());"
    data = {
        'user_id': session['user_id'],
#MAKE RECEIVER_ID DYNAMIC
        'receiver_id': 2,
        'content': request.form['sendMsg']
        }
    mysql.query_db(query, data)

    print('***************CREATED A MESSAGE')
    return redirect('/welcome')





# ===========================================================================
#                       DELETING A MESSAGE
# ===========================================================================


# @app.route('/delete_message', methods=['POST'])
# def create_message():
#     mysql = connectToMySQL("registrationsdb")




# # ===========================================================================
# #         CLEAR OUT SESSION WHEN LOG OUT 
# # ===========================================================================
# @app.route('/reset', methods=['POST'])
# def resetButton():
#     return redirect('/destroy_session')
# # =======================================
# @app.route('/destroy_session')
# def destroySession():
#     session.clear()
#     return redirect('/')


# ===========================================================================
#         START SERVER
# ===========================================================================
if __name__ == "__main__":
    app.run(debug=True)



