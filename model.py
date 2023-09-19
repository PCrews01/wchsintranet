from website import DB

class Users(DB.Model):
	id = DB.Column(DB.Integer, primary_key=True)
	name = DB.Column(DB.String(50))
	email = DB.Column(DB.String(50), unique=True)

class MyForms(DB.Model):
	id = DB.Column(DB.Integer, primary_key=True)
	form_id = DB.Column(DB.String, unique=True)

class MyCard(DB.Model):
	id = DB.Column(DB.Integer, primary_key=True)
	title = DB.Column(DB.String)
	card_img = DB.Column(DB.String)
