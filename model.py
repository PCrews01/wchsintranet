from website import DB
from dataclasses import dataclass
# create dataclasses for the queries that will be returned

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

# use @dataclass decorator
@dataclass
class GWUser(DB.Model):
	# use :[element] to declare return type
	id:str = DB.Column(DB.String, primary_key=True)
	email:str = DB.Column(DB.String)
	is_admin:bool = DB.Column(DB.Boolean)
	is_delegate_admin:bool = DB.Column(DB.Boolean)
	is_mailbox_setup:bool = DB.Column(DB.Boolean)
	kind:str = DB.Column(DB.String)
	language:str = DB.Column(DB.String)
	first_name:str = DB.Column(DB.String)
	last_name:str = DB.Column(DB.String)
	org_unit_path:str = DB.Column(DB.String)
	organizations:str = DB.Column(DB.String)
	primary_email:str = DB.Column(DB.String, unique=True)
	is_suspended:bool = DB.Column(DB.Boolean)
	thumbnail_url:str = DB.Column(DB.String)
	thumbnail_etag:str = DB.Column(DB.String)
	is_student:bool = DB.Column(DB.Boolean)
	extension:str = DB.Column(DB.String(3), default="0")
