from constructs import Construct
from cdktf import TerraformStack

from cdk_functions.get_config import get_config
from cdk_functions.backend_s3 import s3_backend
from cdk_functions.backend_azure import azure_backend

from cdktf_cdktf_provider_cloudflare.provider import CloudflareProvider
from cdktf_cdktf_provider_cloudflare.data_cloudflare_zone import DataCloudflareZone
from cdktf_cdktf_provider_cloudflare.zone import Zone
from cdktf_cdktf_provider_cloudflare.record import Record


class CloudflareStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        config = get_config("config/config.yml")

        if "backend_azure" in config:
            azure_backend(self, id, config)
        elif "backend_s3" in config:
            s3_backend(self, id, config)
        else:
            print("### | {} | No backend specified! Please follow the example readme!".format(
                id
            ))
            exit(1)

        CloudflareProvider(
            self,
            "cloudflare-provider",
            api_key=config['cloudflare']['api_key'],
            email=config['cloudflare']['email'],
            retries=config['cloudflare']['retries'],
        )

        for zone in config['zones']:
            if zone['create_zone'] is True:
                print("### | {} | Creating DNS Zone with name [{}]".format(
                    id,
                    zone['name']
                ))
                domain_zone = Zone(
                    self,
                    "cf-zone-{}".format(
                        zone['name']
                    ),
                    account_id=config['general']['cloudflare_account_id'],
                    zone=zone['name'],
                )
            else:
                print("### | {} | Using DNS Zone with name [{}]".format(
                    id,
                    zone['name']
                ))
                domain_zone = DataCloudflareZone(
                    self,
                    "cf-zone-{}".format(
                        zone['name']
                    ),
                    account_id=config['general']['cloudflare_account_id'],
                    name=zone['name'],
                )

            for record in zone['records']:
                print("### | {} | Adding [{}] as [{}]".format(
                    id,
                    record['name'],
                    record['type'],
                ))
                Record(
                    self,
                    "cf-record-{}-{}".format(
                        zone['name'],
                        record['name']
                    ),
                    name=record['name'],
                    type=record['type'],
                    zone_id=domain_zone.id,
                    allow_overwrite=record['allow_overwrite'] if "allow_overwrite" in record else False,
                    comment=record['comment'] if "comment" in record else None,
                    priority=record['priority'] if "priority" in record else None,
                    proxied=record['proxied'] if "proxied" in record else False,
                    ttl=record['ttl'] if "ttl" in record else 1,
                    value=record['value']
                )
