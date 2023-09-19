# from flask import Blueprint, render_template, request, flash, url_for, redirect
import flask
from tkinter import ttk

from flask_login import login_required, current_user
from model import *

from website import DB
from base64 import b64encode
import json
import requests
import os.path

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

views = flask.Blueprint('views', __name__)

selected_form = "1nUun2se8Lt_2o-yKAiJHrQkfu-GTpTzMoa8Ees7lVR0"
SCOPES = [
	"https://www.googleapis.com/auth/forms.body",
	"openid",
	"https://www.googleapis.com/auth/userinfo.email",
	"https://www.googleapis.com/auth/userinfo.profile",
	"https://www.googleapis.com/auth/drive",
	"https://www.googleapis.com/auth/drive.file",
	"https://www.googleapis.com/auth/drive.readonly",
	"https://www.googleapis.com/auth/forms.body.readonly",
	"https://www.googleapis.com/auth/drive.file",
	"https://www.googleapis.com/auth/contacts.readonly",
	"https://www.googleapis.com/auth/admin.directory.user"
		
	]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
store = file.Storage('token.json')

creds = None
credentials = None
my_forms = []
my_docs = []
my_sheets = []
my_drive = []
my_people = []
drive = None
people = None

@views.route("/get-users")
def grabUsers():
	getUserList()
	return json.dumps(my_people)

@views.route("/get-sheets")
def grabSheets():
	getSheets()
	return json.dumps(my_sheets)

@views.route("/get-drive")
def grabDrive():
	getFiles()
	return json.dumps(my_drive)

@views.route("/get-forms")
def grabForms():
	getForms()
	return json.dumps(my_forms)

@views.route("/get-docs")
def grabDocs():
	while len(my_docs) < 1:
		getDocs()
	return json.dumps(my_docs)

@views.route('/my-docs/<kind>/<id>/<title>')
def showDoc(id, kind, title):
	kind_r = kind
	if kind == "docs":
		kind_r = "document"
	elif kind == "sheets":
		kind_r = "spreadsheets"
	elif kind == "forms":
		kind_r = "forms"

	return flask.render_template("pages/doc_viewer.html", doc=id, title=title, kind=kind_r)

@views.route('/show_doc/<id>')
def alerter(id):
	creds = None
	form_questions = []
	ques = []
	my_forms = []

	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if not creds or creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
					'wchsintranetv/cs.json', SCOPES)
			flow.redirect_uri = "http://127.0.0.1:5000"
			creds = flow.run_local_server(port=5000)
			
	try:
		drive_service = discovery.build("drive", "v3", credentials=creds)
		my_form = discovery.build("forms","v1",credentials=creds)
		creds.from_authorized_user_file('token.json', SCOPES)
		
		form_id = id
		
		get_result = my_form.forms().get(formId=form_id).execute()
		
		form_questions = get_result["items"]
		
		page_token = None

		for key in form_questions:
			let = dict(key)
			if let.__contains__('questionItem'):
				ques.append(let)
				

			forms_list = drive_service.files().list(q="mimeType='application/vnd.google-apps.form'", spaces='drive',
						fields='nextPageToken, files(id, name)',
						pageToken=page_token
					).execute()
			
			for former in forms_list.get('files', []):
				if former.get("name"):
					title = former.get("name")
					if not my_forms.__contains__(former):
						my_forms.append(former)
						
		return flask.render_template("sections/selected_form.html", form=form_questions, id=id, title=title)
	except HttpError as error:
		print(f"Error with creds {error}")

		if os.path.exists('token.json'):
			with open('token.json', 'w') as token:token.write(creds.to_json())
	
	return flask.render_template("sections/selected_form.html", form=form_questions, id=id, title=title)

