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
        self.msg_type = "WEIGHT"
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

    def format_component_data(self) -> tuple:
        """
        Gets the weight from the load cell and formats it for JSON Serialization.
        :return:
        A tuple with an even amount of elements.
        Must be formatted as followed: "x", "x_value".
        """
        return "Weight", self.measure_weight()
