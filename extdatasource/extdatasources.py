from config.config import configobject
from extdatasource.extdatasourceabstract import DSAbstract
import requests


class DStorbulkexitlist(DSAbstract):
    '''
      Torbulkexitlist external data source class

      Attributes:
        raw_data - raw data extracted from data sources
        searchible_data -  IP data that can be searched
        confg_data - configuration data fron conig object
        feed_name - constant feed name
    '''

    raw_data = None
    searchible_data = []
    config_data = None
    feed_name = "Torbulkexitlist"

    def __init__(self) -> None:
        self.config_data = configobject.get_value(self.__class__.__name__)
        if self.config_data is None:
            raise Exception(
                f"No configuration found for {self.__class__.__name__}")

    def _read_data(self) -> None:
        try:
            self.url = self.config_data["URL"]
            response = requests.get(self.url)
            if response.status_code == 200:
                self.raw_data = response.text.split('\n')
            else:
                raise Exception(
                    f"Failed to retrieve IP addresses. Status code: {response.status_code}")
        except requests.exceptions.Timeout:
            print(
                f"Time out exception {self.config_data['URL']} for feeder {self.feed_name}")
        except requests.exceptions.TooManyRedirects:
            print(
                f"Too many rederects {self.config_data['URL']} for feeder {self.feed_name}")
        except requests.exceptions.RequestException as e:
            print(
                f"Too many rederects {self.config_data['URL']} for feeder {self.feed_name}")
        except Exception as e:
            print(e)

    def _create_searchible_structure(self) -> None:
        try:
            self.searchible_data = self.raw_data
        except:
            raise Exception(
                f"Can't create searchibe structure for {self.feed_name}")

    def getFeedName(self):
        return self.feed_name

    def ds_start(self) -> None:
        self._read_data()
        self._create_searchible_structure()

    def searchIP(self, search_item: str) -> bool:
        return search_item in self.searchible_data


class DSIpblocklist(DSAbstract):

    '''
      Torbulkexitlist external data source class

      Attributes:
        raw_data - raw data extracted from data sources
        searchible_data -  IP data that can be searched
        confg_data - configuration data fron conig object
        feed_name - constant feed name 

    '''

    raw_data = None
    searchible_data = []
    config_data = None
    feed_name = "Feodotracker"

    def __init__(self) -> None:
        self.config_data = configobject.get_value(self.__class__.__name__)
        if self.config_data is None:
            raise Exception(
                f"No configuration found for {self.__class__.__name__}")

    def _read_data(self) -> None:
        try:
            self.url = self.config_data["URL"]
            response = requests.get(self.url)
            if response.status_code == 200:
                self.raw_data = response.json()
            else:
                raise Exception(
                    f"Failed to retrieve IP addresses. Status code: {response.status_code}")
        except requests.exceptions.Timeout:
            print(
                f"Time out exception {self.config_data['URL']} for feeder {self.feed_name}")
        except requests.exceptions.TooManyRedirects:
            print(
                f"Too many rederects {self.config_data['URL']} for feeder {self.feed_name}")
        except requests.exceptions.RequestException as e:
            print(
                f"Too many rederects {self.config_data['URL']} for feeder {self.feed_name}")
        except Exception as e:
            print(e)

    def _create_searchible_structure(self) -> None:
        try:
            self.searchible_data = []
            for single_json_record in self.raw_data:
                if 'ip_address' in single_json_record:
                    self.searchible_data.append(
                        single_json_record['ip_address'])
        except:
            raise Exception(
                f"Can't create searchibe structure for {self.feed_name}")

    def getFeedName(self):
        return self.feed_name

    def ds_start(self) -> None:
        self._read_data()
        self._create_searchible_structure()

    def searchIP(self, search_item: str) -> bool:
        return search_item in self.searchible_data
