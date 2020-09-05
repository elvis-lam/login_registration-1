from flask import Flask
# from flask import render_template, redirect, request, session, flash, jsonify
from flask_bcrypt import Bcrypt   
# from mysqlconnection import connectToMySQL
# from datetime import datetime
app = Flask(__name__) 

bcrypt = Bcrypt(app)  
app.secret_key = "ThisIsSecret!"
