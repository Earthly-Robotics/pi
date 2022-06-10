import json
import time

from HX711 import *
import RPi.GPIO as GPIO

from Components.AppComponent import AppComponent


class LoadCell(AppComponent):
    data_pin = 6
    clock_pin = 5
    reference_unit = -1103
    offset = -108042
    hx = SimpleHX711(data_pin, clock_pin, reference_unit, offset)

    def __init__(self, network_controller, data_pin=6, clock_pin=5, reference_unit=-1103, offset=-108042):
        super().__init__(network_controller)
        self.hx.setUnit(Mass.Unit.G)
        self.hx.zero()

    def measure_weight(self, samples=15):
        """
        Measures the weight that the HX711 load cell is holding

        Parameters
        ----------
        samples : int, optional
            Amount of samples
        Returns
        -------
            The weight as a string. "x.xx g"
        """
        return self.hx.weight(samples)

    def update_app_data(self, ip, interval=0):
        while self.sending:
            message = {
                "MT": "LC",
                "W": str(self.measure_weight())
            }
            json_string = json.dumps(message)
            msg = str.encode(json_string)
            self.network_controller.send_message(msg, ip)
            time.sleep(interval)
