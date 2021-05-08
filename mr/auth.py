#
# support for defining and retrieving credentials
#

from .error import MrError
import keyring
import getpass
from .console import ask_password

class AuthError(MrError):
	pass
		
def get_password(credential_name, user):
	try:
		return keyring.get_password(credential_name, user)
	except:
		raise AuthError

def set_password(password, credential_name, user):
	try:
		keyring.set_password(credential_name, user, password)
	except:
		raise AuthError

def ensure_password(credential_name, user=getpass.getuser()):
	password = get_password(credential_name, user)
	if password is None:
		password = ask_password("Enter password/token for '{}' at '{}': ".format(user, credential_name))
		set_password(password, credential_name, user)
		password = get_password(credential_name, user)

	return (user, password)
