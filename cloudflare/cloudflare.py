from constructs import Construct
from cdktf import TerraformStack, S3Backend, Token

from cdk_functions.get_config import get_config

from cdktf_cdktf_provider_cloudflare.provider import CloudflareProvider
from cdktf_cdktf_provider_cloudflare.data_cloudflare_zone import DataCloudflareZone
from cdktf_cdktf_provider_cloudflare.zone import Zone
from cdktf_cdktf_provider_cloudflare.record import Record, RecordData


class CloudflareStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        config = get_config("config/config.yml")

        cf_account_id = config['general']['cloudflare_account_id']
        target_environment = config['general']['environment']
        null_value = Token.as_string(Token.null_value())

        CloudflareProvider(
            self,
            "cloudflare-provider",
            api_key=config['cloudflare']['api_key'],
            email=config['cloudflare']['email'],
            retries=config['cloudflare']['retries'],
        )

        S3Backend(
            self,
            endpoint=config['backend_s3']['endpoint'],
            access_key=config['backend_s3']['access_key'],
            secret_key=config['backend_s3']['secret_key'],
            region=config['backend_s3']['region'],
            bucket=config['backend_s3']['bucket'],

            skip_region_validation=config['backend_s3']['skip_region_validation'],
            skip_metadata_api_check=config['backend_s3']['skip_metadata_api_check'],
            skip_credentials_validation=config['backend_s3']['skip_credentials_validation'],
            force_path_style=config['backend_s3']['force_path_style'],

            key="{}-{}.tfstate".format(
                target_environment,
                id
            )
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
                    account_id=cf_account_id,
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
                    account_id=cf_account_id,
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
