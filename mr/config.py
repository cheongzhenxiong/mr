#
# Utilities to read configuration
#
# See mr.toml in this repo for a configuration sample.
#

from .error import MrError
import tomlkit
import os.path
from collections import Counter

class NoConfigurationFile(MrError):
	def __init__(self, path):
		self.path = path
		
	def __str__(self):
		return "Cannot find configuration file '{}'".format(self.path)

class InvalidConfigurationFile(MrError):
	def __init__(self, path, e):
		self.path = path
		self.e = e
		
	def __str__(self):
		return "Invalid configuration file '{}': {}".format(self.path, self.e)

class DuplicateNames(MrError):
	def __init__(self, item, names):
		self.item = item
		self.names = names
		
	def __str__(self):
		return "{} names are not unique: {}".format(self.item, self.names)

class MissingNames(MrError):
	def __init__(self, item, names):
		self.item = item
		self.names = names
		
	def __str__(self):
		return "{} names are used but not defined: {}".format(self.item, self.names)

def _tasks(config):
	return config["tasks"]

def _servers(config):
	return config["servers"]

def _used_servers(config):
	return [task["server"] for task in _tasks(config)]

def _validate_no_duplicate_names(item_name, items):
	all_names = [item["name"] for item in items]
	if len(set(all_names)) == len(all_names):
		return
	
	duplicate_names = [k for (k, v) in Counter(all_names).items() if v > 1]
	raise DuplicateNames(item_name, duplicate_names)

def _validate_named_items_exist(item_name, names, items):
	existing_names = set(item["name"] for item in items)
	missing_names = set(names) - existing_names

	if not missing_names:
		return
	
	raise MissingNames(item_name, list(missing_names))

def _validate_configuration(config):
	_validate_no_duplicate_names("Task", _tasks(config))
	_validate_no_duplicate_names("Server", _servers(config))
	_validate_named_items_exist("Server", _used_servers(config), _servers(config))


def _fixup_relative_paths(config, base_path):
	for server in _servers(config):
		if not "certs" in server:
			continue

		cert_path = server["certs"]
		if not os.path.isabs(cert_path):
			server["certs"] = os.path.join(base_path, cert_path)

	return config


def fetch_configuration(config_path):
	try:
		h = open(config_path)
	except:
		raise NoConfigurationFile(config_path)

	try:
		config = tomlkit.loads(h.read())
	except Exception as e:
		raise InvalidConfigurationFile(config_path, e)
	finally:
		h.close()

	base_path = os.path.dirname(os.path.abspath(config_path))
	config = _fixup_relative_paths(config, base_path)

	_validate_configuration(config)
		
	return config