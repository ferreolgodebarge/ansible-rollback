from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from .context import set_context

def run_playbook(playbook, inventory, **kwargs):
    set_context(playbook, inventory, **kwargs)
    l = DataLoader()
    if isinstance(inventory, str):
        i = InventoryManager(loader=l, sources=inventory)
    elif isinstance(inventory, InventoryManager):
        i = inventory
    else:
        print("Inventory must be either a string or an Inventory Manager, {} provided".format(type(inventory)))
    v = VariableManager(loader=l, inventory=i)
    pbex = PlaybookExecutor(
        playbooks=[playbook],
        inventory=i,
        variable_manager=v,
        loader=l,
        passwords={},
    )
    result = pbex.run()
    return result, pbex

def hosts_to_be_rollbacked(full_stats):
    inventory_manager = full_stats._tqm._inventory
    inventory = full_stats._tqm._inventory._inventory
    stats = full_stats._tqm._stats.__dict__
    failures = [x for x in stats['failures'].keys()]
    processed = [x for x in stats['processed'].keys()]
    rollack_hosts = {}
    i = 0
    for fail in failures:
        rollack_hosts[i] = fail
        i += 1 
    for process in processed:
        if process not in rollack_hosts.values():
            rollack_hosts[i] = process
            i += 1
    for host in list(inventory_manager.hosts.values()):
        if host.name in rollack_hosts.values():
            inventory.get_host(host)
            continue
        else:
            inventory.remove_host(host)
    inventory.reconcile_inventory()
    inventory_manager.clear_caches()
    return inventory_manager