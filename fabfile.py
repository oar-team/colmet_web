#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os import getenv
from fabric.api import task, run, local, env, cd, execute, roles
from fabric.contrib import files
import fabtools
import fabtools.vagrant

vagrant = fabtools.vagrant.vagrant

env.use_ssh_config = True
env.forward_agent = True
env.app = "colmet"

HOME = getenv('HOME')
WORKON_HOME = getenv('WORKON_HOME', os.path.join(HOME, '.virtualenvs'))
VENV_PATH = os.path.join(WORKON_HOME, env.app)

env.roledefs = {
    'local': ['localhost'],
    'staging': ['vagrant@10.10.10.111:4444']
}


if not env.roles:
    env.roles = ['local']


def setup_env():
    if env.host_string == env.roledefs['staging'][0]:
        env.work_dir = '/var/www/%s' % env.app
    else:
        env.work_dir = os.path.dirname(__file__)


setup_env()


@task
def virtualenv():
    """ Install new virtualenv. """
    fabtools.require.python.virtualenv(VENV_PATH)
    with fabtools.python.virtualenv(VENV_PATH):
        requirements = os.path.join(env.work_dir, "requirements.txt")
        fabtools.python.install_requirements(requirements)
    execute(virtualenv_dev)


@task
@roles("local")
def virtualenv_dev():
    """ Install dev python  packages. """
    with fabtools.python.virtualenv(VENV_PATH):
        requirements = os.path.join(env.work_dir, "dev-requirements.txt")
        fabtools.python.install_requirements(requirements)


@task
def upgrade():
    """ Upgrades virtualenv."""
    with fabtools.python.virtualenv(VENV_PATH):
        run("pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | "
            "xargs pip install -U")


@task
def freeze():
    """ Freezes virtualenv and produces a new requirements.txt."""
    with fabtools.python.virtualenv(VENV_PATH):
        run("pip freeze --local > requirements.txt")


@task
def test():
    """ Runs tests with tox."""
    with cd(env.work_dir):
        with fabtools.python.virtualenv(VENV_PATH):
            run("pip freeze --local > requirements.txt")
    local("tox -- --pdb")


@task
def lint():
    """ Runs python code checks (pep8 and flake)."""
    with fabtools.python.virtualenv(VENV_PATH):
        with cd(env.work_dir):
            run('flake8 $(find . -name "*.py" ! -path "./build/*" ! -path '
                '"./venv/*" ! -path ".tox*" ! -path "*compat.py" '
                '! -path  "*__init__.py" '
                '! -path "*bootstrap.py") ')


@task
@roles("local", "staging")
def sync():
    """ Pushes the commits into remote server."""
    setup_env()
    with cd(env.work_dir):
        run("git sync")


@task
@roles("staging")
def supervisorctl_restart():
    """ Restarts supervisor process."""
    fabtools.supervisor.restart_process(env.app)


@task
def deploy():
    """ Deploys this app to the remote server."""
    execute(sync)
    execute(supervisorctl_restart)


@task
def system_packages():
    """ Install required packages (+extras). """
    fabtools.require.deb.nopackages([
        'apache2.2-common',
    ])
    fabtools.require.deb.packages([
        'build-essential',
        'curl',
        'python-dev',
        'python-pip',
        'git-core',
        'nginx',
        'redis-server',
    ])
    fabtools.require.python.packages([
        'virtualenv',
        'virtualenvwrapper',
    ], use_sudo=True)


@task
def configure_nginx():
    fabtools.require.nginx.server()
    fabtools.require.nginx.proxied_site(
        env.app,
        proxy_url="http://127.0.0.1:5000",
        docroot=os.path.join(env.work_dir, "public"),
    )


@task
def configure_supervisor():
    prod_config_file = "/srv/colmet_prod.cfg"
    prod_config = """
DEBUG=False
HOST=127.0.0.1
PORT=5000
CACHE=redis
CACHE_REDIS_HOST = "localhost"
"""
    files.append(prod_config_file, prod_config, use_sudo=True)
    command = os.path.join(env.work_dir, "manager.py -c %s" % prod_config_file)
    fabtools.require.supervisor.process(
        env.app,
        command=command,
        directory=os.path.join(env.work_dir, "public"),
        user='www-data',
        stdout_logfile='/var/log/supervisor/%s.log' % env.app,
    )


@task
def bootstrap():
    """ Bootstrap. """
    execute(system_packages)
    execute(configure_nginx)
    execute(configure_supervisor)
    execute(virtualenv)
