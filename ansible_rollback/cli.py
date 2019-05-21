import os
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor

from core.context import set_context


def run(playbook, inventory, **kwargs):
    set_context(playbook, inventory, **kwargs)
    l = DataLoader()
    i = InventoryManager(loader=l, sources=inventory)
    v = VariableManager(loader=l, inventory=i)
    pbex = PlaybookExecutor(
        playbooks=[playbook],
        inventory=i,
        variable_manager=v,
        loader=l,
        passwords={},
    )
    results = pbex.run()
    return results

if __name__ == "__main__":
    p = os.path.join(os.getcwd(), 'playbooks/test.yml')
    i = os.path.join(os.getcwd(), 'playbooks/inventories/local/hosts')
    ev = ('rollback=true',)
    run(p, i, extra_vars=ev)