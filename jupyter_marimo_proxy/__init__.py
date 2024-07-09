#!/usr/bin/env python3

import os
import base64
import secrets
import configparser

def setup_marimoserver():
	token = secrets.token_urlsafe(16)
	newpath = os.environ.get('JUPYTERMARIMOPROXY_PATH')
	if not newpath:
		config = configparser.ConfigParser()
		config.read(os.path.expanduser(os.path.join('~', '.jupytermarimoproxyrc')))
		newpath = config.get('jupyter-marimo-proxy', 'path', fallback=config.get('DEFAULT', 'path', fallback=None))
	if newpath:
		seen = set()
		newpath = os.path.expandvars(os.pathsep.join(os.path.expanduser(x) for x in newpath.split(os.pathsep)))
		newpath = os.pathsep.join(x for x in newpath.split(os.pathsep) if x and x not in seen and not seen.add(x) and os.path.exists(x))
	return {
		'command': ['marimo', 'edit', '--port', '{port}', '--base-url', os.environ['JUPYTERHUB_SERVICE_PREFIX'] + 'marimo', '--token', '--token-password', token, '--headless'],
		'environment': { 'PATH': newpath } if newpath else {},
		'timeout': 60,
		'absolute_url': True,
		'request_headers_override': { 'Authorization': 'Basic ' + base64.b64encode(b' :' + token.encode()).decode() },
		'launcher_entry': {
			'title': 'Marimo',
			'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.svg')
		},
	}
