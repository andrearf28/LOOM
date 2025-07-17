# LOOM/src/data_classes/LoomRow.py
class LoomRow:
    def __init__(
        self,
        unixtime: float,
        revolverpos: int,
        samplepos: float,
        pmtpos: float,
        wavelength: float,
        current: float,
        current_std: float,
        dc: float,
        dc_std: float,
        temperature: float,
        humidity: float
    ):
        self.unixtime = unixtime
        self.revolverpos = revolverpos
        self.samplepos = samplepos
        self.pmtpos = pmtpos
        self.wavelength = wavelength
        self.current = current
        self.current_std = current_std
        self.dc = dc
        self.dc_std = dc_std
        self.temperature = temperature
        self.humidity = humidity
