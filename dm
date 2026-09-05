#!/usr/bin/env -S /bin/sh -c '"$(dirname "$0")/backend/venv/bin/python" "$0" "$@"'

import ultraclick as click

from cli.cli import MainGroup

cli = click.group_from_class(MainGroup)
cli(prog_name="dm")
