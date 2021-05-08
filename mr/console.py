from rich.progress import Progress, TextColumn, BarColumn
from rich.prompt import Prompt
from rich.console import Console

APP_NAME = "Mr."

_console = Console(highlight=False)

_progress = Progress(
	TextColumn("[yellow]{task.description}"),
	BarColumn(pulse_style="yellow"),
	transient=True
)

def run_with_indeterminate_progress(f):
	with _progress:
		task = _progress.add_task("Waiting for build to start...", total=1000, start=False)
		return f()

def ask_password(prompt):
	return Prompt.ask("[cyan]{}".format(prompt), password=True)

def log_task_start(task_name):
	_console.print("[b white]{}[/] will run task [b green]{}[/]...".format(APP_NAME, task_name))

def log_build_starting(job, server_url):
	_console.print("Starting job [b white]{}[/] on [b white]{}[/]...".format(job, server_url))

def log_build_started(build_number, build_url):
	_console.print("Build [b green]{}[/] started at [b u blue]{}[/]".format(build_number, build_url))

def log_configuration_found(path):
	_console.print("Using configuration file [b white]{}[/]...".format(path))