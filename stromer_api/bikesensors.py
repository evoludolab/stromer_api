from .general import item, BikeData
from .connection import Connection

# note: caching for "bike/<bikeid>/settings" request does not work 

class BikeSensors(BikeData):
    def __init__(self, connection: Connection, bikeid: int, ) -> None:
        super().__init__
        self._connection = connection
        self._bikeid = bikeid
        self.refresh()

    def refresh(self):
        params = {"fields": "recup_level_user_offset,user_torque_sensitivity"}
        self._data = self._connection.get_endpoint("bike/%s/settings" % self._bikeid, params)

    @property
    def user_torque_sensitivity(self) -> int:
        return item(self._data, "user_torque_sensitivity")

    @property
    def recup_level_user_offset(self) -> int:
        return item(self._data, "recup_level_user_offset")
