import pytest
import requests
from extdatasource.extdatasourcesfactory import DSFactory
from extdatasource.extdatasources import DSIpblocklist, DStorbulkexitlist


def test_search_datasources_found(mocker):

    my_class = DSFactory()

    # Mock the dsObjects attribute with a list of objects
    mock_objects = [
        mocker.Mock(searchIP=lambda x: x == "10.0.0.1",
                    getFeedName=lambda: "Feed 1"),
        mocker.Mock(searchIP=lambda x: x == "10.0.0.2",
                    getFeedName=lambda: "Feed 2"),
        mocker.Mock(searchIP=lambda x: x == "10.0.0.3",
                    getFeedName=lambda: "Feed 3"),
    ]
    my_class.dsObjects = mock_objects

    # Perform the search
    result = my_class.search_datasources("10.0.0.2")

    # Verify the result
    expected_result = {
        "is_found": True,
        "feed_name": "Feed 2",
        "ip": "10.0.0.2"
    }
    assert result == expected_result


def test_search_datasources_notfound(mocker):

    my_class = DSFactory()

    # Mock the dsObjects attribute with a list of objects
    mock_objects = [
        mocker.Mock(searchIP=lambda x: x == "10.0.0.1",
                    getFeedName=lambda: "Feed 1"),
        mocker.Mock(searchIP=lambda x: x == "10.0.0.2",
                    getFeedName=lambda: "Feed 2"),
        mocker.Mock(searchIP=lambda x: x == "10.0.0.3",
                    getFeedName=lambda: "Feed 3"),
    ]
    my_class.dsObjects = mock_objects

    # Perform the search
    result = my_class.search_datasources("10.0.0.8")

    # Verify the result
    expected_result = {
        "is_found": False,
        "feed_name": "",
        "ip": "10.0.0.8"
    }
    assert result == expected_result


# Testing for DStorbulkexitlist object
def test_constructor_with_config_data_DStorbulkexitlist(mocker):
    # Mock the configobject.get_value method to return some config data
    mocker.patch("extdatasource.extdatasources.configobject.get_value",
                 return_value={"key": "value"})

    my_class = DStorbulkexitlist()

    expected_config_data = {"key": "value"}
    assert my_class.config_data == expected_config_data


def test_constructor_without_config_data_DStorbulkexitlist(mocker):
    # Mock the configobject.get_value method to return None
    mocker.patch(
        "extdatasource.extdatasources.configobject.get_value", return_value=None)

    with pytest.raises(Exception) as e:
        my_class = DStorbulkexitlist()

    expected_exception_message = f"No configuration found for DStorbulkexitlist"
    assert str(e.value) == expected_exception_message


def test_read_data_process_DStorbulkexitlist(mocker):

    dstorbulkexitlist_object = DStorbulkexitlist()

    # Mock the config_data and requests.get method
    dstorbulkexitlist_object.config_data = {"URL": "http://example.com"}
    mocker.patch.object(requests, "get", return_value=create_mock_response_DStorbulkexitlist(
        200, "10.01.01.127\n10.01.01.128\n10.01.01.129"))

    # Call the _read_data method
    dstorbulkexitlist_object._read_data()

    # Verify that the url and raw_data attributes are set correctly
    assert dstorbulkexitlist_object.url == "http://example.com"
    assert dstorbulkexitlist_object.raw_data == [
        "10.01.01.127", "10.01.01.128", "10.01.01.129"]

    # Verify that searchible structure was set correctly
    dstorbulkexitlist_object._create_searchible_structure()
    assert dstorbulkexitlist_object.searchible_data == [
        "10.01.01.127", "10.01.01.128", "10.01.01.129"]

    # verify that result is returned correctly for exisrting and not existing values
    assert dstorbulkexitlist_object.searchIP('10.01.01.127') == True
    assert dstorbulkexitlist_object.searchIP('10.01.01.333') == False


