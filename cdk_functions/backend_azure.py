from cdktf import AzurermBackend


def azure_backend(_self, _ns, _config):
    AzurermBackend(
        _self,
        tenant_id=_config['backend_azure']['tenant_id'],
        client_id=_config['backend_azure']['client_id_config'],
        client_secret=_config['backend_azure']['client_secret'],
        subscription_id=_config['backend_azure']['subscription_id'],
        resource_group_name=_config['backend_azure']['resource_group_name'],
        storage_account_name=_config['backend_azure']['storage_account_name'],
        container_name=_config['backend_azure']['container_name'],
        key="{}-{}-{}.tfstate".format(
            _config['backend_azure']['key'],
            _config['general']['environment'],
            _ns
        )
    )
