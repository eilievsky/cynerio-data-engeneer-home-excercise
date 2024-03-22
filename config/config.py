import json

CONFIG_FILE = "config/config.json"


class Config:
    '''
    Configuration manager class
    Using external json file as a configuration storage

    '''

    def __init__(self):
        try:
            with open(CONFIG_FILE, 'r') as config_file:
                file_content = config_file.read()
            self.config = json.loads(file_content)
        except (FileNotFoundError):
            print(f"Problem with loading {CONFIG_FILE} file")
            raise FileNotFoundError

    def get_value(self, key):
        return self.config.get(key)


# Create a single instance of the config object
configobject = Config()
