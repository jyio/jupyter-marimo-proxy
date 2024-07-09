#!/usr/bin/env python3

import os
import setuptools

setuptools.setup(
	name='jupyter-marimo-proxy',
	version='0.0.4',
	url='https://github.com/jyio/jupyter-marimo-proxy',
	author='Jiang Yio',
	description='Jupyter extension to proxy Marimo',
	long_description=open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8').read(),
	long_description_content_type='text/markdown',
	packages=setuptools.find_packages(),
	package_data={
		'jupyter_marimo_proxy': ['icon.svg'],
	},
	entry_points={
		'jupyter_serverproxy_servers': [
			# name = packagename:function_name
			'marimo = jupyter_marimo_proxy:setup_marimoserver',
		]
	},
	install_requires=['jupyter-server-proxy'],
)
