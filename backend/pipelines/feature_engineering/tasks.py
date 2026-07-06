from storage.interfaces.repository import Repository
from shared.enums.datalayer import DataLayer

def get_symbol_list(
    repository: Repository,
    layer: DataLayer
):
    providers = repository.list_providers(layer)
    return repository.list_keys(layer, providers)