# Testing for DSIpblocklist object
def test_constructor_with_config_data_DSIpblocklist(mocker):

    mocker.patch("extdatasource.extdatasources.configobject.get_value",
                 return_value={"key": "value"})

    my_class = DSIpblocklist()

    expected_config_data = {"key": "value"}
    assert my_class.config_data == expected_config_data


def test_constructor_without_config_data_DSIpblocklist(mocker):
    # Mock the configobject.get_value method to return None
    mocker.patch(
        "extdatasource.extdatasources.configobject.get_value", return_value=None)

    with pytest.raises(Exception) as e:
        my_class = DSIpblocklist()

    # Verify that the exception message is correct
    expected_exception_message = f"No configuration found for DSIpblocklist"
    assert str(e.value) == expected_exception_message


def test_read_data_process_DSIpblocklist(mocker):

    dstorbulkexitlist_object = DSIpblocklist()

    # Mock the config_data and requests.get method
    dstorbulkexitlist_object.config_data = {"URL": "http://example.com"}
    mocker.patch.object(
        requests, "get", return_value=create_mock_response_DSIpblocklist(200))

    # Call the _read_data method
    dstorbulkexitlist_object._read_data()

    # Verify that the url and raw_data attributes are set correctly
    assert dstorbulkexitlist_object.url == "http://example.com"
    assert dstorbulkexitlist_object.raw_data == [
        {
            "ip_address": "192.9.135.73",
            "port": 1194,
            "status": "online",
            "hostname": "",
            "as_number": 31898,
            "as_name": "ORACLE-BMC-31898",
            "country": "US",
            "first_seen": "2023-05-23 17:51:44",
            "last_online": "2024-03-22",
            "malware": "Pikabot"
        },
        {
            "ip_address": "103.82.243.5",
            "port": 13785,
            "status": "online",
            "hostname": "103-82-243-5.idcloudhosting.my.id",
            "as_number": 136170,
            "as_name": "EXBCOID-AS-AP PT. EXABYTES NETWORK INDONESIA",
            "country": "ID",
            "first_seen": "2024-02-13 22:11:26",
            "last_online": "2024-03-22",
            "malware": "Pikabot"
        }
    ]

    # verify that searchible object created correctly
    dstorbulkexitlist_object._create_searchible_structure()
    assert dstorbulkexitlist_object.searchible_data == [
        '192.9.135.73', '103.82.243.5']

    # verify that search functionality return correct results for existing and not existing onjects
    assert dstorbulkexitlist_object.searchIP('103.82.243.5') == True
    assert dstorbulkexitlist_object.searchIP('103.82.243.88') == False


def create_mock_response_DStorbulkexitlist(status_code, text=None):
    # create mock data for response DStorbulkexitlist object
    mock_response = requests.Response()
    mock_response.status_code = status_code
    mock_response._content = text.encode() if text else None
    return mock_response


def create_mock_response_DSIpblocklist(status_code):
    # create mock data for response DSIpblocklist object
    mock_response = requests.Response()
    mock_response.status_code = status_code
    text = """[
    {
        "ip_address": "192.9.135.73",
        "port": 1194,
        "status": "online",
        "hostname": "",
        "as_number": 31898,
        "as_name": "ORACLE-BMC-31898",
        "country": "US",
        "first_seen": "2023-05-23 17:51:44",
        "last_online": "2024-03-22",
        "malware": "Pikabot"
    },
    {
        "ip_address": "103.82.243.5",
        "port": 13785,
        "status": "online",
        "hostname": "103-82-243-5.idcloudhosting.my.id",
        "as_number": 136170,
        "as_name": "EXBCOID-AS-AP PT. EXABYTES NETWORK INDONESIA",
        "country": "ID",
        "first_seen": "2024-02-13 22:11:26",
        "last_online": "2024-03-22",
        "malware": "Pikabot"
    }
]"""
    mock_response._content = text.encode()
    return mock_response