@views.route("/")
def splash():
	
	if 'credentials' not in flask.session:
		return flask.redirect('authorize')
	
	credentials = Credentials(
		**flask.session['credentials'])

	if not credentials.valid or credentials.expired:
		print("Wait a second")
		return flask.redirect('logout')

	flask.session['credentials'] = credentials_to_dict(credentials)

	if not credentials.valid or credentials.expired:
		credentials.refresh()
		print("Not authorized")
		return flask.redirect('clear')
	
	my_cards = [
		{"title": "forms", "image": "{{url_for('static', filename='images/undraw/undraw_forms.png')}}", "cards": my_forms, "color": "forms"},
		{"title": "sheets", "image": "{{url_for('static', filename='images/undraw/undraw_sheets.png')}}", "cards": my_sheets, "color": "success"},
		{"title": "docs", "image": "{{url_for('static', filename='images/undraw/undraw_docs.png')}}", "cards": my_docs, "color": "primary"},
		{"title": "drive", "image": "{{url_for('static', filename='images/undraw/undraw_drive.png')}}", "cards": my_drive, "color": "warning"},
	]
	
	return flask.render_template("pages/home.html",cards=my_cards,drive=my_drive,docs=my_docs,forms=my_forms, sheets=my_sheets)

@views.route("/error/<page>/<e>")
def error(page,e):
	return(flask.render_template("pages/error_page.html", title=page, error=e))

@views.route("/authorize")
def authorize():

	flow = InstalledAppFlow.from_client_secrets_file(
		'wchsintranetv/cs.json', scopes=SCOPES
	)

	flow.redirect_uri = flask.url_for('views.oauthcallback', _external=True)

	authorization_url, state = flow.authorization_url(
		access_type = 'offline',
		include_granted_scopes = 'false'
	)

	flask.session['state'] = state

	return flask.redirect(authorization_url)

@views.route('/oauthcallback')
def oauthcallback():

	state = flask.session['state']

	flow = InstalledAppFlow.from_client_secrets_file(
		'wchsintranetv/cs.json',
		scopes=SCOPES,
		state=state
	)	
	flow.redirect_uri = flask.url_for('views.oauthcallback', _external=True)

	authorization_response = flask.request.url

	flow.fetch_token(authorization_response=authorization_response)

	credentials = flow.credentials

	flask.session['credentials'] = credentials_to_dict(credentials)

	return flask.redirect(flask.url_for('views.splash'))

@views.route('/revoke')
def revoke():
	if 'credentials' not in flask.session:
		return ('You need to <a href="/authorize">authorize </a> brfore accessing this page.')
	
	credentials = Credentials(
		**flask.session['credentials']
	)

	revoke = requests.post(
		'http://oauth2.googleapis.com/revoke', 
		params={'token':credentials.token},
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		       )
	status_code = getattr(revoke, 'status_code')

	if status_code == 200:
		return ('Credentials successfully revoked.' )
	else:
		return('An error has occurred.' + printindexTable())
	
@views.route('/clear')
def clearCredentials():
	if 'credentials' in flask.session:
		del flask.session['credentials']
	return (flask.render_template("pages/auth/logout.html"))

@views.route('/logout')
def logout():

	return flask.render_template("pages/auth/logout.html")

@views.route('/home')
def home():
	
	return flask.redirect(flask.url_for("views.splash"))
	
@views.route('/users/<id>')
def user(id):
	credentials=getAuth()
	spreadsheet = discovery.build("sheets", "v4", credentials=credentials,cache_discovery=True)
	
	range_names = "A2:C"
	

	admin_list = discovery.build("admin", "directory_v1", credentials=credentials,cache_discovery=True)
	person_page_token = None
	selected_user = None
	while True:
		try:
			selected_user = admin_list.users().get(
				userKey=id).execute()
			try:
				main_sheet = spreadsheet.spreadsheets()
				main_sheet_results = main_sheet.values().get(
					spreadsheetId="1t52ZcLt8Nni0Biqj7Iu3MCpVerSYvL_KDf0L301PX8o",
					range=range_names
				).execute()

				values = main_sheet_results.get("values", [])
				extension = None
				for row in values:
					if row.__contains__(selected_user['primaryEmail']):
						extension = row[0]
			except HttpError as error:
				print(flask.redirect(f"/error/selected-user/{error.error_details}"))
		except HttpError as error:
			return(flask.redirect(f"/error/users-page/{error.error_details}"))
		break
	return flask.render_template("pages/users.html",user=selected_user, extension=extension)

