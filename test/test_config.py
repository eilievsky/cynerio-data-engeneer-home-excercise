import pytest
from config.config import Config
import os
'''
Testing of configuration manager
'''


def test_ConfigLoadFile(mocker):
    # Mock the file reading operation
    file_content = '{"data1":{"key1": "value1", "key2": "value2"},"data2": {"key3": "value3", "key4": "value4"}}'
    mocker.patch("builtins.open", mocker.mock_open(read_data=file_content))

    # Initialize the Config object
    config = Config()

    # Verify that the config object is initialized correctly
    assert config.get_value("data1") == {'key1': 'value1', 'key2': 'value2'}
    assert config.get_value("data2") == {'key3': 'value3', 'key4': 'value4'}


def test_config_file_not_found(mocker):

    # mock location of not existsing file
    mocker.patch("config.config.CONFIG_FILE", "testfile.json")

    # Verify that the Config object raises FileNotFoundError
    with pytest.raises(FileNotFoundError):
        Config()


def test_ConfigFileLocation(mocker):
    assert os.path.isfile(os.getcwd() + "/config/config.json")
