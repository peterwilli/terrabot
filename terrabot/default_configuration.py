import yaml
import os

def default_configuration(name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_config', name + ".yml")) as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config