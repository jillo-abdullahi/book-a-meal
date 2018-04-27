"""app/utilities.py"""
from flask import jsonify

def check_keys(args, length):
   """Check if dict keys are provided"""
   params = ['email','username','password','full-name','name','category','description','price']
   for key in args.keys():
       if key not in params or len(args) != length:
           return True
   return False

def check_empty_dict(args):
	"""Check if an empty value given for any key"""
	for key in args:
		if not args[key].strip():
			return True
	return False





