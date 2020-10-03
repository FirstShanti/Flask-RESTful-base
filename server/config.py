import os

basedir = os.getcwd()
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_ROOT_PASSWORD')
mysql_host = os.getenv('MYSQL_HOST')
mysql_port = os.getenv('MYSQL_PORT')
mysql_db = os.getenv('MYSQL_DB')

print(mysql_user,
	  mysql_password,
	  mysql_host,
	  mysql_port,
	  mysql_db)


class Configuration(object):
	DEBUG = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.getenv('SECRET_KEY')


class Development(Configuration):
	DEBUG = True
	SQLALCHEMY_ECHO = True
	# SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


class Production(Configuration):
	SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}'
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


env = {
	'Production': Production,
	'Development': Development,
	'Configuration': Configuration
	}
