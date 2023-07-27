from constructs import Construct
from cdktf import App, TerraformStack, S3Backend

from cdk_functions.get_config import get_config

from cdktf_cdktf_provider_cloudflare.provider import CloudflareProvider
from cdktf_cdktf_provider_cloudflare.data_cloudflare_zone import DataCloudflareZone


class CloudflareStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        config = get_config("config/config.yml")

        cf_account_id=config['general']['cloudflare_account_id']
        target_environment=config['general']['environment']

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
            domain_zone = DataCloudflareZone(
                self,
                "cf-zone-{}".format(
                    zone['name']
                ),
                account_id=cf_account_id,
                name=zone['name'],
            )


