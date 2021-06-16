#!/usr/bin/python3 -u

from ThorlabsPM100 import ThorlabsPM100 as tlpm100
from ThorlabsPM100 import USBTMC

from tango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from tango.server import Device, attribute, command, pipe, device_property

class ThorlabsPM100(Device):

    Port = device_property(
        dtype="str",
        default_value="/dev/ttyTLPM100",
    )

    sn = attribute(label="SN", dtype="str", access=AttrWriteType.READ,
                      doc="Sensor serial number")

    model = attribute(label="Model", dtype="str", access=AttrWriteType.READ,
                      doc="Sensor model")

    wavelength = attribute(label="Wavelength", dtype="float",
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ_WRITE,
                         doc="Correction wavelength")

    power = attribute(label="Power",
                      dtype="float",
                      format="%8.3f",
                      display_level=DispLevel.OPERATOR,
                      access=AttrWriteType.READ,
                      doc="Measured power")

    conversion = attribute(label="Conversion factor",
                           dtype="float",
                           format="%6.3e",
                           display_level=DispLevel.OPERATOR,
                           access=AttrWriteType.READ_WRITE,
                           doc="Conversion factor",
                           memorized=True,
                           hw_memorized=True,)

    auto_range = attribute(label="Auto range",
                           dtype="bool",
                           display_level=DispLevel.OPERATOR,
                           access=AttrWriteType.READ_WRITE,)

    upper_range = attribute(label="Range",
                           dtype="float",
                           format="%6.3e",
                           display_level=DispLevel.OPERATOR,
                           access=AttrWriteType.READ_WRITE,)

    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.INIT)

        try:
            self.info_stream('Connecting on Port: {:s}'.format(self.Port))
            self.inst = USBTMC(device=self.Port)
            self.power_meter = tlpm100(inst=self.inst)
            self.set_state(DevState.ON)
            idn = self.power_meter.system.sensor.idn.split(',')
            self.__model = idn[0]
            self.__sn = idn[1]
            self.info_stream('Connected to {:s} with SN: {:s}'.format(self.__model, self.__sn))
        except:
            self.info_stream('Not able to connect on Port: {:s}'.format(self.Port))
            self.set_state(DevState.OFF)

        self.__conversion_factor = 1.0

    def read_sn(self):
        return self.__sn

    def read_model(self):
        return self.__model

    def read_wavelength(self):
        return self.power_meter.sense.correction.wavelength

    def write_wavelength(self, value):
        self.wavelength = value
        self.power_meter.sense.correction.wavelength = value

    def read_auto_range(self):
        return bool(self.power_meter.sense.power.dc.range.auto)

    def write_auto_range(self, value):
        self.power_meter.sense.power.dc.range.auto = int(value)

    def read_upper_range(self):
        return float(self.power_meter.sense.power.dc.range.upper)

    def write_upper_range(self, value):
        self.power_meter.sense.power.dc.range.upper = value

    def read_conversion(self):
        return self.__conversion_factor

    def write_conversion(self, value):
        self.__conversion_factor = value

    def read_power(self):
        self.debug_stream('read power')
        power = self.power_meter.read
        return float(power * self.__conversion_factor)

if __name__ == "__main__":
    ThorlabsPM100.run_server()
