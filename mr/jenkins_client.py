#
# Jenkins API wrappers
#

from .error import MrError
from api4jenkins import Jenkins, ItemNotFoundError
from .console import run_with_indeterminate_progress
from time import sleep

def start_task_wait_confirmation(username, token, server_url, job, parameters):
	jenkins = Jenkins(server_url, auth=(username, token))
	if not jenkins.exists():
		raise CannotConnect(server_url)

	try:
		qi = jenkins.build_job(job, **parameters)

		def go():
			while not qi.get_build():
				sleep(2)
			return qi.get_build()

		return run_with_indeterminate_progress(go)

	except ItemNotFoundError as e:
		raise JobNotFound(job)

	except Exception as e:
		raise InvalidConfiguration(job, parameters)

class CannotConnect(MrError):
	def __init__(self, url):
		self.url = url

	def __str__(self):
		return "Cannot connect to server at '{}'. Is it reachable?".format(self.url)

class JobNotFound(MrError):
	def __init__(self, job):
		self.job = job

	def __str__(self):
		return "Cannot find job '{}'.".format(self.job)

class InvalidConfiguration(MrError):
	def __init__(self, job, params):
		self.job = job

	def __str__(self):
		return "Invalid configuration for job '{}'.".format(self.job)
