from .general import item, datetime_str, BikeData
from .connection import Connection

class BikePosition(BikeData):
    def __init__(self, connection: Connection, bikeid: int, cached: bool = True) -> None:
        super().__init__
        self._connection = connection
        self._bikeid = bikeid
        self._cached = cached
        self.refresh(self._cached)

    def refresh(self, cached: bool = True):
        if cached:
            params = {"cached": "true"}
        else:
            params = {"cached": "false"}
        self._data = self._connection.get_endpoint("bike/%s/position/" % self._bikeid, params)

    @property
    def latitude(self) -> float:
        return item(self._data, "latitude")

    @property
    def longitude(self) -> float:
        return item(self._data, "longitude")

    @property
    def altitude(self) -> int:
        return item(self._data, "altitude")

    @property
    def speed(self) -> float:
        return item(self._data, "speed")

    @property
    def timets(self) -> int:
        return item(self._data, "timets")

    @property
    def timets_str(self) -> str:
        return datetime_str(item(self._data, "timets"))

    @property
    def rcvts(self) -> int:
        return item(self._data, "rcvts")

    @property
    def rcvts_str(self) -> str:
        return datetime_str(item(self._data, "rcvts"))
