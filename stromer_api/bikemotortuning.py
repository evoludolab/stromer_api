from .general import item, BikeData
from .connection import Connection

# note: caching for "bike/<bikeid>/settings" request does not work 

class BikeMotorTuning(BikeData):
    def __init__(self, connection: Connection, bikeid: int, cached: bool = True) -> None:
        super().__init__
        self._connection = connection
        self._bikeid = bikeid
        self._cached = cached
        self.refresh(self._cached)

    def refresh(self, cached: bool = True):
        params = {"fields": "tuning_speed,tuning_torque,tuning_agility"}
        self._data = self._connection.get_endpoint("bike/%s/settings" % self._bikeid, params)

    @property
    def tuning_torque(self) -> int:
        return item(self._data, "tuning_torque")

    @property
    def tuning_speed(self) -> int:
        return item(self._data, "tuning_speed")

    @property
    def tuning_agility(self) -> int:
        return item(self._data, "tuning_agility")
