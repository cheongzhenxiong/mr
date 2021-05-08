#
# Command to start a task
#

from .error import MrError
from .console import *
from .jenkins_client import start_task_wait_confirmation
from .auth import ensure_password

class StartCommand(object):
	def __init__(self, task_name, param_overrides):
		self.task_name = task_name
		self.param_overrides = param_overrides

	def run(self, config):
		task = find_task_by_name(self.task_name, config["tasks"])
		server = find_server_by_name(task["server"], config["servers"])
		username, token = ensure_password(server["credentials"])
		parameters = restrict_overrides_to_known_parameters(task["parameters"], self.param_overrides)

		log_task_start(self.task_name)
		log_build_starting(task["job"], server["url"])
		build = start_task_wait_confirmation(username, token, server["url"], task["job"], parameters)
		log_build_started(build.number, build.url)


class TaskNotFound(MrError):
	def __init__(self, name, available_tasks=[]):
		self.name = name
		self.available_tasks = available_tasks
		
	def __str__(self):
		if self.available_tasks:
			available_names = [task["name"] for task in self.available_tasks]
			return "No tasks found for name '{}'. Available tasks: {}".format(self.name, available_names)
		else:
			return "No tasks found for name '{}'".format(self.name)

class ServerNotFound(MrError):
	def __init__(self, name):
		self.name = name
		
	def __str__(self):
		return "No server found for name '{}'".format(self.name)

class CannotOverride(MrError):
	def __init__(self, parameters):
		self.parameters = parameters
		
	def __str__(self):
		return "Cannot override unknown parameters: {}".format(self.parameters)


def find_one(predicate, items):
	found = [item for item in items if predicate(item)]
	return found[0]

def find_task_by_name(name, tasks):
	try:
		return find_one(lambda task: task["name"] == name, tasks)
	except:
		raise TaskNotFound(name, tasks)

def find_server_by_name(server_name, servers):
	try:
		return find_one(lambda server: server["name"] == server_name, servers)
	except:
		raise ServerNotFound(server_name)

def restrict_overrides_to_known_parameters(known_parameters, overrides):
	unknown_parameters = overrides.keys() - known_parameters.keys()
	if unknown_parameters:
		raise CannotOverride(unknown_parameters)

	return known_parameters | overrides
