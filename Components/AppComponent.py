class AppComponent:
    network_controller = None
    sending = False

    def __init__(self, network_controller):
        self.network_controller = network_controller

    def update_app_data(self, ip, interval=0):
        """
        Updates the data in the app with current data of the component.

        Parameters
        ----------
        interval : float, optional
            Time between each update that's sent to the app in seconds.
        ip : string
            IP address of the client that the update needs to be sent to
        Returns
        -------
            void
        """
        pass
