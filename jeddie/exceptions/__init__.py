class MissingConfigException(Exception):
    """Raised when the config file is not set in environmental variables"""
    print('Please set the CONFIG_PATH environment variable to the json config file.')
    pass
