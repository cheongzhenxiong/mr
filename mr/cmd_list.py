#
# Command to list all tasks in the configuration file.
#

class ListCommand(object):
	def __init__(self):
		pass
		
	def run(self, config):
		tasks = config["tasks"]
		for task in tasks:
			print(task["name"])
