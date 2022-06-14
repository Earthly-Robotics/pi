import json, time


class AppComponent:
    network_controller = None
    sending = False
    msg_type = ""
    interval = 1

    def __init__(self, network_controller):
        self.network_controller = network_controller

    def format_component_data(self) -> tuple:
        """
        Formats the data of the component into a tuple that can be sent to the app
        """
        pass

    def update_app_data(self, ip):
        """
        Updates the data in the app with current data of the component.

        Parameters
        ----------
        ip : string
            IP address of the client that the update needs to be sent to
        Returns
        -------
            void
        """
        while self.sending:
            data = self.format_component_data()
            msg_obj = {
                "MT": self.msg_type,
            }
            for i in range(0, len(data), 2):
                msg_obj[data[i]] = data[i + 1]
            json_string = json.dumps(msg_obj)
            msg = str.encode(json_string)
            self.network_controller.send_message(msg, ip)
            time.sleep(self.interval)
