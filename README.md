# Jupyter + Marimo = ❤️

`jupyter-marimo-proxy` enables the **JupyterLab** launcher and the classic **Jupyter Notebook** file browser to launch **[Marimo](https://marimo.io/)**.

On a **JupyterHub** deployment, `jupyter-marimo-proxy` leverages **JupyterHub**'s existing authenticator and spawner to launch **Marimo** within users' **Jupyter** environments.

## Installation

`jupyter-marimo-proxy` requires **Marimo**, but does not explicitly declare a dependency on `marimo`, so they may be installed separately. Both may be installed using `pip` like so:

```sh
$ pip install 'marimo>=0.6.21' jupyter-marimo-proxy
```

## Minimal demo, single Python environment

The following Dockerfile builds an image that runs **JupyterHub** (on port `8000`) with `DummyAuthenticator` (`demo`:`demo`), `LocalProcessSpawner`, **Marimo**, and `jupyter-marimo-proxy`.

```dockerfile
FROM	quay.io/jupyterhub/jupyterhub:latest
RUN	cd /srv/jupyterhub && jupyterhub --generate-config && \
	echo "c.JupyterHub.authenticator_class = 'dummy'" >> jupyterhub_config.py && \
	echo "c.DummyAuthenticator.password = 'demo'" >> jupyterhub_config.py && \
	pip install --no-cache-dir notebook 'marimo>=0.6.21' jupyter-marimo-proxy
RUN	useradd -ms /bin/bash demo
```

## Advanced demo, multiple Python environments

With more complicated setups that include multiple Python environments, it is vital to determine *where* each package is to be installed. **Marimo** should be installed into the *user's* environment to access the user's packages but made available in the search path so **Jupyter** could find it, and `jupyter-marimo-proxy` must be installed directly into **Jupyter**'s environment so **Jupyter** could import it.

Consider the following example, in which **Jupyter** comes pre-installed in the root environment but **Miniforge** is installed for the user. We take care to install **Marimo** using `/opt/conda/bin/pip` and `jupyter-marimo-proxy` using `/usr/bin/pip`. By the magic of search path manipulation, **Marimo** is also available to **Jupyter**.

```dockerfile
FROM	quay.io/jupyterhub/jupyterhub:latest

RUN	cd /srv/jupyterhub && jupyterhub --generate-config && \
	echo "c.JupyterHub.authenticator_class = 'dummy'" >> jupyterhub_config.py && \
	echo "c.DummyAuthenticator.password = 'demo'" >> jupyterhub_config.py && \
	pip install --no-cache-dir notebook

ENV	PATH=/opt/conda/bin:$PATH
RUN	curl -fsSL https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -o /root/miniforge.sh && chmod +x /root/miniforge.sh && \
	bash /root/miniforge.sh -b -p /opt/conda && rm /root/miniforge.sh

RUN	/opt/conda/bin/pip install --no-cache-dir 'marimo>=0.6.21'
RUN	/usr/bin/pip install --no-cache-dir jupyter-marimo-proxy

RUN	useradd -ms /bin/bash demo
```

## Executable search path modification

For search path modifications that should be available to all users, I'd recommend invoking **Jupyter** with the desired search path, e.g., by setting `PATH` in the Dockerfile or an entrypoint wrapper. On some deployments, it may be impractical to set up the search path before/while invoking **Jupyter**, such as when the exact paths must be resolved at runtime. `jupyter-marimo-proxy` provides two ways to modify the search path: by environment variable or by configuration file.

For example, to prepend `~/.local/bin:~/bin` to the search path, one could set environment variable `JUPYTERMARIMOPROXY_PATH` to `~/.local/bin:~/bin:$PATH` or create a configuration file `~/.jupytermarimoproxyrc` containing:

```ini
[DEFAULT]
path = ~/.local/bin:~/bin:$PATH
```

If using the environment variable, `JUPYTERMARIMOPROXY_PATH` may need to be added to [`c.Spawner.env_keep`](https://jupyterhub.readthedocs.io/en/stable/reference/api/spawner.html#jupyterhub.spawner.Spawner.env_keep) in the **JupyterHub** configuration.

Both methods support home directory and environment variable expansion, and the `JUPYTERMARIMOPROXY_PATH` variable may be subject to double-expansion if not properly escaped or quoted. If the environment variable and the configuration option were both present, the environment variable would take precedence.

## Usage with DockerSpawner

**Marimo** and `jupyter-marimo-proxy` should be installed into the single-user containers. They are not needed by the main hub.

## Troubleshooting

### **Marimo** icon does not appear in the launcher

Make sure `jupyter-marimo-proxy` is installed into the same Python environment where **Jupyter** is installed. See advanced example above.

### **Marimo** icon appears in the launcher, but fails to launch **Marimo**

Make sure **Marimo** is installed and available in the search path. If the search path were modified in a *descendent* of **Jupyter**, the modification would not be available to **Jupyter** itself. See advice regarding search path modification above.

[b-data](https://github.com/b-data) customers should use [b-data's fork](https://github.com/b-data/jupyterlab-r-docker-stack#marimo).

### **Marimo** icon launches **Marimo**, but **Marimo** could not find modules that have already been installed

Make sure **Marimo** is installed into the Python environment where these modules are installed. Alternatively, make sure the expected modules are installed into the Python environment where **Marimo** is installed. See advanced example above.

### **Marimo** returns "Error: No such option: --base-url"

The `--base-url` argument was introduced to `marimo edit` in version `0.6.21`. Try **Marimo** `0.6.21` or newer.
