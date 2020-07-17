from ThorlabsPM100 import ThorlabsPM100, USBTMC

from tango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from tango.server import Device, attribute, command, pipe, device_property

class ThorlabsPM100Tango(Device):

    Port = device_property(
        dtype="str",
        default_value="/dev/usbtmc0",
    )

    wavelength = attribute(label="Wavelength (nm)", dtype=float,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ_WRITE,
                         doc="Correction wavelength")

    power = attribute(label="Power (W)", dtype=float,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ,
                         doc="Measured power")

    conversion = attribute(label="Conversionfactor", dtype=float,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ_WRITE,
                         doc="Conversionfactor",
                         memorized=True,
                         hw_memorized=True,)


    def init_device(self):
        Device.init_device(self)
        self.inst = USBTMC(device=self.Port)
        self.power_meter = ThorlabsPM100(inst=self.inst)
        self._conversion_factor = 1.0
        self.set_state(DevState.ON)

    def read_wavelength(self):
        return self.power_meter.sense.correction.wavelength
    
    def write_wavelength(self, wav):
        self.wavelength = wav
        self.power_meter.sense.correction.wavelength = wav
        
    def read_conversion(self):
        return self._conversion_factor
    
    def write_conversion(self, value):
        self._conversion_factor = value

    def read_power(self):
        self.debug_stream('read power')
        power = self.power_meter.read
        return power * self._conversion_factor
    
    def read_Test(self):
        return self.Test


if __name__ == "__main__":
    ThorlabsPM100Tango.run_server()
