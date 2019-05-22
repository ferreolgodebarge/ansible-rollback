from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from .context import set_context

def run_playbook(playbook, inventory, **kwargs):
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
    result = pbex.run()
    return result, pbex