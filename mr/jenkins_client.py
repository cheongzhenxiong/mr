#
# Jenkins API wrappers
#

from jenkins import Jenkins
from .console import run_with_indeterminate_progress
from time import sleep

def start_task_wait_confirmation(username, token, server_url, job, parameters):
	jenkins = Jenkins(server_url, username, token)
	queue_id = jenkins.build_job(job, parameters)

	def go():
		return poll_queue_until_executable(jenkins, queue_id)

	return run_with_indeterminate_progress(go)

def poll_queue_until_executable(jenkins, queue_id):
	try:
		item = jenkins.get_queue_item(queue_id)
		return item["executable"]
	except KeyError:
		sleep(2)
		return poll_queue_until_executable(jenkins, queue_id)
