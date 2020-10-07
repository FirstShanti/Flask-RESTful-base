import re
from uuid import UUID
# from models import User


def email(email_address):
	# from models.user import User
	if (email_is_valid:= re.match(r"^[a-zA-Z0-9_'+*/^&=?~{}\-](\.?[a-zA-Z0-9_'+*/^&=?~{}\-])*\@((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(\:\d{1,3})?)|(((([a-zA-Z0-9][a-zA-Z0-9\-]+[a-zA-Z0-9])|([a-zA-Z0-9]{1,2}))[\.]{1})+([a-zA-Z]{2,6})))$", email_address)):
		print('email valid')
		# if (user:= User.query.filter(User.email==email_is_valid.string).first()):
		# 	return False
		return email_address
	raise ValueError('Invalid email')


def phone(phone_number):
	# from models.user import User
	if (phone_number_is_valid:= re.match(r"^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$", phone_number)):
		print('phone valid')
		# if (user:= User.query.filter(User.phone_number==phone_number_is_valid.string).first()):
		# 	return False
		return phone_number
	raise ValueError('Invalid phonenumber')


def password(password):
	# from models.user import User
	if (password_is_valid:= re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_-]).{6,}", password)):
		print('password valid')
		return password
	raise ValueError('Invalid password')


def uuid(uuid_):
	if (uuid_:= UUID(uuid_)):
		return uuid_.__str__()
	raise ValueError('Invalid uuid')


User_Validator = {
    'register': {
        'firstname': dict(type=str, required=True, help='This field cannot be blank.'),
        'lastname': dict(type=str, required=True, help='This field cannot be blank.'),
        'username': dict(type=str, required=True, help='This field cannot be blank.'),
        'password': dict(type=password, required=True, help='This field must contain at least one number, one lowercase, one uppercase letter, and least six characters'),
        'email': dict(type=email, required=True, help='Invalid email'),
        'phonenumber': dict(type=phone, required=False, help='Invalid phonenumber'),
        'remember_me': dict(type=bool, required=False)
    },
    'login': {
        'username': dict(type=str, required=True, help='This field cannot be blank.'),
        'password': dict(type=password, required=True, help='This field must contain at least one number, one lowercase, one uppercase letter, and least six characters'),
    },
    'delete': {
    	'uuid': dict(type=uuid, required=True, help='This field cannot be blank.')
    },
    'page_limit': {
    	'page': dict(type=int, required=False),
    	'limit': dict(type=int, required=False)
    },
    'update': {
    	'firstname': dict(type=str, required=False, help='This field cannot be blank'),
        'lastname': dict(type=str, required=False, help='This field cannot be blank'),
        'username': dict(type=str, required=False, help='This field cannot be blank'),
        'email': dict(type=email, required=False, help='Invalid email'),
        'phonenumber': dict(type=phone, required=False, help='Invalid phonenumber'),
    }
}
