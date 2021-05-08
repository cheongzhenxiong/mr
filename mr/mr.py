#
# a script to automate Jenkins builds
#
# usage: mr start TASK
#

from .error import MrError
from .cmdline import parse_arguments
from .config import fetch_configuration
from .console import *

def main():
	try:
		handler, config_path = parse_arguments()
		config = fetch_configuration(config_path)
		log_configuration_found(config_path)
		handler.run(config)
	except MrError as e:
		print(e)
	
if __name__ == "__main__":
	main()
