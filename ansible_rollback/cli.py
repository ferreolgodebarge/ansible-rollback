import os
import json
import click
from core.playbook import (
    run_playbook,
    hosts_to_be_rollbacked,
)

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
    first_result, full = run_playbook(playbook, inventory, extra_vars=extra_vars)
    if first_result != 0:
        rollback_inventory = hosts_to_be_rollbacked(full)
        rollback_extra_vars = extra_vars + ("rollback=1",)
        run_playbook(playbook, rollback_inventory, extra_vars=rollback_extra_vars)
