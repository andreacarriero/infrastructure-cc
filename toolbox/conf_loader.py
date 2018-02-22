import json

class RootConfiguration():
    """
    This functions is a read-only access to app's root configuration.

    Example
    =======
    ```
    from toolbox.conf_loader import RootConfiguration
    conf = RootConfuguration()
    ip = conf.get('ip')
    ```
    """
    
    CONFIGURATION_FILE_PATH = 'data/configuration.json'

    def __init__(self):
        try:
            with open(self.CONFIGURATION_FILE_PATH) as configuration_file:
                self.jconf = json.load(configuration_file)
        except Exception as e:
            print("Something is wrong with the root configuration file.")
            print(e)
    
    def get(self, key):
        return self.jconf[key]
