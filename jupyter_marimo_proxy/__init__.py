#!/usr/bin/env python3

import os

def setup_marimoserver():
	path = os.environ.get('PATH', os.defpath)
	binpath = os.path.expanduser(os.path.join('~', 'bin'))
	if os.path.exists(binpath) and binpath not in path.split(os.pathsep):
		path = (binpath + os.pathsep + path) if len(path) else binpath
	binpath = os.path.expanduser(os.path.join('~', '.local', 'bin'))
	if os.path.exists(binpath) and binpath not in path.split(os.pathsep):
		path = (binpath + os.pathsep + path) if len(path) else binpath
	return {
		'command': ['marimo', 'edit', '--port', '{port}', '--base-url', os.environ['JUPYTERHUB_SERVICE_PREFIX'] + 'marimo', '--no-token', '--headless'],
		'environment': { 'PATH': path },
		'timeout': 60,
		'absolute_url': True,
		'launcher_entry': {
			'title': 'Marimo',
			'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.svg')
		},
	}
