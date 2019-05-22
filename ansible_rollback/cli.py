import os
import json
import click
from core.playbook import run_playbook

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    pass

@cli.command(name="run")
@click.option('--playbook', '-p', required=True, type=click.Path(exists=True), help='Playbook yaml path.')
@click.option('--inventory', '-i', required=True, type=click.Path(exists=True), help='Inventory yaml path.')
@click.option('--extra-vars', '-e', default=None, required=False, multiple=True, help='Extra vars: "key=value".')
def run(playbook, inventory, extra_vars):
    """Run ansible playbook with integrated rollback (need compatible roles)."""
    if not extra_vars:
        extra_vars = ()
    result, full = run_playbook(playbook, inventory, extra_vars=extra_vars)
    print(full._tqm._stats.__dict__)