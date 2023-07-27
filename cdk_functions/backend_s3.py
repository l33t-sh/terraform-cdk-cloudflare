from cdktf import S3Backend


def s3_backend(_self, _id, _config):
    S3Backend(
        _self,
        endpoint=_config['backend_s3']['endpoint'],
        access_key=_config['backend_s3']['access_key'],
        secret_key=_config['backend_s3']['secret_key'],
        region=_config['backend_s3']['region'],
        bucket=_config['backend_s3']['bucket'],
        skip_region_validation=_config['backend_s3']['skip_region_validation'],
        skip_metadata_api_check=_config['backend_s3']['skip_metadata_api_check'],
        skip_credentials_validation=_config['backend_s3']['skip_credentials_validation'],
        force_path_style=_config['backend_s3']['force_path_style'],
        key="{}-{}.tfstate".format(
            _config['general']['environment'],
            _id
        )
    )
