#!/usr/bin/python3
from app import app
from subprocess import run
from app import db

if app.config == 'Development':
	db.create_all()
	db.session.commit()

if __name__=='__main__':
	app.run(host='0.0.0.0')