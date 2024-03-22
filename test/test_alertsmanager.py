from alerts.alertsmanager import AlertManager


def test_formatMessage():
    ''' Testing of format messafe in alert manager'''
    alertmanager = AlertManager()
    alert = "This is alert message"
    alert_data = {"is_found": True,
                  "feed_name": "TestFeedname",
                  "ip": "1.2.3.4"}
    output_type = 'terminal'
    formatted_message = "This is alert message IP: 1.2.3.4 Feed Name: TestFeedname"

    assert alertmanager._formatMessage(
        alert=alert, message_data=alert_data, output_type=output_type) == formatted_message
