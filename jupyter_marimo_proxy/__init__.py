#!/usr/bin/env python3

import os

if (
	os.path.exists(os.path.join(os.environ["HOME"], "bin"))
	and not os.path.join(os.environ["HOME"], "bin") in os.getenv("PATH", "")
):
	os.environ["PATH"] = (
		os.path.join(os.environ["HOME"], "bin")
		+ os.pathsep
		+ os.getenv("PATH", "")
	)

if (
	os.path.exists(os.path.join(os.environ["HOME"], ".local", "bin"))
	and not os.path.join(os.environ["HOME"], ".local", "bin")
	in os.getenv("PATH", "")
):
	os.environ["PATH"] = (
		os.path.join(os.environ["HOME"], ".local", "bin")
		+ os.pathsep
		+ os.getenv("PATH", "")
	)

def setup_marimoserver():
    return {
        "command": [
            "marimo",
            "edit",
            "--port",
            "{port}",
            "--base-url",
            os.environ["JUPYTERHUB_SERVICE_PREFIX"] + "marimo",
            "--no-token",
            "--headless",
        ],
        "timeout": 60,
        "absolute_url": True,
        "launcher_entry": {
            "title": "Marimo",
            "icon_path": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "icon.svg"
            ),
        },
    }
