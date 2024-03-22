from typing import Iterable
from topologies_generation.topology_generator import create_topologies_datasource
from alerts.alertsmanager import alertmanager
from extdatasource.extdatasourcesfactory import DSFactory


class TopologyHandler:
    def __init__(self, topologies_datasource: Iterable[dict]) -> None:
        try:
            self._topologies_datasource = topologies_datasource
            # sel alert output to terminal
            alertmanager.setAlertOutput('terminal')

            # init  external data source and prepare data
            self.exDSFactory = DSFactory()
            self.exDSFactory.init_datasources()
            self.exDSFactory.start_datasources()
        except Exception as e:
            print(
                f"Error during Topology handler init. Operation is aborted. {e}")
            raise SystemExit(1)

    def _handle_topology(self, topology: dict) -> None:
        ip_list = [topology["source_ip"], topology["destination_ip"]]
        for el in ip_list:
            ret_res = self.exDSFactory.search_datasources(el)
            if ret_res["is_found"]:
                alertmanager.sendAlert(
                    alert=" !!!! ALERT !!!! IP Found in feed", alert_data=ret_res, output_type='terminal')
            else:
                alertmanager.sendAlert(
                    alert="IP not found in feed", alert_data=ret_res, output_type='terminal')

    @staticmethod
    def _validate_topology(topology: dict) -> bool:
        return {"source_ip", "source_port", "destination_ip", "destination_port", "topology_timestamp"} \
            .issubset(topology.keys())

    def handle_topologies(self) -> None:
        filtered_topologies = (topology for topology in self._topologies_datasource if
                               self._validate_topology(topology))

        for topology in filtered_topologies:
            try:
                self._handle_topology(topology)
            except Exception as e:
                print(f"Exception during handle topology. {e}")


def main():
    topologies_datasource = create_topologies_datasource()
    TopologyHandler(topologies_datasource).handle_topologies()


if __name__ == "__main__":
    main()
