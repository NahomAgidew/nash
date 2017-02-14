from peewee import *
from config import *

db = SqliteDatabase(nashdb)

class User(Model):
	id = PrimaryKeyField()
	username = TextField()
	email = TextField()
	password = TextField()

	class Meta:
		database = db

class Project(Model):
	username = TextField()
	project_name = TextField()
	progress = IntegerField()

	class Meta:
		database = db



def initialize():
	db.connect()
	db.create_tables([User, Project], safe=True)
