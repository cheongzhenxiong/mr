#
# Jenkins API wrappers
#

from api4jenkins import Jenkins
from .console import run_with_indeterminate_progress
from time import sleep

def start_task_wait_confirmation(username, token, server_url, job, parameters):
	jenkins = Jenkins(server_url, auth=(username, token))

	qi = jenkins.build_job(job, **parameters)

	def go():
		while not qi.get_build():
			sleep(2)
		return qi.get_build()

	return run_with_indeterminate_progress(go)
