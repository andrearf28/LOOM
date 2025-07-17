# LOOM/src/data_classes/LoomSet.py

from typing import List
from .LoomRow import LoomRow

class LoomSet:
    def __init__(self, metadata: dict, data: List[LoomRow]):
        self._metadata = metadata
        self._data = data

    @property
    def metadata(self) -> dict:
        return self._metadata

    @property
    def data(self) -> List[LoomRow]:
        return self._data

    @property
    def currents(self) -> List[float]:
        return [row.current for row in self._data]

    @property
    def currents_std(self) -> List[float]:
        return [row.current_std for row in self._data]
    
    @property
    def dcs(self) -> List[float]:
        return [row.dc for row in self._data]

    @property
    def dcs_std(self) -> List[float]:
        return [row.dc_std for row in self._data]

    @property
    def wavelengths(self) -> List[float]:
        return [row.wavelength for row in self._data]

    @property
    def temperatures(self) -> List[float]:
        return [row.temperature for row in self._data]

    @property
    def humidities(self) -> List[float]:
        return [row.humidity for row in self._data]

    @property
    def times(self) -> List[float]:
        return [row.unixtime for row in self._data]

    @property
    def sample_positions(self) -> List[float]:
        return [row.samplepos for row in self._data]

    @property
    def pmt_positions(self) -> List[float]:
        return [row.pmtpos for row in self._data]

    @property
    def revolver_positions(self) -> List[int]:
        return [row.revolverpos for row in self._data]

    