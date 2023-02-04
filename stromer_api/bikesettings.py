from .general import item, BikeData
from .connection import Connection

# note: caching for "bike/<bikeid>/settings" request does not work 

class BikeSettings(BikeData):
    def __init__(self, connection: Connection, bikeid: int) -> None:
        super().__init__(None)
        self._connection = connection
        self._bikeid = bikeid
        self.refresh()

    def refresh(self):
        params = {"fields": "auto_lock_mode,auto_power_off_time,date_format,distance_unit,language,speed_unit,clock_format"}
        self._data = self._connection.get_endpoint("bike/%s/settings/" % self._bikeid, params)

    @property
    def auto_lock_mode(self) -> bool:
        return item(self._data, "auto_lock_mode")

    @property
    def auto_power_off_time(self) -> int:
        return item(self._data, "auto_power_off_time")

    @property
    def clock_format(self) -> str:
        return item(self._data, "clock_format")

    @property
    def date_format(self) -> str:
        return item(self._data, "date_format")

    @property
    def distance_unit(self) -> str:
        return item(self._data, "distance_unit")

    @property
    def language(self) -> str:
        return item(self._data, "language")

    @property
    def speed_unit(self) -> str:
        return item(self._data, "speed_unit")
