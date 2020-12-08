#!/usr/bin/python3 -u

from ThorlabsPM100 import ThorlabsPM100, USBTMC

from tango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from tango.server import Device, attribute, command, pipe, device_property

class ThorlabsPM100Tango(Device):

    Port = device_property(
        dtype="str",
        default_value="/dev/ttyTLPM100",
    )

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
                           doc="Conversionfactor",
                           memorized=True,
                           hw_memorized=True,)

    auto_range = attribute(label="Auto Range",
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
        self.inst = USBTMC(device=self.Port)
        self.power_meter = ThorlabsPM100(inst=self.inst)
        self.__conversion_factor = 1.0
        self.set_state(DevState.ON)

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
    ThorlabsPM100Tango.run_server()
