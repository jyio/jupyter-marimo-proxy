#!/usr/bin/env python3

import os

def setup_marimoserver():
	return {
		'command': ['marimo', 'edit', '--port', '{port}', '--base-url', os.environ['JUPYTERHUB_SERVICE_PREFIX'] + 'marimo', '--no-token', '--headless'],
		'timeout': 60,
		'absolute_url': True,
		'launcher_entry': {
			'title': 'Marimo',
			'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.svg')
		},
	}
