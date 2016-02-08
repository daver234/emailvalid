from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)

app.secret_key = 'ThisIsSecret' # you need to set a secret key for security purposes
# routing rules and rest of server.py below

mysql = MySQLConnector('friendsdb')

@app.route('/')
def index():
    # friends = mysql.fetch("SELECT * FROM friends")
    # print friends
    return render_template('index.html')

    
@app.route('/friends', methods=['POST'])
def create():
	#friends = mysql.fetch("SELECT * FROM friends")
	
	first = request.form['first_name']
	print "First name entered:",first
	firstnames = mysql.fetch("SELECT first_name FROM friends")
	#print "The first names are:",firstnames
	print(firstnames[0]['first_name'])


	success = 0
	namekey = ""

	for idx in range(0,len(firstnames)):
		print "this is idx:",idx
		print 'first name checking...',(firstnames[idx]['first_name'])
	 	if (firstnames[idx]['first_name']) == first:
	 		namekey = (firstnames[idx]['first_name'])
	 		success = 1

	if success == 0:
		flash("You are not in the database")
		print "value of success is:",success
	 	return redirect('/show')

	print "value of success after match:",success
	print "The namekey is:",namekey
	print "The idx is: ",idx 		

	# 		if 
	# temp = 1
	# for test in firstnames:
	# 	print "this is test:",test['first_name']
	# 	print "length of test",len(firstnames)
	# 	if test['first_name'] != first:
	# 		temp = 0

	# if temp == 0:
	# 	flash("You are not in the database")
	# 	return redirect('/show')


	email = request.form['email']
	if not re.match(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$',email):
		flash("You did not enter a valid email address")
		return redirect('/show')
	query = "INSERT INTO friends (email, updated_at) VALUES ('{}', NOW())".format(request.form['email'])
	print query

	mysql.run_mysql_query(query)
	return redirect('/success')


@app.route('/show')
def showing():
	return redirect('/') 

@app.route('/success')
def success_stuff():

	return render_template('success.html')
app.run(debug=True)
