from HX711 import *
import RPi.GPIO as GPIO


class LoadCell:
    data_pin = 6
    clock_pin = 5
    reference_unit = -1103
    offset = -108042
    hx = SimpleHX711(data_pin, clock_pin, reference_unit, offset)

    def __init__(self, data_pin=6, clock_pin=5, reference_unit=-1103, offset=-108042):
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
