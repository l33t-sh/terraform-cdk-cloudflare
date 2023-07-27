import yaml


def get_config(path_to_config):
    with open(path_to_config, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as yaml_error:
            print(yaml_error)