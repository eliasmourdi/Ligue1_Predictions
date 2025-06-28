import os


def load_config(path = '../config.yaml'):
    """
    Loads a config file according to the path given in argument
    """
    
    path = os.path.abspath(path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path, "r") as f:
        config = yaml.safe_load(f)
        
    return config