def credentials_to_dict(credentials):
	return {
		'token': credentials.token,
		'refresh_token': credentials.token,
		'token_uri': credentials.token_uri,
		'client_id': credentials.client_id,
		'client_secret': credentials.client_secret,
		'scopes': credentials.scopes
	}

def printindexTable():
	return('<h1>Log in successful</h1>')

def getNextPage(next_page_token):
	people_page_token = next_page_token
	credentials = Credentials(
		**flask.session['credentials'])

	admin_list = discovery.build("admin", "directory_v1", credentials=credentials)
	while True:
		try:
			admin_results = admin_list.users().list(
				customer='C01oc0sgs', 
				pageToken=people_page_token,
				maxResults=500,
				query="isSuspended=false").execute()
			
			users = admin_results.get('users', [])
			
			for user in users:
				if not my_people.__contains__(user):
					my_people.append(user)
			
			people_page_token = admin_results.get("nextPageToken")

			if not people_page_token:
				break
			else:
				getNextPage(people_page_token)
				
		except HttpError as error:
			return(flask.redirect(f"/error/next-page-token/{error.error_details}"))
		break

def getAuth():

	if 'credentials' not in flask.session:
		return flask.redirect('authorize')
	
	credentials = Credentials(
		**flask.session['credentials'])

	if not credentials.valid or credentials.expired:
		print("Wait a second")
		return flask.redirect('logout')
	
	drive = discovery.build("drive", "v3", credentials=credentials)
	people = discovery.build("people", "v1", credentials=credentials)
	admin_list = discovery.build("admin", "directory_v1", credentials=credentials,cache_discovery=True)
	
	return credentials

def getForms():
		credentials=getAuth()
		drive = discovery.build("drive", "v3", credentials=credentials)

		forms_list = drive.files().list(q="mimeType='application/vnd.google-apps.form'", spaces='drive',fields='nextPageToken, files(id, name)').execute()
				
		for former in forms_list.get('files', []):
			if former.get("name"):
				if not my_forms.__contains__(former):
					my_forms.append(former)

def getFiles():
	credentials=getAuth()
	drive = discovery.build("drive", "v3", credentials=credentials)
	files = drive.files().list().execute()

	for file in files.get('files', []):
		if file.get("name"):
			if not my_drive.__contains__(file):
				my_drive.append(file)
				
def getSheets():
	credentials=getAuth()
	drive = discovery.build("drive", "v3", credentials=credentials)
	sheets_list = drive.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'", spaces='drive', fields='files(id, name)').execute()

	for sheet in sheets_list.get('files', []):
		if sheet.get("name"):
			if not my_sheets.__contains__(sheet):
				my_sheets.append(sheet)

def getDocs():
		credentials=getAuth()
		drive = discovery.build("drive", "v3", credentials=credentials)
		docs_list = drive.files().list(q="mimeType='application/vnd.google-apps.document'", spaces='drive', fields='files(id, name)').execute()

		for doc in docs_list.get('files', []):
			if doc.get("name"):
				if not my_docs.__contains__(doc):
					my_docs.append(doc)

def getUserList():
	credentials=getAuth()
	admin_list = discovery.build("admin", "directory_v1", credentials=credentials,cache_discovery=True)
	
	people_page_token = None
	
	while True:
		try:
			admin_results = admin_list.users().list(
				customer='C01oc0sgs', 
				maxResults=500,
				pageToken=people_page_token,
				query="isSuspended=false").execute()
			
			users = admin_results.get('users', [])
			
			for user in users:
				if not my_people.__contains__(user):
					my_people.append(user)
			
			people_page_token = admin_results.get("nextPageToken")
		
			if not people_page_token:
				break
			else:
				getNextPage(people_page_token)
		except HttpError as error:
			return(flask.redirect(f"/error/next-page-token/{error.error_details}"))
		break

def returnHome():
	print("Yute")
	getUserList()
	return "Yute"