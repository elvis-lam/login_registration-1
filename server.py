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
    if len(request.form['first-name']) < 2:
        flash("first name must be at least 2 characters", 'f-name')
    if len(request.form['last-name']) < 2:
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
             "first_name": request.form['first-name'],
             "last_name": request.form['last-name'],
             "email": request.form['new-email'],
             "password_hash": pw_hash,
         }
        mysql.query_db(query, data)
        
        # session['user_id'] = request.form
        session['user_name'] = request.form['first_name']
        print('SESSION:', session)
        return redirect('/welcome')
    

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
            print('SESSION:', session)

            # never render on a post, always redirect!
            return redirect('/welcome')
    
    # if username & password don't match
    # --------------------------------------
    else:
        flash("You could not be logged in", 'login')
        return redirect("/")


# ===========================================================================
#                    after registering/logging in
# ===========================================================================
# NEED TO ADD GETTING MESSAGES IN HERE

@app.route('/welcome')
def welcome():
    print('SESSION:', session)
    return render_template('messages.html')


# ===========================================================================
#                       CREATING A MESSAGE
# ===========================================================================

@app.route('/create_message', methods=['POST'])
def create_message():
    mysql = connectToMySQL("registrationsdb")
    # query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(occupation)s, NOW(), NOW());"
    # data = {
    #          'first_name': request.form['first_name'],
    #          'last_name':  request.form['last_name'],
    #          'occupation': request.form['occupation']
    #        }
    # new_friend_id = mysql.query_db(query, data)
    # return redirect('/')

# ===========================================================================
#                       DELETING A MESSAGE
# ===========================================================================






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



