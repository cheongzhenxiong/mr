import sys
import argparse
from .cmd_start import StartCommand
from .cmd_list import ListCommand

DEFAULT_CONFIG_FILE = "./mr.toml"

class ArgumentParser(argparse.ArgumentParser):
	def error(self, message):
		self.print_help(sys.stderr)
		super().error(message)

def parse_arguments():
	parser = ArgumentParser(description="A launcher for Jenkins builds.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	
	configurable_command_parser = ArgumentParser(add_help=False)
	configurable_command_parser.add_argument("--config", default=DEFAULT_CONFIG_FILE, help="The configuration file to use (default: %(default)s)")
	
	subparsers = parser.add_subparsers(title='commands', required=True, dest="command")
	start_parser = subparsers.add_parser("start", description="Starts a build on a Jenkins server", parents=[configurable_command_parser])
	start_parser.add_argument("task", help="The task to start")
	start_parser.add_argument("--override", action="append", nargs=2, default=[], metavar=("name", "value"), help="Override a parameter for the build")
	start_parser.set_defaults(dispatch=dispatch_start)

	list_parser = subparsers.add_parser("list", description="Lists tasks in a configuration file", parents=[configurable_command_parser])
	list_parser.set_defaults(dispatch=dispatch_list)

	try:
		args = parser.parse_args()
		return args.dispatch(args), args.config
	except argparse.ArgumentError:
		parser.print_help()


def dispatch_start(args):
	task_name = args.task
	param_overrides = { item[0]: item[1] for item in args.override }
	return StartCommand(task_name, param_overrides)

def dispatch_list(args):
	return ListCommand()
	