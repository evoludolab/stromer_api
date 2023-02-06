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
        self._data = self._connection.get_endpoint("bike/%s/settings/" % self._bikeid, params)

    @property
    def tuning_torque(self) -> int:
        return item(self._data, "tuning_torque")

    @property
    def tuning_speed(self) -> int:
        return item(self._data, "tuning_speed")

    @property
    def tuning_agility(self) -> int:
        return item(self._data, "tuning_agility")
    
    def set(self, speed = None, torque = None, agility = None):
        if speed is None:
            speed = self.tuning_speed
        if torque is None:
            torque = self.tuning_torque
        if agility is None:
            agility = self.tuning_agility
        # viable range for speed, torque and agility: [0-100]
        speed = max(min(speed, 100), 0)
        torque = max(min(torque, 100), 0)
        agility = max(min(agility, 100), 0)
        data = {"tuning_speed": speed, "tuning_torque": torque, "tuning_agility": agility}
        # note: all three settings must be set at the same time otherwise the POST request
        #   is rejected with a syntax error
        return self._connection.post_endpoint("bike/%s/settings/" % self._bikeid, data)
