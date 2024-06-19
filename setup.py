#!/usr/bin/env python3

import setuptools

setuptools.setup(
	name='jupyter-marimo-proxy',
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
