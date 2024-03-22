from abc import ABC, abstractmethod
'''
Abstract class for external data soirces
Need to be used for implementation of new data sources
'''


class DSAbstract(ABC):

    @abstractmethod
    def ds_start()->None:
        pass

    @abstractmethod
    def searchIP()->bool:
        pass
