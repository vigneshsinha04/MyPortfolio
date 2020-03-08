from flask import Flask, render_template, request, redirect
import smtplib
from email.message import EmailMessage
from string import Template
import password_checker, webscraping

app = Flask(__name__)

@app.route('/')
def hello_world():	
	return render_template('index.html')

@app.route('/<string:page>')
def view_page(page):
	return render_template(page+'.html')

@app.route('/contact_me', methods=['POST', 'GET'])
def email_me():
	if request.method == 'POST':
		try:
			email = EmailMessage()
			email["from"] = request.form['Name'] + ' contact'
			email["to"] = "vigneshsinha04@gmail.com"
			email["subject"] = request.form['Subject']

			email.set_content(request.form['Message'] + '\n My Email is ' + request.form['Email'] )

			with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
				smtp.ehlo()
				smtp.starttls()
				smtp.login('thalaveriyan64@gmail.com', 'asumathi')
				smtp.send_message(email)
			return redirect('/thankyou#contact')
		except:
			return render_template('error.html')

@app.route('/check_password', methods=['POST', 'GET'])
def check_password(param = None):
	if request.method == 'POST':
		try:
			passwords = request.form["password"].split()			
			pwd_message_list = password_checker.main(passwords)
			pwd_message = "<br>".join(pwd_message_list)
			return render_template('passwordchecker.html', text=pwd_message)
		except:
			return render_template('error.html')

@app.route('/web_scraping', methods=['POST', 'GET'])
def scrape_web():
	if request.method == 'POST':
		try:
			html_csv = webscraping.view_csv_in_html()
			return render_template('webscraping.html', text=html_csv)
		except Exception as ex:
			raise ex
			return render_template('error.html')