# from datasource.datasources import DStorbulkexitlist, DSIpblocklist
from extdatasource.extdatasources import DSIpblocklist, DStorbulkexitlist

datasource_objects = [DStorbulkexitlist, DSIpblocklist]


class DSFactory:

    '''
    External data source factory class
    Used as a centrilize gateway for  data source objects
    '''

    def __init__(self) -> None:
        pass

    def init_datasources(self) -> None:
        '''Initiate all datasource objects'''
        self.dsObjects = [x() for x in datasource_objects]

    def start_datasources(self) -> None:
        ''' Start all data source objects'''
        for object_item in self.dsObjects:
            object_item.ds_start()

    def search_datasources(self, search_item: str) -> dict:
        ''' Return dictionary with some available information '''
        for object_item in self.dsObjects:
            if object_item.searchIP(search_item):
                return {
                    "is_found": True,
                    "feed_name": object_item.getFeedName(),
                    "ip": search_item
                }
        return {
            "is_found": False,
            "feed_name": "",
            "ip": search_item
        }
