from typing import Union, Literal

output_types = Literal['terminal', 'db', 'stream']


class AlertManager:
    '''
    A class representing alert manager. 
    Support termina , db and stream output for alerts
    --- only terminal is currently impkemented ----
    '''
    alert_target = []

    def __init__(self) -> None:
        pass

    def setAlertOutput(self, output_type: Union[output_types]) -> None:
        self.alert_target.append(output_type)

    def removeAlertOutput(self, output_type: Union[output_types]) -> None:
        self.alert_target.remove(output_type)

    def sendAlert(self, alert: str, alert_data: dict, output_type: Union[output_types]) -> None:
        try:
            self._alertFactory(
                alert=alert, alert_data=alert_data, output_type=output_type)
        except Exception as e:
            print("Error during alert sending. Print alert to start output")
            print(alert)

    def _alertFactory(self, alert: str, alert_data: dict, output_type: Union[output_types]) -> None:
        '''
        Alert out manager. Will send alert into designated out out
        '''
        if output_type not in self.alert_target:
            print(
                f"Alert target {output_type} not support. Use setAlertOutput to activate alert targer")
            return

        if output_type == 'terminal':
            self._terminalOutput(alert=self._formatMessage(
                alert, alert_data, output_type))
        if output_type == 'db':
            self._dbOutput(alert=self._formatMessage(
                alert, alert_data, output_type))
        if output_type == 'stream':
            self._streamOutput(alert=self._formatMessage(
                alert, alert_data, output_type))

    def _formatMessage(self, alert: str, message_data: dict, output_type: Union[output_types]) -> any:
        '''Formatting message based on  output type'''
        if output_type == 'terminal':
            return f"{alert} IP: {message_data['ip']} Feed Name: {message_data['feed_name']}"
        if output_type == 'db':
            return ""
        if output_type == 'stream':
            return ""

    def _initDbOutput() -> None:
        '''
        Init nessesary objects and connections for db alerts output
        '''
        pass

    def _initStreamOutput() -> None:
        '''
        Init nessesary for stream connections
        '''
        pass

    def _terminalOutput(self, alert: str) -> None:
        print(alert)

    def _dbOutput(self, alert: str) -> None:
        '''
        send alert to db out target
        '''
        pass

    def _streamOutput(self, alert: str) -> None:
        '''
        send alert to sream out target
        '''
        pass


alertmanager = AlertManager()
