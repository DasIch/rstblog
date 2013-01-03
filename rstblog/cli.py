# -*- coding: utf-8 -*-
"""
    rstblog.cli
    ~~~~~~~~~~~

    The command line interface

    :copyright: (c) 2013 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
import sys
import os
import subprocess
from docopt import docopt
from rstblog.config import Config
from rstblog.builder import Builder


def get_builder(project_folder):
    """Runs the builder for the given project folder."""
    config_filename = os.path.join(project_folder, 'config.yml')
    config = Config()
    if not os.path.isfile(config_filename):
        raise ValueError('root config file "%s" is required' % config_filename)
    with open(config_filename) as f:
        config = config.add_from_file(f)
    return Builder(project_folder, config)


def get_host(interface="en0"):
    return subprocess.check_output(
        ["ipconfig", "getifaddr", interface]
    ).strip()


def main():
    """
    Usage:
        run-rstblog
        run-rstblog build [<folder>]
        run-rstblog serve [--port <port>] [(--host <host> | --interface <interface>)] [<folder>]
        run-rstblog -h | --help

    Options:
        -h --help              Show this.
        --port=port            Port used by server [default: 5000].
        --host=host            Host used by server [default 127.0.0.1].
        --interface=interface  Use IP of network interface [default: en0].
    """
    arguments = docopt(main.__doc__)
    if arguments['build']:
        action = 'build'
    elif arguments['serve']:
        action = 'serve'
    else:
        action = 'build'
    if arguments['<folder>'] is None:
        folder = os.getcwd()
    else:
        folder = arguments['<folder>']

    if arguments["--interface"]:
        host = get_host(arguments["--interface"])
    else:
        host = arguments["--host"]

    builder = get_builder(folder)
    if action == 'build':
        builder.run()
    else:
        builder.debug_serve(
            port=int(arguments["--port"]),
            host=host
        )
